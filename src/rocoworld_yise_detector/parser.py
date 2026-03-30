from __future__ import annotations

import re

from rocoworld_yise_detector.models import EncounterRecord


KEY_VALUE_PATTERN = re.compile(r"(?P<key>[A-Za-z0-9_]+)=(?P<value>\"[^\"]*\"|'[^']*'|\S+)")


def _clean_value(raw: str) -> str:
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
        return raw[1:-1]
    return raw


class EncounterParser:
    def __init__(self, field_aliases: dict[str, tuple[str, ...]], line_filters: tuple[str, ...] = ()) -> None:
        self.field_aliases = field_aliases
        self.line_filters = tuple(line_filters)

    def parse_line(self, line: str) -> EncounterRecord | None:
        if self.line_filters and not any(token in line for token in self.line_filters):
            return None

        pairs: dict[str, str] = {}
        for match in KEY_VALUE_PATTERN.finditer(line):
            key = match.group("key").lower()
            pairs[key] = _clean_value(match.group("value"))

        if not pairs:
            return None

        def pick(canonical_key: str) -> str | None:
            for alias in self.field_aliases.get(canonical_key, (canonical_key,)):
                if alias in pairs:
                    return pairs[alias]
            return None

        record = EncounterRecord(
            source_line=line.rstrip("\n"),
            monster_id=pick("monster_id"),
            monster_name=pick("monster_name"),
            form=pick("form"),
            skin=pick("skin"),
            palette=pick("palette"),
            rare_flag=pick("rare_flag"),
        )

        if not record.monster_id and not record.monster_name:
            return None

        used_aliases = {
            alias
            for aliases in self.field_aliases.values()
            for alias in aliases
        }
        record.extras = {key: value for key, value in pairs.items() if key not in used_aliases}
        return record

