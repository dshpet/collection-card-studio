"""Offline checks of how runs resume: a fix round (make_set.py --keep) keeps unchanged cards and redraws the rest,
and a rerun continues only the same request."""

import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import make_set  # noqa: E402
from make_set import keep_cards, run_folder  # noqa: E402

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

    def test_a_new_setting_gets_a_new_model(self):
        self.keep({**CARD, "surface_or_setting": "hanging from a nail on a wall"})
        self.assertFalse((self.run / "models" / "v1_01.png").exists())


class RequestTest(unittest.TestCase):
    ARGS = dict(theme="Western", wishes="", variants=3, cast=0, plan=None, no_references=False, alongside=[],
                no_blockouts=False, candidates=make_set.CANDIDATES, rater=make_set.JUDGE,
                review_rounds=make_set.REVIEW_ROUNDS, keep=None, run=None)

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        patcher = mock.patch.object(make_set, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.folder.cleanup)

    def record(self, name, request):
        (self.root / "runs" / name).mkdir(parents=True)
        (self.root / "runs" / name / "request.json").write_text(json.dumps(request))

    def test_the_same_request_continues_its_folder(self):
        run, request = run_folder(Namespace(**self.ARGS))
        self.record("western", request)
        self.assertEqual(run_folder(Namespace(**self.ARGS))[0].name, "western")

    def test_more_candidates_start_a_new_folder(self):
        self.record("western", run_folder(Namespace(**self.ARGS))[1])
        self.assertEqual(run_folder(Namespace(**{**self.ARGS, "candidates": 8}))[0].name, "western-2")

    def test_an_older_run_counts_as_made_with_the_defaults(self):
        request = run_folder(Namespace(**self.ARGS))[1]
        self.record("western", {k: v for k, v in request.items() if k not in make_set.LATER})
        self.assertEqual(run_folder(Namespace(**self.ARGS))[0].name, "western")
        self.assertEqual(run_folder(Namespace(**{**self.ARGS, "candidates": 8}))[0].name, "western-2")
        self.assertEqual(run_folder(Namespace(**{**self.ARGS, "review_rounds": 0}))[0].name, "western-2")


if __name__ == "__main__":
    unittest.main()
