"""The morning review of the final sets, 2026-11-08. Answers go to runs/ratings.json as the producer's ratings.

Sets: the three final sets and the cast cards, beside a real set; grade each set 1-5 and comment.
Cards: each final card beside its three references, with every candidate drawn for it and the outside rater's grade of
the same card in the pre-final set. Grade 1-5, mark it broken, comment, or pick another candidate.
Blind: the overnight arms of experiments/night.py, unlabelled. Twins: a real card and two redraws, the style before
the night and one arm (smooth surfaces, adopted, or one camera), shuffled: pick the closer one and mark any that is broken. Broken cards:
the nine pre-final cards graded broken, drawn by the current pipeline and by each perspective arm, shuffled: does each
work as built?

    final_review.py build      once the final runs are done
    final_review.py serve      then open http://127.0.0.1:8767
    final_review.py summary    what the answers say
"""

import argparse
import json
import random
import sys
import threading
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from statistics import mean
from urllib.parse import unquote

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules
from common import ROOT, best_try, load_json, save_json  # noqa: E402

FINAL = {"western": ("final3/western", 1), "period-drama": ("final3/period-drama-2", 3),
         "detective": ("final3/detective-3", 2)}
CAST = "final2/cast"
COMPARE = "Beach"  # the real set shown above ours
TWIN_ARMS = {"ns2": "smooth surfaces", "nc": "one camera"}
TWINS_PER_ARM = 12
ITEMS = ROOT / "runs" / "final3" / "review.json"
RATINGS = ROOT / "runs" / "ratings.json"
OUTSIDE = ROOT / "runs" / "prefinal" / "outside" / "ratings.json"
SERVED = ("materials/card_examples/", "runs/")
LOCK = threading.Lock()


def final_cards(run, group, source, variant):
    """Each card of a final run: the chosen drawing, every candidate, references, and the same card in the pre-final
    run it came from (source, variant), with the outside rater's grade."""
    folder = ROOT / "runs" / run
    history = load_json(folder / "check.json")
    outside = load_json(OUTSIDE) if OUTSIDE.exists() else {}
    past_history = load_json(ROOT / "runs" / source / "check.json")
    # the same object in the pre-final run, from the chosen variant first, else from the variant it was swapped in from
    past_briefs = {b["card"]["name"]: b for b in sorted(load_json(ROOT / "runs" / source / "briefs.json"),
                                                        key=lambda b: b["variant"] == variant)}
    for brief in load_json(folder / "briefs.json"):
        tries = history.get(brief["id"])
        if not tries:
            continue
        chosen = best_try(tries)["try_id"]
        prefinal = None
        old = past_briefs.get(brief["card"]["name"])
        if old and past_history.get(old["id"]):
            graded = outside.get(f"card/{source}/{old['id']}|reviewer 2", {})
            prefinal = {"image": f"runs/{source}/tries/{best_try(past_history[old['id']])['try_id']}.png",
                        "grade": graded.get("grade"), "broken": bool(graded.get("broken")),
                        "comment": graded.get("comment", "")}
        yield {"id": f"final/{run}/{brief['id']}", "kind": "final", "group": group, "name": brief["card"]["name"],
               "image": f"runs/{run}/tries/{chosen}.png", "chosen": chosen,
               "candidates": [{"try": t["try_id"], "image": f"runs/{run}/tries/{t['try_id']}.png"}
                              for t in sorted(tries, key=lambda t: int(t["try_id"].rsplit("_", 1)[1]))],
               "references": [f"materials/card_examples/{i}.png" for i in brief["references"]],
               "blockout": f"runs/{run}/models/{brief['id']}.png" if (folder / "models" / f"{brief['id']}.png").exists() else None,
               "prefinal": prefinal}


