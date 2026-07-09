from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KOREAN_PARTICLES = (
    "해야",
    "하나",
    "한가",
    "하는",
    "에서는",
    "에게서",
    "으로서",
    "으로써",
    "부터",
    "까지",
    "에게",
    "에서",
    "으로",
    "라고",
    "처럼",
    "보다",
    "하고",
    "이며",
    "이고",
    "은",
    "는",
    "이",
    "가",
    "을",
    "를",
    "의",
    "에",
    "와",
    "과",
    "도",
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_percentage(text: str) -> dict:
    """Extract a simple percentage value from a short technical note."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*percent", text, flags=re.IGNORECASE)
    if not match:
        return {"value": None, "unit": "percent", "status": "not found"}
    return {"value": float(match.group(1)), "unit": "percent", "status": "ok"}


def strip_korean_particle(token: str) -> str:
    for particle in KOREAN_PARTICLES:
        if token.endswith(particle) and len(token) > len(particle) + 1:
            return token[: -len(particle)]
    return token


def keyword_tokens(text: str) -> set[str]:
    lower = text.lower()
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", lower)
        if len(token) > 1
    }
    for token in re.findall(r"[가-힣]+", lower):
        normalized = strip_korean_particle(token)
        if len(normalized) > 1:
            tokens.add(normalized)
    return tokens


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in keywords)
