from __future__ import annotations

from rocoworld_yise_detector.models import DetectionResult, EncounterRecord, MonsterVariant


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized or None


class ShinyDetector:
    def __init__(self, variants: list[MonsterVariant]) -> None:
        self.variants = variants

    def detect(self, encounter: EncounterRecord) -> DetectionResult:
        encounter_fields = {
            key: value
            for key, value in ((_key, _normalize(_value)) for _key, _value in encounter.as_match_map().items())
            if value is not None
        }

        candidates: list[tuple[int, MonsterVariant]] = []
        for variant in self.variants:
            if not self._variant_matches_identity(variant, encounter_fields):
                continue
            if not self._variant_matches_fields(variant, encounter_fields):
                continue
            candidates.append((self._specificity_score(variant), variant))

        if not candidates:
            return DetectionResult(
                status="UNKNOWN",
                encounter=encounter,
                reason="No database rule matched the current encounter fields.",
            )

        candidates.sort(key=lambda item: item[0], reverse=True)
        _, best = candidates[0]
        return DetectionResult(
            status="SHINY" if best.is_shiny else "NORMAL",
            encounter=encounter,
            reason=f"Matched rule '{best.label}'.",
            matched_variant=best,
        )

    def _variant_matches_identity(self, variant: MonsterVariant, encounter_fields: dict[str, str]) -> bool:
        identity_pairs = {
            "monster_id": variant.monster_id,
            "monster_name": variant.monster_name,
            "form": variant.form,
            "skin": variant.skin,
        }
        matched_identity = False
        for field_name, variant_value in identity_pairs.items():
            normalized = _normalize(variant_value)
            if normalized is None:
                continue
            encounter_value = encounter_fields.get(field_name)
            if encounter_value != normalized:
                return False
            matched_identity = True
        return matched_identity

    def _variant_matches_fields(self, variant: MonsterVariant, encounter_fields: dict[str, str]) -> bool:
        for key, expected in variant.match_fields.items():
            if encounter_fields.get(key) != _normalize(expected):
                return False
        return True

    @staticmethod
    def _specificity_score(variant: MonsterVariant) -> int:
        score = len(variant.match_fields) * 10
        for value in (variant.monster_id, variant.monster_name, variant.form, variant.skin):
            if _normalize(value) is not None:
                score += 1
        return score

