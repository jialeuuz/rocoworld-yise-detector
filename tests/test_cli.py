from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rocoworld_yise_detector.cli import main


class CliTests(unittest.TestCase):
    def _write_config(self, temp_dir: str) -> Path:
        root = Path(temp_dir)
        database_path = root / "variants.json"
        database_path.write_text("[]", encoding="utf-8")

        config_path = root / "config.json"
        config_path.write_text(
            json.dumps(
                {
                    "log_path": "missing.log",
                    "database_path": "variants.json",
                    "encodings": ["utf-8", "gbk"],
                    "poll_interval_seconds": 0.01,
                    "line_filters": ["ENCOUNTER"],
                    "field_aliases": {},
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return config_path

    def test_scan_warns_when_log_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self._write_config(temp_dir)
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = main(["scan", "--config", str(config_path)])

        self.assertEqual(exit_code, 0)
        self.assertIn("Log file not found:", stderr.getvalue())
        self.assertIn("Enable deep logging", stderr.getvalue())

    def test_watch_warns_when_log_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = self._write_config(temp_dir)
            stderr = io.StringIO()

            with mock.patch("rocoworld_yise_detector.cli.tail_log_file", side_effect=KeyboardInterrupt):
                with redirect_stderr(stderr):
                    exit_code = main(["watch", "--config", str(config_path)])

        self.assertEqual(exit_code, 0)
        self.assertIn("Log file not found:", stderr.getvalue())
        self.assertIn("Enable deep logging", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
