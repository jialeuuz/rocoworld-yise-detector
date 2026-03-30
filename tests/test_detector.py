from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rocoworld_yise_detector.detector import ShinyDetector
from rocoworld_yise_detector.models import EncounterRecord, MonsterVariant


class ShinyDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = ShinyDetector(
            [
                MonsterVariant(
                    monster_id="1001",
                    monster_name="火花",
                    form="default",
                    skin=None,
                    label="火花 / Standard",
                    is_shiny=False,
                    match_fields={"palette": "standard"},
                ),
                MonsterVariant(
                    monster_id="1001",
                    monster_name="火花",
                    form="default",
                    skin=None,
                    label="火花 / Shiny Crimson",
                    is_shiny=True,
                    match_fields={"palette": "crimson"},
                ),
            ]
        )

    def test_detects_shiny_variant(self) -> None:
        encounter = EncounterRecord(
            source_line="ENCOUNTER monster_id=1001 monster_name=火花 form=default palette=crimson",
            monster_id="1001",
            monster_name="火花",
            form="default",
            palette="crimson",
        )

        result = self.detector.detect(encounter)
        self.assertEqual(result.status, "SHINY")
        self.assertIsNotNone(result.matched_variant)
        assert result.matched_variant is not None
        self.assertTrue(result.matched_variant.is_shiny)

    def test_returns_unknown_when_no_rule_matches(self) -> None:
        encounter = EncounterRecord(
            source_line="ENCOUNTER monster_id=9999 monster_name=未知兽 form=default",
            monster_id="9999",
            monster_name="未知兽",
            form="default",
        )

        result = self.detector.detect(encounter)
        self.assertEqual(result.status, "UNKNOWN")
        self.assertIsNone(result.matched_variant)


if __name__ == "__main__":
    unittest.main()
