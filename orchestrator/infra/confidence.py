"""infra-confidence agent body.

Two gates:

1. **Confidence floor** — every agent response carries a `confidence` in
   [0, 1]. Below the floor (default 0.90) → escalate to human.
2. **Sensitive-surface gate** — certain paths require human approval
   regardless of confidence. Some surfaces are *owned* by a specific
   author agent (e.g. `prd-author` legitimately writes `docs/prd/**`).
   For those, the owner can write without escalation; any *other* agent
   touching the same path still escalates.
"""

from __future__ import annotations

import fnmatch
from dataclasses import asdict, dataclass

DEFAULT_FLOOR = 0.90

# All sensitive globs. Order matters for diagnostics only.
DEFAULT_SENSITIVE_GLOBS = [
    "secrets/**",
    "infra/**",
    "migrations/**",
    "**/.env*",
    "**/Dockerfile",
    "**/*.tf",
    "**/openapi.yaml",
    "**/openapi.yml",
    "docs/prd/**",
    "docs/tsd/**",
    "docs/sprints/**",
]

# Per-surface allow-list. Listed agents can write the surface without
# triggering the sensitive-surface gate (confidence floor still applies).
# Any glob NOT in this map has an empty allow-list, i.e. always escalates.
DEFAULT_OWNERSHIP: dict[str, set[str]] = {
    "docs/prd/**":     {"prd-author"},
    "docs/tsd/**":     {"tech-spec-author"},
    "docs/sprints/**": {"sprint-planner"},
    "migrations/**":   {"backend"},   # via implement-migration; still human-gated by agent floor
}


@dataclass
class Decision:
    allowed: bool
    reason: str
    needs_human: bool


def evaluate(*, confidence: float,
             touched_paths: list[str] | None = None,
             actor_agent: str | None = None,
             floor: float = DEFAULT_FLOOR,
             sensitive_globs: list[str] | None = None,
             ownership: dict[str, set[str]] | None = None) -> Decision:
    globs = sensitive_globs or DEFAULT_SENSITIVE_GLOBS
    owns = ownership if ownership is not None else DEFAULT_OWNERSHIP

    for p in touched_paths or []:
        for g in globs:
            if not fnmatch.fnmatch(p, g):
                continue
            allowed_actors = owns.get(g, set())
            if actor_agent and actor_agent in allowed_actors:
                # Owner of this surface — fall through to confidence check.
                break
            return Decision(
                False,
                f"sensitive surface touched: {p} (matches {g}, "
                f"actor={actor_agent or '?'})",
                True,
            )

    if confidence < floor:
        return Decision(False, f"confidence {confidence:.2f} below floor {floor:.2f}", True)
    return Decision(True, "ok", False)


def handle(skill: str, inputs: dict) -> dict:
    if skill == "evaluate-confidence":
        d = evaluate(
            confidence=float(inputs.get("confidence", 0.0)),
            touched_paths=inputs.get("touched_paths", []),
            actor_agent=inputs.get("actor_agent"),
            floor=float(inputs.get("floor", DEFAULT_FLOOR)),
        )
        return {"decision": asdict(d)}
    raise ValueError(f"infra-confidence has no skill '{skill}'")
