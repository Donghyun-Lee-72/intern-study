from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv


DEFAULT_MODEL = "gpt-5.4-mini"
MAX_OUTPUT_TOKENS = 700
USAGE_LOG: list[dict[str, int | str | None]] = []


def configured_model() -> str:
    load_dotenv()
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def has_api_key() -> bool:
    load_dotenv()
    return bool(os.getenv("OPENAI_API_KEY"))


def require_api_key() -> None:
    if not has_api_key():
        raise RuntimeError(
            "OPENAI_API_KEY is required. Copy .env.example to .env and set OPENAI_API_KEY. "
            f"Verified class default model is {DEFAULT_MODEL}; set OPENAI_MODEL to the provided low-cost model if needed."
        )


def call_llm(prompt: str) -> str:
    require_api_key()
    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=configured_model(),
        input=prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    usage = getattr(response, "usage", None)
    USAGE_LOG.append(
        {
            "model": configured_model(),
            "input_tokens": getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
    )
    return response.output_text.strip()


def usage_totals() -> dict[str, int]:
    input_tokens = sum(item["input_tokens"] or 0 for item in USAGE_LOG)
    output_tokens = sum(item["output_tokens"] or 0 for item in USAGE_LOG)
    total_tokens = sum(item["total_tokens"] or 0 for item in USAGE_LOG)
    return {
        "calls": len(USAGE_LOG),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        parsed = json.loads(text[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object from the model.")
    return parsed


def call_json(prompt: str, *, max_attempts: int = 2) -> dict[str, Any]:
    json_prompt = (
        f"{prompt}\n\n"
        "Return only one valid JSON object. Do not wrap it in Markdown fences."
    )
    last_error: Exception | None = None
    current_prompt = json_prompt
    for _ in range(max_attempts):
        text = call_llm(current_prompt)
        try:
            return parse_json_object(text)
        except (json.JSONDecodeError, ValueError) as error:
            last_error = error
            current_prompt = (
                f"{json_prompt}\n\n"
                "Your previous response was not a valid JSON object. "
                f"Validation error: {error}. Return only corrected JSON."
            )
    raise ValueError(f"Model did not return valid JSON after {max_attempts} attempts.") from last_error
