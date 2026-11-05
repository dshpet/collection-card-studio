"""A local page for human ratings. Answers go straight to runs/ratings.json.

Twins: a real card and its redraw, sides shuffled. Pick the generated one. Old-style redraws are mixed in as a control.
Closest: a real card and its redraws in every style drawn so far, shuffled. Pick the closest.
Cards: every set card beside its three reference cards, all at the same size, graded 1-5.
Trial: each drawing of experiments/trial.py beside its real card, arm hidden: does it work as built, and a grade 1-5.
Redraw: each final card, as chosen before and as redrawn from a blockout, mixed and unlabelled, beside its
reference cards: does it work as built, and a grade 1-5.
Soft: the cards of experiments/trial2.py, each arm and the old card mixed and unlabelled, rated as in Redraw.
Param: a real card with its final-style twin and the twins redrawn by experiments/param.py rounds, shuffled. Pick the
closest, or same when none is.
Cast: each card of experiments/cast_trial.py, arms mixed and unlabelled, beside real cards with the same characters:
does the scene work, and a grade 1-5.

    rate_ui.py              then open http://127.0.0.1:8765
    rate_ui.py --summary    what the ratings say so far
    rate_ui.py --sets western-final sci-fi-final horror-final    rate the cards of other runs
"""

import argparse
import json
import random
import threading
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from statistics import mean
from urllib.parse import unquote

from common import ROOT, best_try, load_json, save_json


RATINGS = ROOT / "runs" / "ratings.json"
SETS = ("western", "sci-fi", "horror")
SERVED = ("materials/card_examples/", "runs/")
CLOSEST_STYLES = ("final", "old", "r3", "r9")
PARAM = ("p1", "p2")  # experiments/param.py rounds under test
LOCK = threading.Lock()


