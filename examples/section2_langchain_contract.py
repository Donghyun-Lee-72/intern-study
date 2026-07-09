from __future__ import annotations

import json

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from schema import DocumentExtraction, Evidence, filter_evidence_to_allowed
from live_llm import call_llm
from section1_llm_api import load_notes


def build_parser() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=DocumentExtraction)


def build_prompt(parser: PydanticOutputParser) -> PromptTemplate:
    return PromptTemplate(
        template=(
            "당신은 기술 문서를 읽는 개발 보조자입니다.\n"
            "문서에서 topic, objective, method, result, limitations, evidence, confidence를 추출하세요.\n"
            "문서에 없는 정보는 추측하지 말고 not specified로 쓰세요.\n\n"
            "evidence의 source_id는 반드시 입력 문서 ID인 {source_id}만 사용하세요.\n\n"
            "{format_instructions}\n\n"
            "문서:\n{note}"
        ),
        input_variables=["source_id", "note"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )


def live_model_response(prompt_text: str) -> str:
    return call_llm(
        prompt_text
        + "\n\nReturn only one valid JSON object that follows the schema. Do not use Markdown fences."
    )


def parse_supported_output(
    parser: PydanticOutputParser,
    model_text: str,
    *,
    source_id: str,
    source_text: str,
) -> DocumentExtraction:
    parsed = parser.parse(model_text)
    accepted_evidence = filter_evidence_to_allowed(
        parsed.evidence,
        [Evidence(source_id=source_id, quote=source_text)],
        default_source_id=source_id,
    )
    return DocumentExtraction(
        topic=parsed.topic,
        objective=parsed.objective,
        method=parsed.method,
        result=parsed.result,
        limitations=parsed.limitations,
        evidence=accepted_evidence,
        confidence=parsed.confidence,
    )


def main() -> None:
    parser = build_parser()
    prompt = build_prompt(parser)
    item = load_notes()[0]

    prompt_text = prompt.format(source_id=item["id"], note=item["text"])
    model_text = live_model_response(prompt_text)
    parsed = parse_supported_output(
        parser,
        model_text,
        source_id=item["id"],
        source_text=item["text"],
    )

    print("--- LANGCHAIN PROMPT PREVIEW ---")
    print(prompt_text[:700] + "...")
    print("--- LIVE MODEL TEXT ---")
    print(model_text)
    print("--- PARSED PYDANTIC OBJECT ---")
    print(json.dumps(parsed.model_dump(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
