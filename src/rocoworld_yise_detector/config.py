from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_FIELD_ALIASES = {
    "monster_id": ("monster_id", "pet_id", "id"),
    "monster_name": ("monster_name", "pet_name", "name"),
    "form": ("form", "variant", "shape"),
    "skin": ("skin", "appearance", "costume"),
    "palette": ("palette", "color", "colour", "chromatic"),
    "rare_flag": ("rare_flag", "shiny", "is_shiny"),
}


@dataclass(slots=True)
class AppConfig:
    config_path: Path
    log_path: Path
    database_path: Path
    encodings: tuple[str, ...] = ("utf-8", "gbk")
    poll_interval_seconds: float = 1.0
    line_filters: tuple[str, ...] = ("ENCOUNTER",)
    field_aliases: dict[str, tuple[str, ...]] = field(default_factory=dict)


def _resolve_path(base_path: Path, target: str) -> Path:
    candidate = Path(target)
    if candidate.is_absolute():
        return candidate
    return (base_path.parent / candidate).resolve()


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path).resolve()
    payload = json.loads(config_path.read_text(encoding="utf-8"))

    field_aliases: dict[str, tuple[str, ...]] = {}
    raw_aliases = payload.get("field_aliases", {})
    for key, default_aliases in DEFAULT_FIELD_ALIASES.items():
        configured = raw_aliases.get(key, default_aliases)
        field_aliases[key] = tuple(alias.lower() for alias in configured)

    return AppConfig(
        config_path=config_path,
        log_path=_resolve_path(config_path, payload["log_path"]),
        database_path=_resolve_path(config_path, payload["database_path"]),
        encodings=tuple(payload.get("encodings", ("utf-8", "gbk"))),
        poll_interval_seconds=float(payload.get("poll_interval_seconds", 1.0)),
        line_filters=tuple(payload.get("line_filters", ("ENCOUNTER",))),
        field_aliases=field_aliases,
    )

