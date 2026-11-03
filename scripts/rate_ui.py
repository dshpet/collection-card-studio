"""A local page for human ratings. Answers go straight to runs/ratings.json.

Twins: a real card and its redraw, sides shuffled. Pick the generated one. Old-style redraws are mixed in as a control.
Cards: every set card beside its three reference cards, graded 1-5.

    rate_ui.py              then open http://127.0.0.1:8765
    rate_ui.py --summary    what the ratings say so far
"""

import argparse
import json
import random
import threading
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from statistics import mean
from urllib.parse import unquote

from common import ROOT, load_json, save_json

from make_set import best_try

RATINGS = ROOT / "runs" / "ratings.json"
SETS = ("western", "sci-fi", "horror")
SERVED = ("materials/card_examples/", "runs/")
LOCK = threading.Lock()


def items():
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
    final = load_json(ROOT / "runs" / "final.json")
    cards = []
    for run in SETS:
        history = load_json(ROOT / "runs" / run / "check.json")
        for brief in load_json(ROOT / "runs" / run / "briefs.json"):
            best = best_try(history[brief["id"]])
            cards.append({"id": f"card/{run}/{brief['id']}", "kind": "card", "name": brief["card"]["name"],
                          "set": f"{run} v{brief['variant']}", "final": brief["id"] in final[run],
                          "images": [f"runs/{run}/tries/{best['try_id']}.png"]
                          + [f"materials/card_examples/{i}.png" for i in brief["references"]]})
    cards.sort(key=lambda card: not card["final"])
    return twins + cards


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
    picks, grades = defaultdict(list), defaultdict(list)
    for entry in data:
        if entry["kind"] == "twin" and entry["answer"] != "neither":
            picks[entry["id"].split("/")[1]].append(entry["correct"])
        elif entry["kind"] == "card":
            grades[entry["set"]].append(entry["grade"])
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
.refs { display: flex; flex-direction: column; gap: 8px; }
.refs img { width: 140px; }
.row { display: flex; gap: 8px; justify-content: center; margin: 14px 0; flex-wrap: wrap; }
textarea { display: block; width: 100%; max-width: 876px; height: 56px; margin: 0 auto; box-sizing: border-box; }
#result { text-align: center; min-height: 22px; font-weight: 600; }
</style></head><body>
<header><b>Card ratings</b><button id="tab-twin">Twins</button><button id="tab-card">Cards</button>
<span id="progress"></span><label style="margin-left:auto">Rater <input id="rater" size="10"></label></header>
<main id="main"></main>
<script>
let items = [], ratings = {}, mode = "twin";
const position = { twin: 0, card: 0 };
const rater = document.getElementById("rater");
try { rater.value = localStorage.getItem("rater") || "me"; } catch (e) { rater.value = "me"; }
rater.onchange = () => { try { localStorage.setItem("rater", rater.value); } catch (e) {} show(); };
const list = kind => items.filter(item => item.kind === kind);
const key = item => item.id + "|" + rater.value;
const current = () => list(mode)[position[mode]];
const grades = ["", "Clearly off", "Noticeably off", "Close", "Very close", "Can't tell"];

function save(fields) {
  const item = current();
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
  const item = current(), entry = ratings[key(item)];
  for (const kind of ["twin", "card"]) document.getElementById("tab-" + kind).className = kind === mode ? "on" : "";
  const counts = kind => list(kind).filter(i => ratings[key(i)]).length + "/" + list(kind).length;
  document.getElementById("progress").textContent = "Twins " + counts("twin") + " · Cards " + counts("card");
  let html;
  if (mode === "twin") {
    html = `<p class="hint">One card is real, one was generated from a text brief. Which one is generated? Keys: A, B, N for can't tell, arrows to move.</p>
      <div class="cards">${item.images.map((src, i) => `<figure class="big"><img src="/${src}"><figcaption>${"AB"[i]}</figcaption></figure>`).join("")}</div>
      <div class="row">${["A", "B", "neither"].map(a => `<button data-answer="${a}" class="${entry && entry.answer === a ? "on" : ""}">${a === "neither" ? "Can't tell" : a + " is generated"}</button>`).join("")}</div>`;
  } else {
    const [card, ...references] = item.images;
    html = `<p class="hint">Could this card sit next to the real ones on the right? Keys: 1 to 5, arrows to move.</p>
      <div class="cards"><figure class="big"><img src="/${card}"><figcaption>${item.name} · ${item.set}${item.final ? " · final set" : ""}</figcaption></figure>
      <div class="refs">${references.map(src => `<figure><img src="/${src}"><figcaption>real</figcaption></figure>`).join("")}</div></div>
      <div class="row">${[1, 2, 3, 4, 5].map(g => `<button data-grade="${g}" class="${entry && entry.grade === g ? "on" : ""}">${g} · ${grades[g]}</button>`).join("")}</div>`;
  }
  const result = mode === "twin" && entry ? (entry.answer === "neither" ? "Skipped" : (entry.correct ? "Right" : "Wrong")) +
    ` · ${item.generated} was generated · ${item.name}` : "";
  document.getElementById("main").innerHTML = html + `<textarea id="comment" placeholder="Comment, optional: what looks off?">${entry && entry.comment ? entry.comment : ""}</textarea>
    <div id="result">${result}</div><div class="row"><button id="back">← Back</button><button id="next">Next →</button></div>`;
  document.querySelectorAll("[data-answer]").forEach(b => b.onclick = () => save({ answer: b.dataset.answer, correct: b.dataset.answer === item.generated }));
  document.querySelectorAll("[data-grade]").forEach(b => b.onclick = () => save({ grade: Number(b.dataset.grade) }));
  document.getElementById("comment").onchange = () => { if (ratings[key(item)]) save({}); };
  document.getElementById("back").onclick = () => move(-1);
  document.getElementById("next").onclick = () => move(1);
}

document.onkeydown = event => {
  if (["TEXTAREA", "INPUT"].includes(event.target.tagName)) return;
  const press = event.key.toLowerCase(), item = current();
  if (event.key === "ArrowRight") move(1);
  else if (event.key === "ArrowLeft") move(-1);
  else if (mode === "twin" && "abn".includes(press) && press) {
    const answer = press === "n" ? "neither" : press.toUpperCase();
    save({ answer, correct: answer === item.generated });
  } else if (mode === "card" && "12345".includes(press) && press) save({ grade: Number(press) });
};
for (const kind of ["twin", "card"]) document.getElementById("tab-" + kind).onclick = () => { mode = kind; show(); };
fetch("/data").then(r => r.json()).then(data => {
  items = data.items; ratings = data.ratings;
  for (const kind of ["twin", "card"]) position[kind] = Math.max(0, list(kind).findIndex(i => !ratings[key(i)]));
  show();
});
</script></body></html>"""


def main():
    global ITEMS
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.summary:
        summary()
        return
    ITEMS = items()
    print(f"open http://127.0.0.1:{args.port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Page).serve_forever()


if __name__ == "__main__":
    main()