def items(sets=SETS):
    rng = random.Random(3)
    twins = []
    for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
        for style in ("final", "old"):
            real = f"materials/card_examples/{brief['real']}.png"
            drawn = f"runs/twins40/{style}/tries/{brief['id']}_1.png"
            first = rng.random() < 0.5
            twins.append({"id": f"twin/{style}/{brief['id']}", "kind": "twin", "name": brief["card"]["name"],
                          "images": [drawn, real] if first else [real, drawn], "generated": "A" if first else "B"})
    rng.shuffle(twins)
    closest = []
    for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json"):
        drawn = [(style, f"runs/twins40/{style}/tries/{brief['id']}_1.png") for style in sorted(CLOSEST_STYLES)
                 if (ROOT / "runs" / "twins40" / style / "tries" / f"{brief['id']}_1.png").exists()]
        rng.shuffle(drawn)
        closest.append({"id": f"closest/{brief['id']}", "kind": "closest", "name": brief["card"]["name"],
                        "images": [f"materials/card_examples/{brief['real']}.png"] + [path for _, path in drawn],
                        "styles": [style for style, _ in drawn]})
    final = load_json(ROOT / "runs" / "final.json")
    cards = []
    for run in sets:
        history = load_json(ROOT / "runs" / run / "check.json")
        for brief in load_json(ROOT / "runs" / run / "briefs.json"):
            if not history.get(brief["id"]):  # every draw of this card failed
                continue
            best = best_try(history[brief["id"]])
            cards.append({"id": f"card/{run}/{brief['id']}", "kind": "card", "name": brief["card"]["name"],
                          "set": f"{run} v{brief['variant']}", "final": brief["id"] in final.get(run, []),
                          "images": [f"runs/{run}/tries/{best['try_id']}.png"]
                          + [f"materials/card_examples/{i}.png" for i in brief["references"]]})
    cards.sort(key=lambda card: not card["final"])
    trial = []
    real = {brief["id"]: brief for brief in load_json(ROOT / "runs" / "twins40" / "briefs.json")}
    for path in sorted((ROOT / "runs" / "trial").glob("*/tries/*.png")):
        brief = real[path.stem.split("_")[0]]
        trial.append({"id": f"trial/{path.parent.parent.name}/{path.stem}", "kind": "trial", "name": brief["card"]["name"],
                      "images": [f"materials/card_examples/{brief['real']}.png", str(path.relative_to(ROOT))]})
    rng.shuffle(trial)
    redraw = []
    for run in final:
        new_run = ROOT / "runs" / f"{run}-blockout"
        if not (new_run / "check.json").exists():
            continue
        old_briefs = {brief["id"]: brief for brief in load_json(ROOT / "runs" / run / "briefs.json")}
        old_history, new_history = load_json(ROOT / "runs" / run / "check.json"), load_json(new_run / "check.json")
        for brief in load_json(new_run / "briefs.json"):
            if not new_history.get(brief["id"]):
                continue
            old_id = brief["source"].split("/")[1]
            for arm, folder, try_id in (("old", run, best_try(old_history[old_id])["try_id"]),
                                        ("new", new_run.name, best_try(new_history[brief["id"]])["try_id"])):
                redraw.append({"id": f"redraw/{arm}/{run}/{old_id}", "kind": "redraw", "name": brief["card"]["name"],
                               "images": [f"runs/{folder}/tries/{try_id}.png"]
                               + [f"materials/card_examples/{i}.png" for i in old_briefs[old_id]["references"]]})
    rng.shuffle(redraw)
    soft = []
    for path in sorted((ROOT / "runs" / "trial2").glob("*/*/tries/*_1.png")):
        arm, run, card_id = path.parts[-4], path.parts[-3], path.stem[:-2]
        brief = next(b for b in load_json(ROOT / "runs" / run / "briefs.json") if b["id"] == card_id)
        references = [f"materials/card_examples/{i}.png" for i in brief["references"]]
        old = f"runs/{run}/tries/{best_try(load_json(ROOT / 'runs' / run / 'check.json')[card_id])['try_id']}.png"
        for name, image in ((arm, str(path.relative_to(ROOT))), ("old", old)):
            if not any(item["id"] == f"soft/{name}/{run}/{card_id}" for item in soft):
                soft.append({"id": f"soft/{name}/{run}/{card_id}", "kind": "soft", "name": brief["card"]["name"],
                             "images": [image] + references})
    rng.shuffle(soft)
    param = []
    for index, brief in enumerate(load_json(ROOT / "runs" / "twins40" / "briefs.json")):
        drawn = [(style, f"runs/twins40/{style}/tries/{brief['id']}_1.png") for style in ("final", *PARAM)]
        if all((ROOT / path).exists() for _, path in drawn):
            # Rotated, not shuffled, so every style sits in every position equally often
            shift = index % len(drawn)
            drawn = drawn[shift:] + drawn[:shift]
            if (index // len(drawn)) % 2:
                drawn.reverse()
            param.append({"id": f"param/{'+'.join(PARAM)}/{brief['id']}", "kind": "param", "name": brief["card"]["name"],
                          "images": [f"materials/card_examples/{brief['real']}.png"] + [path for _, path in drawn],
                          "styles": [style for style, _ in drawn]})
    rng.shuffle(param)
    cast = []
    trial_cards = ROOT / "runs" / "cast_trial" / "cards.json"
    if trial_cards.exists():
        figures = load_json(ROOT / "analysis" / "cast.json")
        for card in load_json(trial_cards):
            shown = sorted({f["card"] for f in figures if f["character"] in card["cast"]
                            and f.get("labels", {}).get("is_character")})[:3]
            for path in sorted((ROOT / "runs" / "cast_trial" / "tries").glob(f"{card['id']}_*.png")):
                cast.append({"id": f"cast/{path.stem.split('_')[-2]}/{path.stem}", "kind": "cast",
                             "name": card["subject"], "images": [str(path.relative_to(ROOT))]
                             + [f"materials/card_examples/{i}.png" for i in shown]})
    rng.shuffle(cast)
    return twins + closest + cards + trial + redraw + soft + param + cast


def ratings():
    return load_json(RATINGS) if RATINGS.exists() else {}


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(self.path).lstrip("/")
        if not path:
            return self.reply(PAGE.encode(), "text/html; charset=utf-8")
        if path == "data":
            return self.reply(json.dumps({"items": ITEMS, "ratings": ratings()}).encode(), "application/json")
        file = (ROOT / path).resolve()
        if path.startswith(SERVED) and file.is_relative_to(ROOT) and file.suffix == ".png" and file.exists():
            return self.reply(file.read_bytes(), "image/png")
        self.send_error(404)

    def do_POST(self):
        entry = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with LOCK:
            data = ratings()
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
    data = ratings().values()
    picks, grades, closest = defaultdict(list), defaultdict(list), defaultdict(int)
    works, trial = defaultdict(lambda: defaultdict(int)), defaultdict(list)
    for entry in data:
        if entry["kind"] == "twin" and entry["answer"] != "neither":
            picks[entry["id"].split("/")[1]].append(entry["correct"])
        elif entry["kind"] == "card":
            grades[entry["set"]].append(entry["grade"])
        elif entry["kind"] in ("closest", "param"):
            closest[f"{entry['kind']}: {entry['style']}"] += 1
        elif entry["kind"] in ("trial", "redraw", "soft", "cast"):
            arm = entry["kind"] + "/" + entry["id"].split("/")[1]
            if entry.get("works"):
                works[arm][entry["works"]] += 1
            if entry.get("grade"):
                trial[arm].append(entry["grade"])
    for arm in sorted(set(works) | set(trial)):
        counts = ", ".join(f"{works[arm][w]} {w}" for w in ("yes", "slight", "no"))
        grade = f", mean grade {mean(trial[arm]):.1f} from {len(trial[arm])}" if trial[arm] else ""
        print(f"{arm}: works {counts}{grade}")
    for style, count in sorted(closest.items(), key=lambda item: -item[1]):
        print(f"{style} chosen {count} times")
    for style, hits in sorted(picks.items()):
        print(f"twins, {style} style: found the generated card {sum(hits)} of {len(hits)} (chance is half)")
    for group, values in sorted(grades.items()):
        print(f"cards, {group}: mean grade {mean(values):.1f} from {len(values)}")
    for entry in data:
        if entry.get("comment"):
            print(f"- {entry['id']} ({entry['rater']}): {entry['comment']}")


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Card ratings</title>
<style>
:root { --bg: #18181b; --panel: #26262b; --button: #3a3a42; --text: #ececf1; --muted: #9a9aa5; --accent: #f5b83d; }
body { margin: 0; background: var(--bg); color: var(--text); font: 15px system-ui, sans-serif; }
header { display: flex; gap: 12px; align-items: center; padding: 12px 20px; background: var(--panel); flex-wrap: wrap; }
button { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }
button.on { background: var(--accent); color: #000; }
input, textarea { background: var(--button); color: var(--text); border: 0; border-radius: 6px; padding: 8px; font: inherit; }
main { max-width: 1200px; margin: 0 auto; padding: 16px; }
.hint, figcaption, #progress { color: var(--muted); }
.cards { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
figure { margin: 0; text-align: center; }
img { display: block; max-width: 100%; border-radius: 10px; }
.big img { width: 430px; }
.same img { width: 270px; }
.same figure:first-child img, .trial figure:first-child img { outline: 3px solid var(--accent); }
.row { display: flex; gap: 8px; justify-content: center; margin: 14px 0; flex-wrap: wrap; }
textarea { display: block; width: 100%; max-width: 876px; height: 56px; margin: 0 auto; box-sizing: border-box; }
#result { text-align: center; min-height: 22px; font-weight: 600; }
</style></head><body>
<header><b>Card ratings</b><button id="tab-twin">Twins</button><button id="tab-closest">Closest</button><button id="tab-card">Cards</button><button id="tab-trial">Trial</button><button id="tab-redraw">Redraw</button><button id="tab-soft">Soft</button><button id="tab-param">Param</button><button id="tab-cast">Cast</button>
<span id="progress"></span><label style="margin-left:auto">Rater <input id="rater" size="10"></label></header>
<main id="main"></main>
<script>
let items = [], ratings = {}, mode = "twin";
const position = { twin: 0, closest: 0, card: 0, trial: 0, redraw: 0, soft: 0, param: 0, cast: 0 };
const kinds = ["twin", "closest", "card", "trial", "redraw", "soft", "param", "cast"];
const works = [["yes", "Y · Works"], ["slight", "S · Slightly off"], ["no", "X · Broken"]];
const rater = document.getElementById("rater");
try { rater.value = localStorage.getItem("rater") || "me"; } catch (e) { rater.value = "me"; }
rater.onchange = () => { try { localStorage.setItem("rater", rater.value); } catch (e) {} show(); };
const list = kind => items.filter(item => item.kind === kind);
const key = item => item.id + "|" + rater.value;
const current = () => list(mode)[position[mode]];
const grades = ["", "Clearly off", "Noticeably off", "Close", "Very close", "Can't tell"];

function save(fields) {
  const item = current();
  if (!item) return;
  const entry = { ...ratings[key(item)], ...fields, id: item.id, kind: item.kind, rater: rater.value,
                  set: item.set, comment: document.getElementById("comment").value, time: new Date().toISOString() };
  ratings[key(item)] = entry;
  fetch("/rate", { method: "POST", body: JSON.stringify(entry) });
  show();
}

function move(step) {
  position[mode] = Math.min(Math.max(position[mode] + step, 0), list(mode).length - 1);
  show();
}

function show() {
  const item = current(), entry = item && ratings[key(item)];
  for (const kind of kinds) document.getElementById("tab-" + kind).className = kind === mode ? "on" : "";
  if (!item) {
    document.getElementById("progress").textContent = "";
    document.getElementById("main").innerHTML = "<p class=\"hint\">Nothing to rate here.</p>";
    return;
  }
  const counts = kind => list(kind).filter(i => ratings[key(i)]).length + "/" + list(kind).length;
  document.getElementById("progress").textContent = "Twins " + counts("twin") + " · Closest " + counts("closest") + " · Cards " + counts("card") + " · Trial " + counts("trial") + " · Redraw " + counts("redraw") + " · Soft " + counts("soft") + " · Param " + counts("param") + " · Cast " + counts("cast");
  let html;
  if (mode === "twin") {
    html = `<p class="hint">One card is real, one was generated from a text brief. Which one is generated? Keys: A, B, N for can't tell, arrows to move.</p>
      <div class="cards">${item.images.map((src, i) => `<figure class="big"><img src="/${src}"><figcaption>${"AB"[i]}</figcaption></figure>`).join("")}</div>
      <div class="row">${["A", "B", "neither"].map(a => `<button data-answer="${a}" class="${entry && entry.answer === a ? "on" : ""}">${a === "neither" ? "Can't tell" : a + " is generated"}</button>`).join("")}</div>`;
  } else if (mode === "closest" || mode === "param") {
    const [real, ...drawn] = item.images;
    const same = mode === "param" ? `<button data-same="1" class="${entry && entry.style === "same" ? "on" : ""}">Same</button>` : "";
    html = `<p class="hint">The outlined card is real. Which redraw is closest to it in look? Keys: 1 to ${drawn.length}${mode === "param" ? ", N for same" : ""}, arrows to move.</p>
      <div class="cards same"><figure><img src="/${real}"><figcaption>real · ${item.name}</figcaption></figure>
      ${drawn.map((src, i) => `<figure><img src="/${src}"><figcaption>${i + 1}</figcaption></figure>`).join("")}</div>
      <div class="row">${drawn.map((_, i) => `<button data-pick="${i}" class="${entry && entry.style === item.styles[i] ? "on" : ""}">${i + 1} is closest</button>`).join("")}${same}</div>`;
  } else if (mode === "trial") {
    html = `<p class="hint">The outlined card is real. Does the generated object work as built, and could the card sit beside the real one? Keys: Y, S, X and 1 to 5, arrows to move.</p>
      <div class="cards trial">${item.images.map((src, i) => `<figure class="big"><img src="/${src}"><figcaption>${i ? "generated" : "real · " + item.name}</figcaption></figure>`).join("")}</div>
      <div class="row">${works.map(([w, label]) => `<button data-works="${w}" class="${entry && entry.works === w ? "on" : ""}">${label}</button>`).join("")}</div>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry && entry.grade === g ? "on" : ""}">${g} · ${grades[g]}</button>`).join("")}</div>`;
  } else if (mode === "redraw" || mode === "soft" || mode === "cast") {
    const [card, ...references] = item.images;
    html = `<p class="hint">Does the outlined object work as built, and could the card sit next to the real ones beside it? Keys: Y, S, X and 1 to 5, arrows to move.</p>
      <div class="cards same"><figure><img src="/${card}"><figcaption>${item.name}</figcaption></figure>
      ${references.map(src => `<figure><img src="/${src}"><figcaption>real</figcaption></figure>`).join("")}</div>
      <div class="row">${works.map(([w, label]) => `<button data-works="${w}" class="${entry && entry.works === w ? "on" : ""}">${label}</button>`).join("")}</div>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry && entry.grade === g ? "on" : ""}">${g} · ${grades[g]}</button>`).join("")}</div>`;
  } else {
    const [card, ...references] = item.images;
    html = `<p class="hint">Could the outlined card sit next to the real ones beside it? Keys: 1 to 5, arrows to move.</p>
      <div class="cards same"><figure><img src="/${card}"><figcaption>${item.name} · ${item.set}${item.final ? " · final set" : ""}</figcaption></figure>
      ${references.map(src => `<figure><img src="/${src}"><figcaption>real</figcaption></figure>`).join("")}</div>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry && entry.grade === g ? "on" : ""}">${g} · ${grades[g]}</button>`).join("")}</div>`;
  }
  const result = mode === "twin" && entry ? (entry.answer === "neither" ? "Skipped" : (entry.correct ? "Right" : "Wrong")) +
    ` · ${item.generated} was generated · ${item.name}` : "";
  document.getElementById("main").innerHTML = html + `<textarea id="comment" placeholder="Comment, optional: what looks off?">${entry && entry.comment ? entry.comment : ""}</textarea>
    <div id="result">${result}</div><div class="row"><button id="back">← Back</button><button id="next">Next →</button></div>`;
  document.querySelectorAll("[data-answer]").forEach(b => b.onclick = () => save({ answer: b.dataset.answer, correct: b.dataset.answer === item.generated }));
  document.querySelectorAll("[data-grade]").forEach(b => b.onclick = () => save({ grade: Number(b.dataset.grade) }));
  document.querySelectorAll("[data-pick]").forEach(b => b.onclick = () => save({ style: item.styles[Number(b.dataset.pick)] }));
  document.querySelectorAll("[data-same]").forEach(b => b.onclick = () => save({ style: "same" }));
  document.querySelectorAll("[data-works]").forEach(b => b.onclick = () => save({ works: b.dataset.works }));
  document.getElementById("comment").onchange = () => { if (ratings[key(item)]) save({}); };
  document.getElementById("back").onclick = () => move(-1);
  document.getElementById("next").onclick = () => move(1);
}

document.onkeydown = event => {
  if (["TEXTAREA", "INPUT"].includes(event.target.tagName)) return;
  const press = event.key.toLowerCase(), item = current();
  if (!item) return;
  if (event.key === "ArrowRight") move(1);
  else if (event.key === "ArrowLeft") move(-1);
  else if (mode === "twin" && "abn".includes(press) && press) {
    const answer = press === "n" ? "neither" : press.toUpperCase();
    save({ answer, correct: answer === item.generated });
  } else if (["card", "trial", "redraw", "soft", "cast"].includes(mode) && "12345".includes(press) && press) save({ grade: Number(press) });
  else if (["trial", "redraw", "soft", "cast"].includes(mode) && "ysx".includes(press) && press) save({ works: { y: "yes", s: "slight", x: "no" }[press] });
  else if (mode === "param" && press === "n") save({ style: "same" });
  else if ((mode === "closest" || mode === "param") && Number(press) >= 1 && Number(press) <= item.styles.length) save({ style: item.styles[Number(press) - 1] });
};
for (const kind of kinds) document.getElementById("tab-" + kind).onclick = () => { mode = kind; show(); };
fetch("/data").then(r => r.json()).then(data => {
  items = data.items; ratings = data.ratings;
  for (const kind of kinds) position[kind] = Math.max(0, list(kind).findIndex(i => !ratings[key(i)]));
  mode = list("param").some(i => !ratings[key(i)]) ? "param" : list("soft").some(i => !ratings[key(i)]) ? "soft" : list("redraw").length ? "redraw" : mode;
  show();
});
</script></body></html>"""


def main():
    global ITEMS
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--sets", nargs="+", default=list(SETS), help="runs whose cards the Cards tab shows")
    args = parser.parse_args()
    if args.summary:
        summary()
        return
    ITEMS = items(args.sets)
    print(f"open http://127.0.0.1:{args.port}", flush=True)
    try:
        ThreadingHTTPServer(("127.0.0.1", args.port), Page).serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
