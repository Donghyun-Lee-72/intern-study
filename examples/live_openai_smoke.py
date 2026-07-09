from __future__ import annotations

import os

from dotenv import load_dotenv

from live_llm import configured_model, has_api_key


def main() -> None:
    load_dotenv()
    if not has_api_key():
        print("skipped_live_openai: set OPENAI_API_KEY to run")
        return

    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=configured_model(),
        input=(
            "Reply in one short Korean sentence. "
            "Say that the OpenAI live API connection is working."
        ),
    )
    print(response.output_text)


if __name__ == "__main__":
    main()
