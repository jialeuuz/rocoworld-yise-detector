from __future__ import annotations

import time
from pathlib import Path
from typing import Iterator


def _read_text_with_fallback(path: Path, encodings: tuple[str, ...]) -> str:
    raw = path.read_bytes()
    last_error: UnicodeDecodeError | None = None
    for encoding in encodings:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    return raw.decode()


def scan_log_file(path: str | Path, encodings: tuple[str, ...]) -> list[str]:
    target = Path(path)
    if not target.exists():
        return []
    return _read_text_with_fallback(target, encodings).splitlines()


def tail_log_file(
    path: str | Path,
    encodings: tuple[str, ...],
    poll_interval_seconds: float,
    from_start: bool = False,
) -> Iterator[str]:
    target = Path(path)
    previous_lines: list[str] = []

    while True:
        if not target.exists():
            time.sleep(poll_interval_seconds)
            continue

        current_lines = _read_text_with_fallback(target, encodings).splitlines()

        if not previous_lines and from_start:
            new_lines = current_lines
        elif len(current_lines) < len(previous_lines):
            new_lines = current_lines
        else:
            new_lines = current_lines[len(previous_lines):]

        for line in new_lines:
            yield line

        previous_lines = current_lines
        time.sleep(poll_interval_seconds)

