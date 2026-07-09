from __future__ import annotations

import json
from pathlib import Path

from live_llm import call_json
from schema import Evidence, GroundedAnswer, filter_evidence_to_allowed
from tools import keyword_tokens, read_text


ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "data" / "corpus"


def load_corpus() -> list[dict]:
    docs = []
    for path in sorted(CORPUS.glob("*.txt")):
        docs.append({"source_id": path.stem, "text": read_text(path)})
    return docs


def score(query: str, text: str) -> int:
    return len(keyword_tokens(query) & keyword_tokens(text))


def retrieve(query: str, top_k: int = 2) -> list[dict]:
    ranked = sorted(
        load_corpus(),
        key=lambda doc: score(query, doc["text"]),
        reverse=True,
    )
    return [doc for doc in ranked[:top_k] if score(query, doc["text"]) > 0]


def build_evidence(docs: list[dict]) -> list[Evidence]:
    return [Evidence(source_id=doc["source_id"], quote=doc["text"].strip()) for doc in docs]


def live_grounded_answer(query: str, evidence: list[Evidence]) -> GroundedAnswer:
    raw = call_json(
        f"""
당신은 RAG 답변 생성기입니다.
질문과 검색된 evidence만 사용해 한국어로 답하세요.

규칙:
- evidence에 답이 없으면 not_answered를 true로 두고, answer_ko는 "제공된 문서에서 답을 찾을 수 없습니다."로 쓰세요.
- evidence에 없는 내용을 추측하지 마세요.
- evidence 배열에는 실제 사용한 source_id와 quote만 남기세요.
- source_ids는 evidence의 source_id 목록이어야 합니다.

질문:
{query}

evidence:
{json.dumps([item.model_dump() for item in evidence], ensure_ascii=False, indent=2)}

출력 JSON 필드:
answer_ko, evidence, source_ids, not_answered
""".strip()
    )
    accepted_evidence = filter_evidence_to_allowed(raw.get("evidence", []), evidence)
    not_answered = bool(raw.get("not_answered", False)) or not accepted_evidence
    if not_answered:
        return GroundedAnswer(
            answer_ko="제공된 문서에서 답을 찾을 수 없습니다.",
            evidence=[],
            source_ids=[],
            not_answered=True,
        )
    return GroundedAnswer(
        answer_ko=raw["answer_ko"],
        evidence=accepted_evidence,
        source_ids=[item.source_id for item in accepted_evidence],
        not_answered=False,
    )


def answer_question(query: str) -> GroundedAnswer:
    docs = retrieve(query)
    if not docs:
        return GroundedAnswer(
            answer_ko="제공된 문서에서 답을 찾을 수 없습니다.",
            not_answered=True,
        )
    evidence = build_evidence(docs)
    return live_grounded_answer(query, evidence)


def main() -> None:
    questions = [
        "support ticket triage는 어떤 fallback을 가져야 해?",
        "API onboarding guide에는 무엇이 들어가야 해?",
        "RAG 답변을 신뢰하기 전에 무엇을 확인해야 해?",
        "pricing 정보는 어디에 있어?",
    ]
    for question in questions:
        result = answer_question(question)
        print("\nQUESTION:", question)
        print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