def build():
    rng = random.Random(11)
    real = {c["id"]: c["name"] for c in load_json(ROOT / "analysis" / "cards.json")}
    sets = {s["title"]: s for s in load_json(ROOT / "analysis" / "sets.json")}
    cards, rows = [], []
    for genre, (run, variant) in FINAL.items():
        found = list(final_cards(run, genre, f"prefinal/{genre}", variant))
        cards += found
        rows.append({"id": f"final/set/{run}", "kind": "final", "title": load_json(ROOT / "runs" / run / "plan.json")["title"],
                     "cards": found})
    if (ROOT / "runs" / CAST / "check.json").exists():
        found = list(final_cards(CAST, "cast", "prefinal/cast", 1))
        cards += found
        rows.append({"id": f"final/set/{CAST}", "kind": "final", "title": "Cast bonus", "cards": found})

    blind = []
    twins = load_json(ROOT / "runs" / "twins40" / "briefs.json")
    for arm in TWIN_ARMS:
        drawn = [t for t in twins if all((ROOT / "runs" / "twins40" / label / "tries" / f"{t['id']}_1.png").exists()
                                         for label in ("n0", arm))]
        for twin in rng.sample(drawn, min(TWINS_PER_ARM, len(drawn))):
            images = [("n0", f"runs/twins40/n0/tries/{twin['id']}_1.png"), (arm, f"runs/twins40/{arm}/tries/{twin['id']}_1.png")]
            rng.shuffle(images)
            blind.append({"id": f"night/twin/{arm}/{twin['id']}", "kind": "night", "type": "twin", "name": twin["card"]["name"],
                          "real": f"materials/card_examples/{twin['real']}.png", "images": [p for _, p in images],
                          "arms": [a for a, _ in images]})
    night = ROOT / "runs" / "night" / "perspective"
    for brief in load_json(night / "cam" / "briefs.json"):
        genre, old = brief["source"].split("/")[-1], brief["source_id"]
        images = [("control", f"runs/prefinal/{genre}/tries/{old}_1.png"), ("cam", f"runs/night/perspective/cam/tries/{brief['id']}_1.png")]
        if (night / "model" / "tries" / f"{brief['id']}_1.png").exists():
            images.append(("model", f"runs/night/perspective/model/tries/{brief['id']}_1.png"))
        images = [(a, p) for a, p in images if (ROOT / p).exists()]
        rng.shuffle(images)
        blind.append({"id": f"night/broken/{brief['id']}", "kind": "night", "type": "broken", "name": brief["card"]["name"],
                      "references": [f"materials/card_examples/{i}.png" for i in brief["references"]],
                      "images": [p for _, p in images], "arms": [a for a, _ in images]})
    rng.shuffle(blind)
    save_json(ITEMS, {"compare": {"title": COMPARE, "cards": [{"name": real[i], "image": f"materials/card_examples/{i}.png"}
                                                               for i in sets[COMPARE]["cards"]]},
                      "sets": rows, "cards": cards, "blind": blind})
    print(f"{len(rows)} sets, {len(cards)} cards, {len(blind)} blind items")


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path).lstrip("/")
        if not path:
            return self.reply(PAGE.encode(), "text/html; charset=utf-8")
        if path == "data":
            ratings = {k: v for k, v in (load_json(RATINGS) if RATINGS.exists() else {}).items()
                       if v.get("kind") in ("final", "night")}
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
    given = {v["id"]: v for v in (load_json(RATINGS) if RATINGS.exists() else {}).values()
             if v.get("kind") in ("final", "night") and v.get("rater") == "me"}
    for row in items["sets"]:
        answer = given.get(row.get("id"), {})
        if answer.get("grade"):
            print(f"set {row['title']}: {answer['grade']} ({SET_GRADES[answer['grade']]})")
    groups = defaultdict(list)
    for card in items["cards"]:
        answer = given.get(card["id"], {})
        if answer.get("grade"):
            groups[card["group"]].append((card, answer))
    for group, rows in groups.items():
        before = [c["prefinal"]["grade"] for c, _ in rows if c.get("prefinal") and c["prefinal"]["grade"]]
        print(f"{group}: mean grade {mean(a['grade'] for _, a in rows):.2f} from {len(rows)}, broken "
              f"{sum(bool(a.get('broken')) for _, a in rows)}" + (f"; outside rater on pre-final: {mean(before):.2f} "
                                                                    f"from {len(before)}" if before else ""))
    picks = [(c, given[c["id"]]["pick"]) for c in items["cards"] if given.get(c["id"], {}).get("pick")]
    for card, pick in picks:
        print(f"  pick {card['id']}: {pick} instead of {card['chosen']}")
    closer, works = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
    for item in items["blind"]:
        answer = given.get(item["id"])
        if not answer:
            continue
        if item["type"] == "twin":
            arm = next(a for a in item["arms"] if a != "n0")
            choice = answer.get("closer")
            closer[arm][item["arms"][int(choice)] if choice not in (None, "same") else "same"] += 1
        for index, verdict in (answer.get("works") or {}).items():
            works[f"{item['type']}/{item['arms'][int(index)]}"][verdict] += 1
    for arm, counts in closer.items():
        print(f"twins, {TWIN_ARMS[arm]}: closer {dict(counts)}")
    for arm, counts in sorted(works.items()):
        print(f"{arm}: works {counts['yes']}, slightly off {counts['slight']}, broken {counts['no']}")
    for entry in given.values():
        if entry.get("comment"):
            print(f"- {entry['id']}: {entry['comment']}")


