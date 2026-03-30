from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rocoworld_yise_detector.config import DEFAULT_FIELD_ALIASES
from rocoworld_yise_detector.parser import EncounterParser


class EncounterParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = EncounterParser(dict(DEFAULT_FIELD_ALIASES), ("ENCOUNTER",))

    def test_parse_line_extracts_canonical_fields(self) -> None:
        line = '2026-03-30 ENCOUNTER monster_id=1001 monster_name="火花" form=default palette=crimson'
        record = self.parser.parse_line(line)

        self.assertIsNotNone(record)
        assert record is not None
        self.assertEqual(record.monster_id, "1001")
        self.assertEqual(record.monster_name, "火花")
        self.assertEqual(record.form, "default")
        self.assertEqual(record.palette, "crimson")

    def test_parse_line_returns_none_for_non_encounter_line(self) -> None:
        record = self.parser.parse_line("2026-03-30 DEBUG scene=battle_ui")
        self.assertIsNone(record)


if __name__ == "__main__":
    unittest.main()

