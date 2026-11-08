"""Rebuild text, inventory and galleries offline; never acquire or resample images.

Refresh sources/board.svg through Codex + Miro separately. Local images are the
board's original files; sources/original_images.json records their provenance.
"""

import argparse
from collections import defaultdict
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from common import ROOT


DOCUMENTS = {
    "3458764679650208648": "02_collection_explanation",
    "3458764679650284128": "03_art_guide",
    "3458764679652501906": "01_task_description",
}
FRAMES = {
    "Примеры карточек": "card_examples",
    "Пример коллекции": "collection_examples",
    "Фрейм для описания хода работы и результатов": "result_templates",
}
# Deliberately omit source URLs and arbitrary attributes from derived inventories.
ATTRIBUTES = (
    "data-miro-id", "data-type", "data-widget-type", "data-frame",
    "x", "y", "width", "height", "transform",
)


def save(path, text):
    data = text.encode("utf-8")
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def position(item):
    return float(item.get("y", 0)), float(item.get("x", 0)), item["data-miro-id"]


def main():
    board = ET.parse(ROOT / "sources/board.svg").getroot()
    items, documents = [], {}

    def walk(element, frame="board"):
        frame = element.attrib.get("data-frame", frame)
        tag = element.tag.split("}")[-1]
        item_id = element.attrib.get("data-miro-id")
        if item_id:
            text = "".join(element.itertext()).strip()
            item = {key: element.attrib[key] for key in ATTRIBUTES if key in element.attrib}
            items.append(dict(item, frame=frame, tag=tag, text=text))
            if tag == "foreignObject" and item_id in DOCUMENTS:
                documents[DOCUMENTS[item_id]] = text + "\n"
        for child in element:
            walk(child, frame)

    walk(board)
    if set(documents) != set(DOCUMENTS.values()):
        raise ValueError("Expected three saved board documents; check the Codex + Miro export.")

    provenance = json.loads((ROOT / "sources/original_images.json").read_text("utf-8"))
    images = sorted((item for item in items if item["tag"] == "image"), key=position)
    manifest = []
    for item in images:
        item_id = item["data-miro-id"]
        group = FRAMES.get(item["frame"])
        entry = {
            "id": item_id, "frame": item["frame"], "group": group,
            "x": float(item.get("x", 0)), "y": float(item.get("y", 0)),
            "status": "missing_local_image",
        }
        local = ROOT / "materials" / str(group) / (item_id + ".png")
        if group and local.is_file():
            data = local.read_bytes()
            width, height = (int.from_bytes(data[i:i + 4], "big") for i in (16, 20))
            entry.update(
                status="board_original",
                file=local.relative_to(ROOT).as_posix(),
                sha256=sha256(data).hexdigest(),
                width=width, height=height,
                board_filename=provenance[item_id]["board_filename"],
            )
        manifest.append(entry)

    cards = defaultdict(list)
    for item in images:
        if item["frame"] == "Примеры карточек":
            cards[float(item.get("y", 0))].append(item)
    card_html = (
        '<meta charset="utf-8"><h1>Card references</h1>'
        '<p>Board original files, ordered by board row and column.</p>'
        '<div style="display:grid;grid-template-columns:repeat(10,1fr);gap:8px">'
    )
    for row, y in enumerate(sorted(cards), 1):
        for column, item in enumerate(sorted(cards[y], key=position), 1):
            filename = item["data-miro-id"] + ".png"
            if (ROOT / "materials/card_examples" / filename).is_file():
                card_html += (
                    f'<a href="{escape(filename, quote=True)}"><img width="90" '
                    f'src="{escape(filename, quote=True)}"><br>{row}:{column}</a>'
                )
    card_html += "</div>"

    collection_html = (
        '<html><meta charset="utf-8"><title>Collection examples</title><style>'
        'body{font-family:sans-serif} .grid{display:grid;grid-template-columns:repeat(5,1fr);gap:16px}'
        'img{max-width:100%;max-height:280px}figure{margin:0}'
        'figcaption{font-size:11px;overflow-wrap:anywhere}</style><h1>Collection examples</h1>'
    )
    collection_html += '<div class="grid">'
    for entry in manifest:
        if entry["group"] == "collection_examples" and "file" in entry:
            filename = escape(entry["id"] + ".png", quote=True)
            collection_html += (
                f'<figure><a href="{filename}"><img loading="lazy" src="{filename}"></a>'
                f'<figcaption>{entry["id"]}<br>board x={entry["x"]}, '
                f'y={entry["y"]}</figcaption></figure>'
            )
    collection_html += "</div></html>"

    for name, text in documents.items():
        save(ROOT / "materials" / (name + ".md"), text)
    save(ROOT / "sources/items.json", json_text(items))
    save(ROOT / "sources/image_manifest.json", json_text(manifest))
    save(ROOT / "materials/card_examples/index.html", card_html)
    save(ROOT / "materials/collection_examples/index.html", collection_html)
    print(f"Offline rebuild: {len(documents)} documents, {len(items)} inventory entries, "
          f"{len(manifest)} board images; existing image files unchanged.")


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()  # --help only; the script takes no options
    main()
