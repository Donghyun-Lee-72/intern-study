from __future__ import annotations

from pathlib import Path

from section1_llm_api import live_llm_extract, load_notes


ROOT = Path(__file__).resolve().parent


def main() -> None:
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)
    for item in load_notes():
        validated = live_llm_extract(item["id"], item["text"])
        out_path = out_dir / f"{item['id']}.json"
        out_path.write_text(validated.model_dump_json(indent=2), encoding="utf-8")
        print(f"validated {item['id']} -> {out_path}")


if __name__ == "__main__":
    main()
