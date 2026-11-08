"""A grading session for an outside rater, in Ukrainian: a blind real-or-AI test, the task in brief, then the pre-final
sets and cards graded beside the real ones. Answers go to runs/prefinal/outside/ratings.json, apart from the
producer's runs/ratings.json.

    outside_rating.py build      fix the sample once the runs are done
    outside_rating.py serve      then open http://127.0.0.1:8766
    outside_rating.py summary    what the answers say

Five candidate genres for three sets: every variant is shown whole in the sets part, and a random half of each variant
is graded card by card, to keep the session near 60 minutes. The blind test comes first, before the rater knows the
topics or has seen our cards labelled: the real cards are all from a summer collection and ours are film genres, so
knowing either would give ours away by topic. Generated cards are 430x480 like the real ones, with the same sharpness
and no compression marks, so file traits give nothing away.
Each generated card in the blind test faces a real card of the same art category.
"""

import argparse
import json
import random
import sys
import threading
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from math import comb
from pathlib import Path
from statistics import mean
from urllib.parse import unquote

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules
from common import ROOT, best_try, load_json, save_json  # noqa: E402

RUNS = {genre: f"prefinal/{genre}" for genre in ("western", "sci-fi", "horror", "period-drama", "detective")}
NAMES = {"western": "Вестерн", "sci-fi": "Фантастика", "horror": "Жахи", "period-drama": "Історична драма",
         "detective": "Детектив"}
CAST = "prefinal/cast"
WINDOWS = ("Seafaring", "Music Fest", "Road Trip")  # real sets shown as game windows in the task brief
COMPARE = "Beach"  # the real set shown above our variants
BLIND_PER_VARIANT, GRADED_PER_VARIANT = 2, 5
OUT = ROOT / "runs" / "prefinal" / "outside"
ITEMS, RATINGS = OUT / "items.json", OUT / "ratings.json"
SERVED = ("materials/card_examples/", "materials/collection_examples/", "runs/")
LOCK = threading.Lock()


def chosen(run):
    """(brief, path) of each card's chosen drawing in a run."""
    history = load_json(ROOT / "runs" / run / "check.json")
    for brief in load_json(ROOT / "runs" / run / "briefs.json"):
        if history.get(brief["id"]):
            yield brief, f"runs/{run}/tries/{best_try(history[brief['id']])['try_id']}.png"


