from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Evidence(StrictModel):
    source_id: str = Field(min_length=1)
    quote: str = Field(min_length=1)


def normalize_evidence_items(
    value: Any,
    *,
    default_source_id: str = "not specified",
    fallback: list[Evidence] | None = None,
) -> list[Evidence]:
    """Convert common LLM evidence variants into Evidence objects."""
    if value is None:
        return []
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        value = [value]

    normalized: list[Evidence] = []
    for item in value:
        if isinstance(item, Evidence):
            normalized.append(item)
        elif isinstance(item, dict):
            source_id = str(item.get("source_id") or default_source_id)
            quote = str(item.get("quote") or item.get("text") or "").strip()
            if quote:
                normalized.append(Evidence(source_id=source_id, quote=quote))
        elif isinstance(item, str):
            quote = item.strip()
            if not quote:
                continue
            matched = None
            for candidate in fallback or []:
                if quote in candidate.quote or candidate.quote in quote:
                    matched = candidate.source_id
                    break
            normalized.append(Evidence(source_id=matched or default_source_id, quote=quote))
    return normalized


def filter_evidence_to_allowed(
    value: Any,
    allowed: list[Evidence],
    *,
    default_source_id: str = "not specified",
) -> list[Evidence]:
    """Keep only evidence that can be matched to the retrieved context."""
    candidates = normalize_evidence_items(
        value,
        default_source_id=default_source_id,
        fallback=allowed,
    )
    accepted: list[Evidence] = []
    seen: set[tuple[str, str]] = set()

    for candidate in candidates:
        for item in allowed:
            same_source = candidate.source_id == item.source_id
            exact_quote = candidate.quote == item.quote
            quote_inside_allowed = candidate.quote in item.quote
            allowed_inside_quote = item.quote in candidate.quote
            if same_source and (exact_quote or quote_inside_allowed or allowed_inside_quote):
                key = (item.source_id, item.quote)
                if key not in seen:
                    accepted.append(item)
                    seen.add(key)
                break

    return accepted


class DocumentExtraction(StrictModel):
    topic: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    method: str = Field(min_length=1)
    result: str = Field(min_length=1)
    limitations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("limitations", mode="before")
    @classmethod
    def normalize_limitations(cls, value: Any) -> list[str]:
        """Accept common LLM variants while keeping the public schema stable."""
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, str):
            normalized = value.strip()
            if not normalized or normalized.lower() in {"none", "not specified", "n/a", "없음"}:
                return []
            return [normalized]
        return [str(value)]

    @field_validator("confidence", mode="before")
    @classmethod
    def reject_non_numeric_confidence(cls, value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError("confidence must be a number between 0 and 1")
        return float(value)

    @model_validator(mode="after")
    def require_evidence_for_confident_claims(self) -> "DocumentExtraction":
        if self.confidence >= 0.5 and not self.evidence:
            raise ValueError("evidence is required when confidence is 0.5 or higher")
        return self

class GroundedAnswer(StrictModel):
    answer_ko: str = Field(min_length=1)
    evidence: list[Evidence] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    not_answered: bool = False


class WorkflowAnswer(StrictModel):
    answer_ko: str = Field(min_length=1)
    facts: DocumentExtraction
    evidence: list[Evidence] = Field(default_factory=list)
    not_answered: bool = False
    log: list[str] = Field(default_factory=list)


if __name__ == "__main__":
    example = DocumentExtraction(
        topic="support ticket routing",
        objective="route incoming support tickets to the right team",
        method="rule-based classifier with optional LLM review",
        result="reduced manual triage work in the pilot queue",
        limitations=["requires periodic label review"],
        evidence=[
            Evidence(
                source_id="note_a",
                quote="reduced manual triage work in the pilot queue",
            )
        ],
        confidence=0.9,
    )
    print(example.model_dump_json(indent=2))
