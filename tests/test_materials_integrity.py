"""Check the real image corpus against its manifest and provenance records."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"card_examples": 160, "collection_examples": 16, "result_templates": 4}


class MaterialsIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "sources/image_manifest.json").read_text("utf-8"))
        cls.provenance = json.loads((ROOT / "sources/original_images.json").read_text("utf-8"))

    def test_expected_counts_all_promoted(self):
        counts = {}
        for entry in self.manifest:
            self.assertEqual(entry["status"], "board_original", entry["id"])
            counts[entry["group"]] = counts.get(entry["group"], 0) + 1
        self.assertEqual(counts, EXPECTED)

    def test_manifest_matches_provenance_and_files(self):
        self.assertEqual({e["id"] for e in self.manifest}, set(self.provenance))
        for entry in self.manifest:
            record = self.provenance[entry["id"]]
            self.assertEqual(entry["file"], record["file"])
            self.assertEqual(entry["sha256"], record["sha256"])
            self.assertEqual(sha256((ROOT / entry["file"]).read_bytes()).hexdigest(),
                             record["sha256"], entry["id"])

    def test_no_untracked_images(self):
        tracked = {e["file"] for e in self.manifest}
        for group in EXPECTED:
            found = {p.relative_to(ROOT).as_posix()
                     for p in (ROOT / "materials" / group).glob("*.png")}
            self.assertEqual(found - tracked, set(), group)


if __name__ == "__main__":
    unittest.main()
