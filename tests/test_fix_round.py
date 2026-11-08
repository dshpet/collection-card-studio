"""A fix round (make_set.py --keep) keeps unchanged cards and redraws the rest, offline."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from make_set import keep_cards  # noqa: E402

CARD = {"name": "Pocket Watch", "subject": "A gold pocket watch on a chain", "category": "1",
        "pattern": "rays", "hero_colors": "gold", "build_model": True}


class FixRoundTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.source, self.run = Path(self.folder.name, "source"), Path(self.folder.name, "fix")
        for sub in ("tries", "models"):
            (self.source / sub).mkdir(parents=True)
        (self.source / "tries" / "v1_01_1.png").write_bytes(b"png")
        (self.source / "models" / "v1_01.png").write_bytes(b"render")
        (self.source / "briefs.json").write_text(json.dumps([{"id": "v1_01", "card": CARD}]))
        (self.source / "check.json").write_text(json.dumps({"v1_01": [{"try_id": "v1_01_1", "chosen": True}]}))

    def tearDown(self):
        self.folder.cleanup()

    def keep(self, card):
        return keep_cards(self.run, self.source, [{"id": "v1_01", "card": card}])[0]

    def test_an_unchanged_card_keeps_its_drawing_and_pick(self):
        brief = self.keep(dict(CARD))
        history = json.loads((self.run / "check.json").read_text())
        self.assertEqual(brief["card"], CARD)
        self.assertTrue(history["v1_01"][0]["kept"] and history["v1_01"][0]["chosen"])
        self.assertTrue((self.run / "tries" / "v1_01_1.png").exists())

    def test_new_colors_redraw_the_card_on_the_same_model(self):
        self.keep({**CARD, "hero_colors": "silver"})
        self.assertEqual(json.loads((self.run / "check.json").read_text()), {})
        self.assertTrue((self.run / "models" / "v1_01.png").exists())

    def test_a_producer_note_gets_a_new_model(self):
        self.keep({**CARD, "note": "a shorter, sturdier chain"})
        self.assertEqual(json.loads((self.run / "check.json").read_text()), {})
        self.assertFalse((self.run / "models" / "v1_01.png").exists())


if __name__ == "__main__":
    unittest.main()
