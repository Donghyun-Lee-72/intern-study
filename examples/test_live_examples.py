from __future__ import annotations

import os

from live_llm import has_api_key, usage_totals
from section1_llm_api import live_llm_extract, load_notes
from section2_langchain_contract import build_parser, build_prompt, live_model_response, parse_supported_output
from section3_langchain_rag import answer_question
from section4_workflow import run_workflow


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_live_section1_extraction() -> None:
    item = load_notes()[0]
    parsed = live_llm_extract(item["id"], item["text"])
    assert_true(parsed.evidence, "live extraction should keep evidence")
    assert_true(0 <= parsed.confidence <= 1, "confidence should be valid")
    assert_true(parsed.topic.strip(), "topic should not be empty")
    assert_true(parsed.objective.strip(), "objective should not be empty")
    assert_true(
        all(e.source_id == item["id"] for e in parsed.evidence),
        "live extraction should preserve the input source_id",
    )


def test_live_langchain_contract_parser() -> None:
    parser = build_parser()
    prompt = build_prompt(parser)
    item = load_notes()[0]
    model_text = live_model_response(prompt.format(source_id=item["id"], note=item["text"]))
    parsed = parse_supported_output(
        parser,
        model_text,
        source_id=item["id"],
        source_text=item["text"],
    )
    assert_true(parsed.evidence, "LangChain parser should keep evidence")
    assert_true(0 <= parsed.confidence <= 1, "parsed confidence should be valid")
    assert_true(
        all(e.source_id == item["id"] for e in parsed.evidence),
        "LangChain parser should preserve the input source_id",
    )
    assert_true(
        all(e.quote in item["text"] or item["text"] in e.quote for e in parsed.evidence),
        "LangChain parser should preserve quotes from the input text",
    )


def test_live_rag_answer() -> None:
    api = answer_question("API onboarding guide에는 무엇이 들어가야 해?")
    assert_true(not api.not_answered, "API onboarding query should be answered")
    assert_true(api.evidence, "API onboarding answer should cite evidence")
    assert_true(
        "doc_002_api_onboarding" in api.source_ids,
        "API query should use onboarding source",
    )
    answer = api.answer_ko.lower()
    expected_cues = [
        ("authentication", "인증"),
        ("environment", "환경"),
        ("rate", "레이트", "속도 제한"),
        ("smoke", "연결 테스트"),
    ]
    assert_true(
        sum(any(cue in answer for cue in group) for group in expected_cues) >= 3,
        "API onboarding answer should mention the representative corpus facts",
    )


def test_live_workflow_not_answered_policy() -> None:
    pricing = run_workflow("pricing 정보는 어디에 있어?")
    assert_true(pricing.not_answered, "pricing should not be answered from this corpus")
    assert_true(pricing.facts.confidence < 0.5, "not answered case should have low confidence")


def main() -> None:
    if os.getenv("RUN_LIVE_OPENAI_TESTS") != "1":
        print("skipped_live_tests: set RUN_LIVE_OPENAI_TESTS=1 to run paid API checks")
        return
    if not has_api_key():
        print("skipped_live_tests: OPENAI_API_KEY is not set")
        return

    test_live_section1_extraction()
    test_live_langchain_contract_parser()
    test_live_rag_answer()
    test_live_workflow_not_answered_policy()
    print("all_live_tests_passed")
    print("usage_totals", usage_totals())


if __name__ == "__main__":
    main()