SET_GRADES = ["", "Clearly no", "Rather no", "Maybe", "Yes, with small issues", "Yes"]

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Final review</title>
<style>
:root { --bg: #18181b; --panel: #26262b; --button: #3a3a42; --text: #ececf1; --muted: #a0a0ab; --accent: #f5b83d; }
body { margin: 0; background: var(--bg); color: var(--text); font: 15px/1.45 system-ui, sans-serif; }
header { display: flex; gap: 8px; align-items: center; padding: 10px 20px; background: var(--panel); flex-wrap: wrap; }
button { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 7px 13px; font: inherit; cursor: pointer; }
button.on { background: var(--accent); color: #000; }
textarea { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 8px; font: inherit;
  display: block; width: 100%; max-width: 900px; height: 50px; margin: 0 auto; box-sizing: border-box; }
main { max-width: 1320px; margin: 0 auto; padding: 14px 20px 40px; }
.hint, figcaption, #progress { color: var(--muted); }
.hint { text-align: center; max-width: 900px; margin: 6px auto 14px; }
.cards { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; align-items: flex-start; }
figure { margin: 0; text-align: center; }
img { display: block; max-width: 100%; border-radius: 10px; }
.grade img { width: min(300px, 23vw); }
.grade figure:first-child img { outline: 3px solid var(--accent); }
.strip { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin: 10px 0; }
.strip img { width: 96px; border-radius: 6px; cursor: pointer; opacity: .75; }
.strip img.on { outline: 3px solid var(--accent); opacity: 1; }
.past { display: flex; gap: 10px; align-items: center; justify-content: center; color: var(--muted); margin: 6px 0; }
.past img { width: 64px; border-radius: 4px; }
.set { display: grid; grid-template-columns: 110px repeat(10, 1fr); gap: 6px; align-items: center; margin: 8px 0; }
.set figure img { width: 100%; border-radius: 6px; }
.set figcaption { font-size: 11px; line-height: 1.2; }
.set .label { font-weight: 600; }
.blind img { width: min(330px, 30vw); }
.blind figure.real img { outline: 3px solid var(--muted); }
.refs img { width: 150px; }
.row { display: flex; gap: 8px; justify-content: center; margin: 10px 0; flex-wrap: wrap; }
.marks { display: flex; gap: 4px; justify-content: center; margin-top: 6px; }
</style></head><body>
<header><b>Final review</b><span id="tabs"></span><span id="progress" style="margin-left:auto"></span></header>
<main id="main"></main>
<script>
const TABS = [["sets", "Sets"], ["cards", "Cards"], ["blind", "Blind arms"]];
const GRADES = ["", "Clearly off", "Noticeably off", "Close", "Very close", "Indistinguishable"];
const SET_GRADES = ["", "Clearly no", "Rather no", "Maybe", "Yes, with small issues", "Yes"];
const WORKS = [["yes", "Works"], ["slight", "Slightly off"], ["no", "Broken"]];
const rater = "me";
let items, ratings = {}, tab = "sets";
const position = { cards: 0, blind: 0 };
const answer = id => ratings[id + "|" + rater];
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const done = list => list.filter(i => answer(i.id)).length;

function save(item, fields) {
  const entry = { ...answer(item.id), ...fields, id: item.id, kind: item.kind, rater, time: new Date().toISOString() };
  ratings[item.id + "|" + rater] = entry;
  fetch("/rate", { method: "POST", body: JSON.stringify(entry) });
}

const setRow = (label, cards) => `<div class="set"><div class="label">${esc(label)}</div>${cards.map(c =>
  `<figure><img src="/${(answer(c.id) || {}).pick ? c.candidates.find(x => x.try === answer(c.id).pick).image : c.image}"><figcaption>${esc(c.name)}</figcaption></figure>`).join("")}</div>`;

const views = {
  sets() {
    const votes = s => { const entry = answer(s.id) || {};
      return `<div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-set="${esc(s.id)}" data-setgrade="${g}" class="${entry.grade === g ? "on" : ""}">${g} · ${SET_GRADES[g]}</button>`).join("")}</div>
        <textarea data-setcomment="${esc(s.id)}" placeholder="What stands out of the set? Optional">${esc(entry.comment || "")}</textarea>`; };
    return `<p class="hint">The three final sets and the bonus cast cards, with a real set on top. Could each set stand in the game beside the real ones, by idea and by look? A candidate picked on the Cards tab replaces the card here.</p>
      ${setRow("Real: " + items.compare.title, items.compare.cards)}${items.sets.map(s => setRow(s.title, s.cards) + votes(s)).join("")}`;
  },
  cards() {
    const item = items.cards[position.cards], entry = answer(item.id) || {}, past = item.prefinal;
    const shown = entry.pick ? item.candidates.find(c => c.try === entry.pick).image : item.image;
    return `<p class="hint">${esc(item.group)} · <b>${esc(item.name)}</b> · ${position.cards + 1} of ${items.cards.length}. Framed: our card; beside it, its three reference cards. Below: every candidate drawn for it (the chosen one is lit); click one to pick it instead. Keys 1-5 grade and move on, X marks broken, arrows move.</p>
      <div class="cards grade"><figure><img src="/${shown}"><figcaption>ours${entry.pick ? " (your pick)" : ""}</figcaption></figure>
      ${item.references.map(src => `<figure><img src="/${src}"><figcaption>real</figcaption></figure>`).join("")}</div>
      <div class="strip">${item.candidates.map(c => `<img data-try="${c.try}" src="/${c.image}" class="${c.try === (entry.pick || item.chosen) ? "on" : ""}" title="${c.try}">`).join("")}
      ${item.blockout ? `<img src="/${item.blockout}" title="blockout" style="cursor:default;opacity:1;border:1px dashed #888">` : ""}</div>
      ${past ? `<div class="past"><img src="/${past.image}"><span>Pre-final drawing, outside rater: ${past.grade ? past.grade + "/5" : "not graded"}${past.broken ? ", broken" : ""}${past.comment ? " · " + esc(past.comment) : ""}</span></div>` : ""}
      <div class="row"><button id="broken" class="${entry.broken ? "on" : ""}">X · Broken</button></div>
      <textarea id="comment" placeholder="Comment, optional">${esc(entry.comment || "")}</textarea>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry.grade === g ? "on" : ""}">${g} · ${GRADES[g]}</button>`).join("")}</div>
      <div class="row"><button id="back">← Back</button><button id="next">Next →</button></div>`;
  },
  blind() {
    const item = items.blind[position.blind], entry = answer(item.id) || {}, works = entry.works || {};
    const marks = i => `<div class="marks">${WORKS.map(([v, label]) => `<button data-works="${i}" data-value="${v}" class="${works[i] === v ? "on" : ""}">${label}</button>`).join("")}</div>`;
    const head = item.type === "twin"
      ? `<p class="hint"><b>${esc(item.name)}</b> · ${position.blind + 1} of ${items.blind.length}. Left: the real card. A and B redraw it from text, in random order. Which is closer to the real card? Mark any that is broken.</p>
         <div class="cards blind"><figure class="real"><img src="/${item.real}"><figcaption>real</figcaption></figure>
         ${item.images.map((src, i) => `<figure><img src="/${src}"><figcaption>${"AB"[i]}</figcaption>${marks(i)}</figure>`).join("")}</div>
         <div class="row">${["0", "1", "same"].map(v => `<button data-closer="${v}" class="${entry.closer === v ? "on" : ""}">${v === "same" ? "Same" : "AB"[v] + " closer"}</button>`).join("")}</div>`
      : `<p class="hint"><b>${esc(item.name)}</b> · ${position.blind + 1} of ${items.blind.length}. A card graded broken in the pre-final set, drawn again in different ways, in random order. Does each work as built: perspective, parts, what it stands on?</p>
         <div class="cards refs">${item.references.map(src => `<figure><img src="/${src}"><figcaption>reference</figcaption></figure>`).join("")}</div>
         <div class="cards blind">${item.images.map((src, i) => `<figure><img src="/${src}"><figcaption>${"ABC"[i]}</figcaption>${marks(i)}</figure>`).join("")}</div>`;
    return head + `<textarea id="comment" placeholder="Comment, optional">${esc(entry.comment || "")}</textarea>
      <div class="row"><button id="back">← Back</button><button id="next">Next →</button></div>`;
  },
};

function show() {
  document.getElementById("tabs").innerHTML = TABS.map(([id, label]) => `<button data-tab="${id}" class="${tab === id ? "on" : ""}">${label}</button>`).join(" ");
  document.querySelectorAll("[data-tab]").forEach(b => b.onclick = () => { tab = b.dataset.tab; show(); });
  document.getElementById("progress").textContent = `Sets ${done(items.sets)}/${items.sets.length} · Cards ${done(items.cards)}/${items.cards.length} · Blind ${done(items.blind)}/${items.blind.length}`;
  document.getElementById("main").innerHTML = views[tab]();
  const on = (id, f) => { const el = document.getElementById(id); if (el) el.onclick = f; };
  const comment = () => (document.getElementById("comment") || {}).value || "";
  if (tab === "cards") {
    const item = items.cards[position.cards];
    document.querySelectorAll("[data-grade]").forEach(b => b.onclick = () => grade(Number(b.dataset.grade)));
    document.querySelectorAll("[data-try]").forEach(b => b.onclick = () => { save(item, { pick: b.dataset.try === item.chosen ? null : b.dataset.try, comment: comment() }); show(); });
    on("broken", () => { save(item, { broken: !(answer(item.id) || {}).broken, comment: comment() }); show(); });
  }
  if (tab === "sets") {
    const byId = id => items.sets.find(s => s.id === id);
    document.querySelectorAll("[data-setgrade]").forEach(b => b.onclick = () => { save(byId(b.dataset.set), { grade: Number(b.dataset.setgrade) }); show(); });
    document.querySelectorAll("[data-setcomment]").forEach(t => t.onchange = () => save(byId(t.dataset.setcomment), { comment: t.value }));
  }
  if (tab === "blind") {
    const item = items.blind[position.blind];
    document.querySelectorAll("[data-closer]").forEach(b => b.onclick = () => { save(item, { closer: b.dataset.closer, comment: comment() }); show(); });
    document.querySelectorAll("[data-works]").forEach(b => b.onclick = () => {
      save(item, { works: { ...(answer(item.id) || {}).works, [b.dataset.works]: b.dataset.value }, comment: comment() }); show();
    });
  }
  const box = document.getElementById("comment");
  if (box) box.onchange = () => save(items[tab][position[tab]], { comment: comment() });
  on("back", () => move(-1));
  on("next", () => move(1));
}

function move(by) {
  const list = items[tab];
  position[tab] = Math.min(list.length - 1, Math.max(0, position[tab] + by));
  show(); window.scrollTo(0, 0);
}

function grade(g) {
  save(items.cards[position.cards], { grade: g, comment: (document.getElementById("comment") || {}).value || "" });
  move(1);
}

document.onkeydown = event => {
  if (["TEXTAREA", "INPUT"].includes(event.target.tagName) || !items) return;
  const press = event.key.toLowerCase();
  if (tab === "cards" && "12345".includes(press) && press) grade(Number(press));
  else if (tab === "cards" && press === "x") document.getElementById("broken").click();
  else if (event.key === "ArrowRight") move(1);
  else if (event.key === "ArrowLeft") move(-1);
};

fetch("/data").then(r => r.json()).then(data => {
  items = data.items; ratings = data.ratings;
  position.cards = Math.max(0, items.cards.findIndex(i => !answer(i.id)));
  position.blind = Math.max(0, items.blind.findIndex(i => !answer(i.id)));
  show();
});
</script></body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("build", "serve", "summary"))
    parser.add_argument("--port", type=int, default=8767)
    args = parser.parse_args()
    if args.action == "build":
        build()
    elif args.action == "summary":
        summary()
    else:
        if not ITEMS.exists():
            raise SystemExit("run build first, once the final runs are done")
        print(f"open http://127.0.0.1:{args.port}", flush=True)
        try:
            ThreadingHTTPServer(("127.0.0.1", args.port), Page).serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
