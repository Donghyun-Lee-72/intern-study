from __future__ import annotations

from schema import DocumentExtraction
from tools import keyword_tokens
from section3_rag import retrieve
from section3_langchain_rag import load_documents, retrieve as langchain_retrieve, split_documents
from section4_workflow import run_workflow


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_keyword_tokens() -> None:
    tokens = keyword_tokens("API는 ticket-routing에서는 어떤 fallback이 필요하나?")
    assert_true("api" in tokens, "API should be searchable without Korean particle")
    assert_true("ticket-routing" in tokens, "hyphenated English terms should be preserved")
    assert_true("fallback" in tokens, "English terms should be preserved")
    assert_true("필요" in tokens, "Korean content words should be preserved")


def test_schema_requires_evidence_for_confident_claims() -> None:
    try:
        DocumentExtraction(
            topic="API onboarding",
            objective="teach API setup",
            method="not specified",
            result="not specified",
            limitations=[],
            evidence=[],
            confidence=0.8,
        )
    except ValueError:
        return
    raise AssertionError("confident extraction without evidence should fail validation")


def test_retrieve_expected_sources() -> None:
    api_docs = retrieve("API는 어떤 onboarding 정보를 포함해야 해?")
    assert_true(api_docs, "API onboarding query should retrieve a document")
    assert_true(
        api_docs[0]["source_id"] == "doc_002_api_onboarding",
        "API onboarding query should rank doc_002 first",
    )

    support_docs = retrieve("support ticket routing workflow에는 어떤 fallback이 필요해?")
    support_ids = [doc["source_id"] for doc in support_docs]
    assert_true(
        "doc_001_support_triage" in support_ids,
        "support fallback query should retrieve support triage source",
    )

    pricing_docs = retrieve("pricing 정책은 어디에 있어?")
    assert_true(not pricing_docs, "pricing query should not retrieve unsupported documents")


def test_langchain_retrieval_preserves_source_and_quote() -> None:
    chunks = split_documents(load_documents())
    retrieved = langchain_retrieve("RAG 답변을 신뢰하기 전에 무엇을 확인해야 해?", chunks)
    assert_true(retrieved, "RAG quality query should retrieve chunks")
    assert_true(
        retrieved[0].metadata["source_id"] == "doc_003_rag_quality",
        "RAG quality query should rank doc_003 first",
    )
    assert_true(
        "retrieved chunks" in retrieved[0].page_content,
        "retrieved chunk should contain the answer-bearing quote",
    )


def test_workflow_not_answered_without_api_call() -> None:
    result = run_workflow("pricing 정책은 어디에 있어?")
    assert_true(result.not_answered, "pricing should remain not_answered")
    assert_true(not result.evidence, "not_answered workflow should not keep evidence")
    assert_true(result.facts.confidence < 0.5, "not_answered facts should have low confidence")


def main() -> None:
    test_keyword_tokens()
    test_schema_requires_evidence_for_confident_claims()
    test_retrieve_expected_sources()
    test_langchain_retrieval_preserves_source_and_quote()
    test_workflow_not_answered_without_api_call()
    print("local_tests_passed")


if __name__ == "__main__":
    main()
