"""infra-confidence agent body."""

from __future__ import annotations

import fnmatch
from dataclasses import asdict, dataclass

DEFAULT_FLOOR = 0.90

DEFAULT_SENSITIVE_GLOBS = [
    "secrets/**",
    "infra/**",
    "migrations/**",
    "**/.env*",
    "**/Dockerfile",
    "**/*.tf",
    "**/openapi.yaml",
    "**/openapi.yml",
]


@dataclass
class Decision:
    allowed: bool
    reason: str
    needs_human: bool


def evaluate(*, confidence: float, touched_paths: list[str] | None = None,
             floor: float = DEFAULT_FLOOR,
             sensitive_globs: list[str] | None = None) -> Decision:
    globs = sensitive_globs or DEFAULT_SENSITIVE_GLOBS
    for p in touched_paths or []:
        for g in globs:
            if fnmatch.fnmatch(p, g):
                return Decision(False, f"sensitive surface touched: {p} (matches {g})", True)
    if confidence < floor:
        return Decision(False, f"confidence {confidence:.2f} below floor {floor:.2f}", True)
    return Decision(True, "ok", False)


def handle(skill: str, inputs: dict) -> dict:
    if skill == "evaluate-confidence":
        d = evaluate(
            confidence=float(inputs.get("confidence", 0.0)),
            touched_paths=inputs.get("touched_paths", []),
            floor=float(inputs.get("floor", DEFAULT_FLOOR)),
        )
        return {"decision": asdict(d)}
    raise ValueError(f"infra-confidence has no skill '{skill}'")