def build():
    if ITEMS.exists():
        raise SystemExit(f"{ITEMS.relative_to(ROOT)} exists and answers refer to it; move it away to rebuild")
    rng = random.Random(7)
    real = load_json(ROOT / "analysis" / "cards.json")
    sets = {s["title"]: s for s in load_json(ROOT / "analysis" / "sets.json")}
    names = {c["id"]: c["name"] for c in real}
    image = lambda card_id: f"materials/card_examples/{card_id}.png"  # noqa: E731

    ours = {genre: list(chosen(run)) for genre, run in RUNS.items()}
    ours["cast"] = list(chosen(CAST)) if (ROOT / "runs" / CAST / "check.json").exists() else []

    # Blind: two cards per variant at random, every cast card, each against a real card of its art category
    picked = []
    for genre, run in RUNS.items():
        for variant in sorted({b["variant"] for b, _ in ours[genre]}):
            pool = [(b, p) for b, p in ours[genre] if b["variant"] == variant]
            picked += [(genre, run, b, p) for b, p in rng.sample(pool, min(BLIND_PER_VARIANT, len(pool)))]
    picked += [("cast", CAST, b, p) for b, p in ours["cast"]]
    by_category = defaultdict(list)
    for card in real:
        by_category[card["form"]["staging"]["art_category"]].append(card)
    for cards in by_category.values():
        rng.shuffle(cards)
    blind = []
    for genre, run, brief, path in picked:
        twin = by_category[brief["card"]["category"]].pop()
        blind.append({"id": f"blind/ai/{run}/{brief['id']}", "truth": "ai", "group": genre, "name": brief["card"]["name"],
                      "image": path})
        blind.append({"id": f"blind/real/{twin['id']}", "truth": "real", "group": "real", "name": twin["name"],
                      "image": image(twin["id"])})
    rng.shuffle(blind)

    genres = []
    for genre, run in RUNS.items():
        plan = load_json(ROOT / "runs" / run / "plan.json")
        variants = defaultdict(list)
        for brief, path in ours[genre]:
            variants[brief["variant"]].append({"name": brief["card"]["name"], "image": path})
        genres.append({"id": f"set/{run}", "genre": genre, "title": f"{NAMES[genre]} ({plan['title']})",
                       "variants": [{"variant": v, "cards": cards} for v, cards in sorted(variants.items())]})

    graded = [(genre, run, b, p) for genre, run in RUNS.items()
              for variant in sorted({b["variant"] for b, _ in ours[genre]})
              for b, p in rng.sample([(b, p) for b, p in ours[genre] if b["variant"] == variant],
                                     min(GRADED_PER_VARIANT, sum(b["variant"] == variant for b, _ in ours[genre])))]
    graded += [("cast", CAST, b, p) for b, p in ours["cast"]]
    cards = [{"id": f"card/{run}/{brief['id']}", "group": genre, "variant": brief["variant"], "name": brief["card"]["name"],
              "image": path, "references": [image(i) for i in brief["references"]]} for genre, run, brief, path in graded]
    rng.shuffle(cards)

    save_json(ITEMS, {
        "windows": [f"materials/collection_examples/{sets[title]['id']}.png" for title in WINDOWS],
        "compare": {"title": COMPARE, "cards": [{"name": names[i], "image": image(i)} for i in sets[COMPARE]["cards"]]},
        "blind": blind, "sets": genres, "cards": cards})
    print(f"{len(blind)} blind cards ({len(picked)} ours), {len(genres)} genres, {len(cards)} cards to grade")


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path).lstrip("/")
        if not path:
            return self.reply(PAGE.encode(), "text/html; charset=utf-8")
        if path == "data":
            ratings = load_json(RATINGS) if RATINGS.exists() else {}
            return self.reply(json.dumps({"items": load_json(ITEMS), "ratings": ratings}).encode(), "application/json")
        file = (ROOT / path).resolve()
        if path.startswith(SERVED) and file.is_relative_to(ROOT) and file.suffix == ".png" and file.exists():
            return self.reply(file.read_bytes(), "image/png")
        self.send_error(404)

    def do_POST(self):
        entry = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with LOCK:
            data = load_json(RATINGS) if RATINGS.exists() else {}
            data[f"{entry['id']}|{entry['rater']}"] = entry
            save_json(RATINGS, data)
        self.reply(b"{}", "application/json")

    def reply(self, body, kind):
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def summary():
    items = load_json(ITEMS)
    blind = {i["id"]: i for i in items["blind"]}
    cards = {i["id"]: i for i in items["cards"]}
    answers = defaultdict(dict)
    for entry in (load_json(RATINGS) if RATINGS.exists() else {}).values():
        answers[entry["rater"]][entry["id"]] = entry
    for rater, given in answers.items():
        print(f"== {rater}")
        rows = [(blind[i], a["score"]) for i, a in given.items() if i in blind and a.get("score")]
        if rows:
            n, right = len(rows), sum((score >= 3) == (item["truth"] == "ai") for item, score in rows)
            tail = sum(comb(n, k) for k in range(min(right, n - right) + 1)) / 2 ** n
            ai = [s for item, s in rows if item["truth"] == "ai"]
            real = [s for item, s in rows if item["truth"] == "real"]
            auc = mean((a > r) + 0.5 * (a == r) for a in ai for r in real) if ai and real else float("nan")
            print(f"blind: {right} of {n} right ({right / n:.0%}), two-sided p {min(1, 2 * tail):.3f} against chance; "
                  f"AUC {auc:.2f} (0.5 is chance)")
            print(f"  real cards called real {sum(s <= 2 for s in real)} of {len(real)}")
            for group in (*RUNS, "cast"):
                scores = [s for item, s in rows if item["group"] == group]
                if scores:
                    caught = [item["name"] for item, s in rows if item["group"] == group and s == 4]
                    print(f"  {group}: called AI {sum(s >= 3 for s in scores)} of {len(scores)}; surely AI: "
                          f"{', '.join(caught) or 'none'}")
        for genre in items["sets"]:
            entry = given.get(genre["id"], {})
            grades = entry.get("grades", {})
            if grades or entry.get("best"):
                print(f"set {genre['genre']}: grades {grades}, best variant {entry.get('best')}"
                      + (f" | {entry['comment']}" if entry.get("comment") else ""))
        graded = [(cards[i], a) for i, a in given.items() if i in cards and a.get("grade")]
        groups = defaultdict(list)
        for card, answer in graded:
            groups[(card["group"], card["variant"])].append(answer)
        for (group, variant), entries in sorted(groups.items()):
            print(f"cards {group} v{variant}: mean grade {mean(a['grade'] for a in entries):.2f} from {len(entries)}, "
                  f"broken {sum(bool(a.get('broken')) for a in entries)}")
        for card, answer in sorted(graded, key=lambda row: (row[0]["group"], row[0]["variant"], row[0]["id"])):
            mark = " X" if answer.get("broken") else ""
            note = f" | {answer['comment']}" if answer.get("comment") else ""
            print(f"  {card['id'].split('/', 1)[1]} {card['name']}: {answer['grade']}{mark}{note}")
        for item_id, answer in given.items():
            if item_id in blind and answer.get("comment"):
                item = blind[item_id]
                print(f"  blind {item['truth']} {item['name']} ({answer['score']}): {answer['comment']}")
        if given.get("genres", {}).get("keep"):
            print(f"genres to keep: {', '.join(given['genres']['keep'])}")
        if given.get("final", {}).get("comment"):
            print(f"final: {given['final']['comment']}")


