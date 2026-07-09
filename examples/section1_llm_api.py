from __future__ import annotations

import json
from pathlib import Path

from live_llm import call_json
from schema import DocumentExtraction, Evidence, filter_evidence_to_allowed


ROOT = Path(__file__).resolve().parent


def load_notes() -> list[dict]:
    return json.loads((ROOT / "data" / "notes.json").read_text(encoding="utf-8"))


def build_prompt(note: str) -> str:
    return f"""
당신은 기술 문서를 읽는 개발 보조자입니다.
아래 문서에서 topic, objective, method, result를 추출하세요.
문서에 없는 정보는 추측하지 말고 "not specified"라고 쓰세요.
가능하면 근거 문장도 포함하세요.

문서:
{note}
""".strip()


def calibrated_confidence(raw_confidence: float, raw: dict) -> float:
    confidence = float(raw_confidence)
    joined = " ".join(
        str(value)
        for key in ("objective", "method", "result", "limitations")
        for value in ([raw.get(key)] if not isinstance(raw.get(key), list) else raw.get(key, []))
    ).lower()
    missing_markers = (
        "not specified",
        "does not specify",
        "unspecified",
        "missing",
        "lack",
        "lacked",
        "없음",
        "명시되지",
    )
    if any(marker in joined for marker in missing_markers):
        return min(confidence, 0.45)
    return confidence


def live_llm_extract(note_id: str, note: str) -> DocumentExtraction:
    raw = call_json(
        f"""
당신은 기술 문서와 짧은 연구 문서를 구조화하는 개발 보조자입니다.
아래 문서에서 정보를 추출하세요.

필드:
- topic: 문서의 주제
- objective: 문서가 달성하려는 목표
- method: 목표를 달성하는 방법
- result: 문서가 말하는 결과
- limitations: 한계 목록. 없으면 빈 배열
- evidence: source_id와 quote를 가진 배열. source_id는 "{note_id}"만 사용
- confidence: 0과 1 사이 숫자

규칙:
- 문서에 없는 내용은 추측하지 말고 "not specified"라고 쓰세요.
- evidence quote는 반드시 아래 문서에서 온 문장이나 구절이어야 합니다.
- 입력 데이터, 평가 지표, 검증 방법처럼 핵심 정보가 명시되지 않았으면 confidence를 0.45 이하로 두세요.

문서:
{note}
""".strip()
    )
    allowed_evidence = [Evidence(source_id=note_id, quote=note)]
    accepted_evidence = filter_evidence_to_allowed(
        raw.get("evidence", []),
        allowed_evidence,
        default_source_id=note_id,
    )
    return DocumentExtraction(
        topic=raw["topic"],
        objective=raw["objective"],
        method=raw["method"],
        result=raw["result"],
        limitations=raw.get("limitations", []),
        evidence=accepted_evidence,
        confidence=calibrated_confidence(raw["confidence"], raw),
    )


def main() -> None:
    for item in load_notes():
        prompt = build_prompt(item["text"])
        extraction = live_llm_extract(item["id"], item["text"])
        print("\n--- PROMPT PREVIEW ---")
        print(prompt[:350] + "...")
        print("--- LIVE LLM VALIDATED OUTPUT ---")
        print(json.dumps(extraction.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
