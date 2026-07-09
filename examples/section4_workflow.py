from __future__ import annotations

import json

from live_llm import call_json
from schema import DocumentExtraction, GroundedAnswer, WorkflowAnswer
from schema import filter_evidence_to_allowed
from section3_langchain_rag import answer_question


def build_facts(grounded: GroundedAnswer) -> DocumentExtraction:
    if grounded.not_answered:
        return DocumentExtraction(
            topic="not specified",
            objective="not specified",
            method="not specified",
            result="not specified",
            limitations=["no supporting evidence in corpus"],
            evidence=grounded.evidence,
            confidence=0.2,
        )

    raw = call_json(
        f"""
당신은 workflow의 structured facts 추출 단계입니다.
아래 한국어 답변과 evidence만 사용해 구조화 정보를 추출하세요.

규칙:
- evidence에 없는 내용은 추측하지 말고 "not specified"라고 쓰세요.
- evidence quote는 입력 evidence에서 온 문장만 사용하세요.
- confidence는 0과 1 사이 숫자입니다.

answer_ko:
{grounded.answer_ko}

evidence:
{json.dumps([item.model_dump() for item in grounded.evidence], ensure_ascii=False, indent=2)}

출력 JSON 필드:
topic, objective, method, result, limitations, evidence, confidence
""".strip()
    )
    accepted_evidence = filter_evidence_to_allowed(raw.get("evidence", []), grounded.evidence)
    if not accepted_evidence:
        return DocumentExtraction(
            topic="not specified",
            objective="not specified",
            method="not specified",
            result="not specified",
            limitations=["structured extraction did not return supported evidence"],
            evidence=[],
            confidence=0.2,
        )

    return DocumentExtraction(
        topic=raw["topic"],
        objective=raw["objective"],
        method=raw["method"],
        result=raw["result"],
        limitations=raw.get("limitations", []),
        evidence=accepted_evidence,
        confidence=raw["confidence"],
    )


def run_workflow(question: str) -> WorkflowAnswer:
    grounded = answer_question(question)
    facts = build_facts(grounded)
    return WorkflowAnswer(
        answer_ko=grounded.answer_ko,
        facts=facts,
        evidence=grounded.evidence,
        not_answered=grounded.not_answered,
        log=[
            "received question",
            "retrieved documents",
            "built structured facts",
            "validated WorkflowAnswer schema",
        ],
    )


def main() -> None:
    questions = [
        "API onboarding guide에는 무엇이 들어가야 해?",
        "pricing 정보는 어디에 있어?",
    ]
    for question in questions:
        result = run_workflow(question)
        print("\nQUESTION:", question)
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