PAGE = """<!doctype html><html lang="uk"><head><meta charset="utf-8"><title>Оцінка карток</title>
<style>
:root { --bg: #18181b; --panel: #26262b; --button: #3a3a42; --text: #ececf1; --muted: #a0a0ab; --accent: #f5b83d; }
body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.5 system-ui, sans-serif; }
header { display: flex; gap: 8px; align-items: center; padding: 10px 20px; background: var(--panel); flex-wrap: wrap; }
button { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }
button.on { background: var(--accent); color: #000; }
button:disabled { opacity: .35; cursor: default; }
input, textarea { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 8px; font: inherit; }
main { max-width: 1280px; margin: 0 auto; padding: 16px 20px 40px; }
.text { max-width: 760px; margin: 0 auto; }
.hint, figcaption, #progress { color: var(--muted); }
.hint { text-align: center; max-width: 900px; margin: 8px auto 16px; }
.cards { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
figure { margin: 0; text-align: center; }
img { display: block; max-width: 100%; border-radius: 10px; }
.blind img { width: 430px; }
.grade img { width: min(290px, 22vw); }
.grade figure:first-child img { outline: 3px solid var(--accent); }
.window { display: block; width: min(820px, 100%); aspect-ratio: 1.4; object-fit: cover; margin: 12px auto; }
.set { display: grid; grid-template-columns: 110px repeat(10, 1fr); gap: 6px; align-items: center; margin: 6px 0; }
.set figure img { width: 100%; border-radius: 6px; }
.set figcaption { font-size: 11px; line-height: 1.2; }
.set .label { font-weight: 600; }
.set.real .label { color: var(--muted); }
.votes { display: flex; gap: 6px; flex-wrap: wrap; justify-content: center; margin: 2px 0 16px 116px; }
.row { display: flex; gap: 8px; justify-content: center; margin: 12px 0; flex-wrap: wrap; }
textarea { display: block; width: 100%; max-width: 900px; height: 52px; margin: 0 auto; box-sizing: border-box; }
h1, h2 { font-weight: 650; }
</style></head><body>
<header><b>Оцінка карток</b><span id="tabs"></span><span id="progress" style="margin-left:auto"></span></header>
<main id="main"></main>
<script>
const STEPS = [["start", "Початок"], ["blind", "1 · Справжня чи ШІ"], ["task", "Про завдання"], ["sets", "2 · Набори"], ["cards", "3 · Картки"], ["end", "Кінець"]];
const BLIND = ["Точно з гри", "Скоріше з гри", "Скоріше ШІ", "Точно ШІ"];
const GRADES = ["", "Явно інакше", "Помітно інакше", "Близько", "Дуже близько", "Не відрізнити"];
const SET_GRADES = ["", "Явно ні", "Скоріше ні", "Можливо", "Так, з дрібницями", "Так"];
let items, ratings = {}, step = "start", rater = "";
const position = { blind: 0, sets: 0, cards: 0 };
try { rater = localStorage.getItem("outside-rater") || ""; } catch (e) {}
const key = id => id + "|" + rater;
const answer = id => ratings[key(id)];
const done = list => list.filter(i => answer(i.id)).length;
const blindDone = () => items && done(items.blind) === items.blind.length;
const setRow = (label, cards, real) => `<div class="set ${real ? "real" : ""}"><div class="label">${label}</div>${cards.map(c =>
  `<figure><img src="/${c.image}"><figcaption>${esc(c.name)}</figcaption></figure>`).join("")}</div>`;
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

function save(id, fields) {
  const entry = { ...answer(id), ...fields, id, rater, time: new Date().toISOString() };
  ratings[key(id)] = entry;
  fetch("/rate", { method: "POST", body: JSON.stringify(entry) });
}

function go(next) { step = next; show(); window.scrollTo(0, 0); }

function tabs() {
  document.getElementById("tabs").innerHTML = STEPS.map(([id, label]) => {
    const locked = !rater ? id !== "start" : (id === "blind" ? blindDone() : id !== "start" && !blindDone());
    return `<button data-step="${id}" class="${step === id ? "on" : ""}" ${locked && step !== id ? "disabled" : ""}>${label}</button>`;
  }).join(" ");
  document.querySelectorAll("[data-step]").forEach(b => b.onclick = () => go(b.dataset.step));
  document.getElementById("progress").textContent = items && rater ?
    `Частина 1: ${done(items.blind)}/${items.blind.length} · Набори: ${done(items.sets)}/${items.sets.length}${answer("genres") ? " ✓" : ""} · Картки: ${done(items.cards)}/${items.cards.length}` : "";
}

const views = {
  start() {
    return `<div class="text"><h1>Оцінка ігрових карток</h1>
      <p>Дякуємо, що погодилися допомогти! Це займе близько години. Кожна відповідь зберігається одразу, тож можна зробити перерву й продовжити пізніше на цій самій сторінці.</p>
      <ol><li><b>Справжня чи ШІ?</b> По одній картці: вирішіть, чи вона з гри, чи її намалював ШІ. Близько 12 хвилин.</li>
      <li><b>Про завдання:</b> коротко, що ми робимо. 3 хвилини.</li>
      <li><b>Набори:</b> чи тримаються наші набори як ціле і які жанри залишити. Близько 11 хвилин.</li>
      <li><b>Картки:</b> половина наших карток, кожна поруч зі справжніми, оцінка від 1 до 5. Близько 27 хвилин.</li></ol>
      <p>Порядок важливий: спершу сліпий тест, поки ви ще не бачили наших карток і не знаєте тем. Тому, будь ласка, не шукайте нічого про ці картки заздалегідь.</p>
      <p>Ваше ім'я: <input id="name" value="${esc(rater)}" size="16"> <button id="begin">Почати</button></p></div>`;
  },
  blind() {
    if (blindDone()) return `<div class="text"><h2>Частину 1 завершено</h2><p>Результат покажемо в кінці.</p><button id="ahead">Далі: про завдання</button></div>`;
    const list = items.blind, i = Math.max(0, list.findIndex(x => !answer(x.id))), item = list[i];
    position.blind = i;
    return `<p class="hint">Частина карток — справжні, з мобільної гри Playrix, решту намалював наш ШІ-інструмент. Скільки яких — не кажемо. Теми карток різні: не вгадуйте за темою, дивіться, як картку намальовано. Відповідайте за першим враженням, кілька секунд на картку. Клавіші 1–4.</p>
      <div class="cards blind"><figure><img src="/${item.image}"><figcaption>${i + 1} з ${list.length}</figcaption></figure></div>
      <textarea id="comment" placeholder="Необов'язково: що підказало?"></textarea>
      <div class="row">${BLIND.map((label, k) => `<button data-score="${k + 1}">${k + 1} · ${label}</button>`).join("")}</div>`;
  },
  task() {
    return `<div class="text"><h2>Про завдання</h2>
      <p>Це тестове завдання Playrix на роль AI-продюсера. Треба зробити інструмент, який за темою й побажаннями продюсера сам, без ручної роботи, створює набір колекційних карток у стилі гри. Перевірка така: чи можна поставити наш набір у гру поруч зі справжніми так, щоб гравці не помітили різниці ні в ідеї, ні в малюнку.</p>
      <p><b>Як влаштована колекція.</b> Колекція в грі складається з 16 наборів по 10 карток. Набір — це підтема колекції: у літній колекції, наприклад, «Пляж», «Сад», «Спорт». Картки — це предмети цієї підтеми: для «Пляжу» це м'яч, замок з піску, пляжна сумка. Ось три справжні набори так, як їх бачить гравець:</p></div>
      ${items.windows.map(src => `<img class="window" src="/${src}">`).join("")}
      <div class="text"><p><b>Що ми зробили.</b> За умовою потрібно три набори для колекції «Кіно», кожен про свій жанр. Лише предмети, без персонажів: картки з персонажами в грі «золоті», а їх умова не просить. Ми зробили набори для п'яти жанрів (Вестерн, Фантастика, Жахи, Історична драма, Детектив) і залишимо три. Кожен набір має три варіанти, з яких продюсер обирає один. Окремо, як бонус, є кілька карток з персонажами гри.</p>
      <p>Все, що ви побачите далі, намалював ШІ. Ваші оцінки допоможуть вибрати жанри, варіанти й картки та побачити, що ще видає ШІ.</p>
      <button id="ahead">Далі: набори</button></div>`;
  },
  sets() {
    if (position.sets === items.sets.length) return views.genres();
    const genre = items.sets[position.sets], entry = answer(genre.id) || {}, grades = entry.grades || {}, row = setRow;
    return `<p class="hint">${position.sets + 1} з ${items.sets.length}: <b>${esc(genre.title)}</b>. Три варіанти набору по 10 карток, зверху для порівняння — справжній набір із гри. Чи міг би кожен варіант стояти в грі поруч зі справжніми: за ідеєю (зрозумілий, цілісний набір предметів на тему) і за виглядом (картки тримаються разом)? Оцініть кожен і виберіть найкращий.</p>
      ${row("Справжній: " + esc(items.compare.title), items.compare.cards, true)}
      ${genre.variants.map(v => row("Варіант " + v.variant, v.cards) + `<div class="votes">${[1, 2, 3, 4, 5].map(g =>
        `<button data-variant="${v.variant}" data-grade="${g}" class="${grades[v.variant] === g ? "on" : ""}">${g} · ${SET_GRADES[g]}</button>`).join("")}</div>`).join("")}
      <div class="row">${genre.variants.map(v => `<button data-best="${v.variant}" class="${entry.best === v.variant ? "on" : ""}">Найкращий: варіант ${v.variant}</button>`).join("")}</div>
      <textarea id="comment" placeholder="Коментар, необов'язково: що вибивається з набору?">${esc(entry.comment || "")}</textarea>
      <div class="row"><button id="back">← Назад</button><button id="next">${position.sets + 1 < items.sets.length ? "Далі →" : "Далі: вибір жанрів"}</button></div>`;
  },
  genres() {
    const keep = (answer("genres") || {}).keep || [];
    return `<p class="hint">Останнє в цій частині: які три жанри ви б залишили для колекції? Кожен жанр показано варіантом, який ви назвали найкращим.</p>
      ${items.sets.map(g => {
        const best = (answer(g.id) || {}).best, v = g.variants.find(x => x.variant === best) || g.variants[0];
        return setRow(esc(g.title), v.cards) + `<div class="votes"><button data-keep="${g.genre}" class="${keep.includes(g.genre) ? "on" : ""}">${keep.includes(g.genre) ? "✓ Залишити" : "Залишити"}</button></div>`;
      }).join("")}
      <p class="hint">Вибрано ${keep.length} з 3</p>
      <div class="row"><button id="back">← Назад</button><button id="next">Далі: картки</button></div>`;
  },
  cards() {
    const item = items.cards[position.cards], entry = answer(item.id) || {};
    return `<p class="hint">У рамці — наша картка «${esc(item.name)}», поруч — справжні картки з гри того ж типу. Чи могла б наша стояти поруч із ними? Якщо щось зламано (предмет так не збудуєш, деталі не з'єднуються, перспектива не сходиться), натисніть X. Оцінку ставте останньою: вона одразу переводить до наступної картки. Клавіші X, 1–5, стрілки.</p>
      <div class="cards grade"><figure><img src="/${item.image}"><figcaption>наша · ${position.cards + 1} з ${items.cards.length}</figcaption></figure>
      ${item.references.map(src => `<figure><img src="/${src}"><figcaption>з гри</figcaption></figure>`).join("")}</div>
      <div class="row"><button id="broken" class="${entry.broken ? "on" : ""}">X · Щось зламано</button></div>
      <textarea id="comment" placeholder="Коментар, необов'язково: що не так?">${esc(entry.comment || "")}</textarea>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry.grade === g ? "on" : ""}">${g} · ${GRADES[g]}</button>`).join("")}</div>
      <div class="row"><button id="back">← Назад</button><button id="next">Далі →</button></div>`;
  },
  end() {
    const rows = items.blind.map(i => [i, answer(i.id)]).filter(([, a]) => a && a.score);
    const right = rows.filter(([i, a]) => (a.score >= 3) === (i.truth === "ai")).length;
    const ai = rows.filter(([i]) => i.truth === "ai"), real = rows.filter(([i]) => i.truth === "real");
    const left = items.cards.length - done(items.cards), sets = items.sets.length - done(items.sets), entry = answer("final") || {};
    return `<div class="text"><h2>Дякуємо!</h2>
      <p>Сліпий тест: ви правильно визначили <b>${right} з ${rows.length}</b> карток (навмання вийшла б приблизно половина). Карток ШІ розпізнано ${ai.filter(([, a]) => a.score >= 3).length} з ${ai.length}, справжніх визнано справжніми ${real.filter(([, a]) => a.score <= 2).length} з ${real.length}.</p>
      ${sets ? `<p>Ще не оцінено наборів: ${sets}. Можна повернутися до частини 2.</p>` : ""}
      ${left ? `<p>Ще не оцінено карток: ${left}. Можна повернутися до частини 3.</p>` : ""}
      <p>Загальне враження: що найбільше видає ШІ? Що вийшло добре?</p>
      <textarea id="final" style="height:120px">${esc(entry.comment || "")}</textarea>
      <div class="row"><button id="send">Зберегти</button></div><p id="saved" class="hint"></p></div>`;
  },
};

function show() {
  tabs();
  document.getElementById("main").innerHTML = views[step]();
  const on = (id, f) => { const el = document.getElementById(id); if (el) el.onclick = f; };
  const comment = () => (document.getElementById("comment") || {}).value || "";
  on("begin", () => {
    rater = document.getElementById("name").value.trim();
    if (!rater) return;
    try { localStorage.setItem("outside-rater", rater); } catch (e) {}
    go(blindDone() ? "task" : "blind");
  });
  on("ahead", () => go(step === "blind" ? "task" : "sets"));
  document.querySelectorAll("[data-score]").forEach(b => b.onclick = () => {
    save(items.blind[position.blind].id, { score: Number(b.dataset.score), comment: comment() });
    show();
  });
  if (step === "sets" && position.sets === items.sets.length) {
    document.querySelectorAll("[data-keep]").forEach(b => b.onclick = () => {
      const keep = ((answer("genres") || {}).keep || []).slice(), at = keep.indexOf(b.dataset.keep);
      if (at >= 0) keep.splice(at, 1); else if (keep.length < 3) keep.push(b.dataset.keep);
      save("genres", { keep }); show();
    });
    on("back", () => { position.sets--; show(); });
    on("next", () => go("cards"));
  } else if (step === "sets") {
    const genre = items.sets[position.sets];
    const update = fields => save(genre.id, { comment: comment(), ...fields });
    document.querySelectorAll("[data-variant]").forEach(b => b.onclick = () => {
      update({ grades: { ...(answer(genre.id) || {}).grades, [b.dataset.variant]: Number(b.dataset.grade) } }); show();
    });
    document.querySelectorAll("[data-best]").forEach(b => b.onclick = () => { update({ best: Number(b.dataset.best) }); show(); });
    document.getElementById("comment").onchange = () => update({});
    on("back", () => { position.sets = Math.max(0, position.sets - 1); show(); });
    on("next", () => { position.sets++; show(); window.scrollTo(0, 0); });
  }
  if (step === "cards") {
    const item = items.cards[position.cards];
    document.querySelectorAll("[data-grade]").forEach(b => b.onclick = () => grade(Number(b.dataset.grade)));
    on("broken", () => { save(item.id, { broken: !(answer(item.id) || {}).broken, comment: comment() }); show(); });
    document.getElementById("comment").onchange = () => save(item.id, { comment: comment() });
    on("back", () => move(-1));
    on("next", () => move(1));
  }
  on("send", () => { save("final", { comment: document.getElementById("final").value }); document.getElementById("saved").textContent = "Збережено. Дякуємо!"; });
}

function move(by) {
  const next = position.cards + by;
  if (next >= items.cards.length) return go("end");
  position.cards = Math.max(0, next);
  show();
}

function grade(g) {
  const item = items.cards[position.cards];
  save(item.id, { grade: g, comment: (document.getElementById("comment") || {}).value || "" });
  move(1);
}

document.onkeydown = event => {
  if (["TEXTAREA", "INPUT"].includes(event.target.tagName) || !items || !rater) return;
  const press = event.key.toLowerCase();
  if (step === "blind" && !blindDone() && "1234".includes(press) && press) {
    save(items.blind[position.blind].id, { score: Number(press), comment: (document.getElementById("comment") || {}).value || "" });
    show();
  } else if (step === "cards") {
    if ("12345".includes(press) && press) grade(Number(press));
    else if (press === "x") document.getElementById("broken").click();
    else if (event.key === "ArrowRight") move(1);
    else if (event.key === "ArrowLeft") move(-1);
  }
};

fetch("/data").then(r => r.json()).then(data => {
  items = data.items; ratings = data.ratings;
  position.cards = Math.max(0, items.cards.findIndex(i => !answer(i.id)));
  const open = items.sets.findIndex(i => !answer(i.id));
  position.sets = open >= 0 ? open : answer("genres") ? 0 : items.sets.length;
  if (rater) {  // a reload resumes at the first unfinished part
    const sets = done(items.sets), cards = done(items.cards);
    step = !blindDone() ? "blind" : !sets && !cards ? "task" : sets < items.sets.length || !answer("genres") ? "sets"
      : cards < items.cards.length ? "cards" : "end";
  }
  show();
});
</script></body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("build", "serve", "summary"))
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    if args.action == "build":
        build()
    elif args.action == "summary":
        summary()
    else:
        if not ITEMS.exists():
            raise SystemExit("run build first, once the runs are done")
        print(f"open http://127.0.0.1:{args.port}", flush=True)
        try:
            ThreadingHTTPServer(("127.0.0.1", args.port), Page).serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
