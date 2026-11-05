"""Real photos of an object from Wikimedia Commons, for the modeller to see how it is built.

    photos.py "covered wagon" runs/trial2/photos/wagon

Fetches twenty candidates, then a model keeps up to three clear photos of the whole real object.
Photos are untrusted downloads: each is opened as an image and re-saved as PNG, and nothing else is kept.
"""

import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "scripts"))  # the pipeline's modules

import argparse
import io
import json
import urllib.parse
import urllib.request

from PIL import Image

from rate import ask_claude

API = "https://commons.wikimedia.org/w/api.php"
AGENT = {"User-Agent": "card-photo-reference/0.1 (research script)"}
PICK_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["picks"],
               "properties": {"picks": {"type": "array", "items": {"type": "integer"}}}}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=60) as response:
        return response.read()


def candidates(query, limit=20):
    params = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrlimit": limit,
              "gsrsearch": f"{query} -poster -film -movie -drawing -painting filetype:bitmap", "prop": "imageinfo", "iiprop": "url|mime", "iiurlwidth": 800}
    pages = json.loads(get(f"{API}?{urllib.parse.urlencode(params)}")).get("query", {}).get("pages", {})
    return [p["imageinfo"][0]["thumburl"] for p in sorted(pages.values(), key=lambda p: p.get("index", 0))
            if p.get("imageinfo") and p["imageinfo"][0].get("mime") in ("image/jpeg", "image/png")]


def fetch(query, out, keep=3):
    """Saves up to keep photos as out/1.png... and returns their paths."""
    out = Path(out).resolve()
    if (out / "picks.json").exists():
        return [out / name for name in json.loads((out / "picks.json").read_text())["files"]]
    pool = out / "candidates"
    pool.mkdir(parents=True, exist_ok=True)
    paths = []
    for number, url in enumerate(candidates(query), 1):
        try:
            image = Image.open(io.BytesIO(get(url))).convert("RGB")
        except Exception:
            continue
        image.thumbnail((800, 800))
        path = pool / f"{number:02d}.png"
        image.save(path)
        paths.append(path)
    picks = ask_claude(f"These are search results for photos of: {query}. Pick up to {keep} real photos in which most of "
                       "one such object is visible, so a 3D modeller can see its main parts and how they connect. Some "
                       "background or a partly hidden part is fine. Skip posters, paintings, drawings, close-ups of one "
                       "part and scenes where the object is tiny. Answer with their positions in the list, counting from "
                       "1, best first. Pick at least one unless none shows the object.", paths, PICK_SCHEMA)["picks"]
    chosen = [paths[i - 1] for i in picks if 0 < i <= len(paths)][:keep]
    files = []
    for number, path in enumerate(chosen, 1):
        target = out / f"{number}.png"
        target.write_bytes(path.read_bytes())
        files.append(target.name)
    (out / "picks.json").write_text(json.dumps({"query": query, "files": files}))
    return [out / name for name in files]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("out")
    args = parser.parse_args()
    print(fetch(args.query, args.out))


if __name__ == "__main__":
    main()
