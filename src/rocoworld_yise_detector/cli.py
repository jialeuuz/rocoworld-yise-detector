from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rocoworld_yise_detector.config import load_config
from rocoworld_yise_detector.database import load_variants
from rocoworld_yise_detector.detector import ShinyDetector
from rocoworld_yise_detector.models import DetectionResult, EncounterRecord
from rocoworld_yise_detector.parser import EncounterParser
from rocoworld_yise_detector.watcher import scan_log_file, tail_log_file


DEEP_LOG_HINT = (
    "For real game logs, enable deep logging (深度日志) first: in game Compass -> Settings -> User -> "
    "Enable deep logging, or from the login screen Repair Tool -> Enable deep logging."
)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rocoworld-yise-detector",
        description="Local log-based shiny detector scaffold for Rocoworld.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a log file once.")
    scan_parser.add_argument("--config", default="config/config.example.json", help="Path to the JSON config file.")
    scan_parser.add_argument("--file", help="Optional log file override.")

    watch_parser = subparsers.add_parser("watch", help="Watch a log file for appended lines.")
    watch_parser.add_argument("--config", default="config/config.example.json", help="Path to the JSON config file.")
    watch_parser.add_argument("--from-start", action="store_true", help="Emit existing lines when watch starts.")

    parse_line_parser = subparsers.add_parser("parse-line", help="Parse a single log line for debugging.")
    parse_line_parser.add_argument("--config", default="config/config.example.json", help="Path to the JSON config file.")
    parse_line_parser.add_argument("--line", required=True, help="A raw log line to parse.")

    return parser


def _record_to_dict(record: EncounterRecord) -> dict[str, object]:
    return {
        "monster_id": record.monster_id,
        "monster_name": record.monster_name,
        "form": record.form,
        "skin": record.skin,
        "palette": record.palette,
        "rare_flag": record.rare_flag,
        "extras": record.extras,
    }


def _format_result(result: DetectionResult) -> str:
    encounter = result.encounter
    bits = [result.status]
    if encounter.monster_name:
        bits.append(f"name={encounter.monster_name}")
    if encounter.monster_id:
        bits.append(f"id={encounter.monster_id}")
    if encounter.form:
        bits.append(f"form={encounter.form}")
    if result.matched_variant is not None:
        bits.append(f"rule={result.matched_variant.label}")
    bits.append(f"reason={result.reason}")
    return " | ".join(bits)


def _process_line(raw_line: str, parser: EncounterParser, detector: ShinyDetector) -> str | None:
    record = parser.parse_line(raw_line)
    if record is None:
        return None
    return _format_result(detector.detect(record))


def _warn_missing_log_file(log_path: Path) -> None:
    print(
        f"Log file not found: {log_path}. {DEEP_LOG_HINT} Then verify that log_path points to the generated file.",
        file=sys.stderr,
    )


def _scan(config_path: str, file_override: str | None) -> int:
    config = load_config(config_path)
    parser = EncounterParser(config.field_aliases, config.line_filters)
    detector = ShinyDetector(load_variants(config.database_path))
    log_path = Path(file_override).resolve() if file_override else config.log_path

    if not log_path.exists():
        _warn_missing_log_file(log_path)
        return 0

    for line in scan_log_file(log_path, config.encodings):
        rendered = _process_line(line, parser, detector)
        if rendered:
            print(rendered)
    return 0


def _watch(config_path: str, from_start: bool) -> int:
    config = load_config(config_path)
    parser = EncounterParser(config.field_aliases, config.line_filters)
    detector = ShinyDetector(load_variants(config.database_path))

    if not config.log_path.exists():
        _warn_missing_log_file(config.log_path)

    try:
        for line in tail_log_file(
            config.log_path,
            config.encodings,
            config.poll_interval_seconds,
            from_start=from_start,
        ):
            rendered = _process_line(line, parser, detector)
            if rendered:
                print(rendered)
    except KeyboardInterrupt:
        return 0
    return 0


def _parse_line(config_path: str, raw_line: str) -> int:
    config = load_config(config_path)
    parser = EncounterParser(config.field_aliases, config.line_filters)
    record = parser.parse_line(raw_line)
    print(json.dumps(_record_to_dict(record) if record else None, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return _scan(args.config, args.file)
    if args.command == "watch":
        return _watch(args.config, args.from_start)
    if args.command == "parse-line":
        return _parse_line(args.config, args.line)
    parser.error(f"Unsupported command: {args.command}")
    return 2
