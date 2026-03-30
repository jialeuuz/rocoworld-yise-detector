from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EncounterRecord:
    source_line: str
    monster_id: str | None = None
    monster_name: str | None = None
    form: str | None = None
    skin: str | None = None
    palette: str | None = None
    rare_flag: str | None = None
    extras: dict[str, str] = field(default_factory=dict)

    def as_match_map(self) -> dict[str, str]:
        values: dict[str, str] = {}
        for key in ("monster_id", "monster_name", "form", "skin", "palette", "rare_flag"):
            value = getattr(self, key)
            if value:
                values[key] = value
        values.update(self.extras)
        return values


@dataclass(slots=True)
class MonsterVariant:
    monster_id: str | None
    monster_name: str | None
    form: str | None
    skin: str | None
    label: str
    is_shiny: bool
    match_fields: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class DetectionResult:
    status: str
    encounter: EncounterRecord
    reason: str
    matched_variant: MonsterVariant | None = None

