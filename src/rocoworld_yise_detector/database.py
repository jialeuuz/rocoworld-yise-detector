from __future__ import annotations

import json
from pathlib import Path

from rocoworld_yise_detector.models import MonsterVariant


def load_variants(path: str | Path) -> list[MonsterVariant]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = payload["variants"] if isinstance(payload, dict) else payload
    variants: list[MonsterVariant] = []
    for row in rows:
        variants.append(
            MonsterVariant(
                monster_id=row.get("monster_id"),
                monster_name=row.get("monster_name"),
                form=row.get("form"),
                skin=row.get("skin"),
                label=row.get("label") or row.get("monster_name") or "unknown",
                is_shiny=bool(row.get("is_shiny", False)),
                match_fields={str(key): str(value) for key, value in row.get("match_fields", {}).items()},
            )
        )
    return variants

