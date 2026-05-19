"""Confidence gate. Enforces the >=0.90 floor and sensitive-surface gating."""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass

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
class GateDecision:
    allowed: bool
    reason: str
    needs_human: bool


def evaluate(
    *,
    confidence: float,
    touched_paths: list[str] | None = None,
    floor: float = DEFAULT_FLOOR,
    sensitive_globs: list[str] | None = None,
) -> GateDecision:
    globs = sensitive_globs or DEFAULT_SENSITIVE_GLOBS
    touched_paths = touched_paths or []

    for path in touched_paths:
        for g in globs:
            if fnmatch.fnmatch(path, g):
                return GateDecision(
                    allowed=False,
                    reason=f"sensitive surface touched: {path} (matches {g})",
                    needs_human=True,
                )

    if confidence < floor:
        return GateDecision(
            allowed=False,
            reason=f"confidence {confidence:.2f} below floor {floor:.2f}",
            needs_human=True,
        )

    return GateDecision(allowed=True, reason="ok", needs_human=False)


def prompt_human(decision: GateDecision, context: dict) -> str:
    """Render a prompt for the human. The actual capture is platform-specific."""
    return (
        f"[HUMAN GATE] {decision.reason}\n"
        f"Context: {context}\n"
        f"Type 'approve' to proceed, or supply guidance:"
    )
