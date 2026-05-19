"""Structural integrity tests for SKILL.md and agent files.

These tests fail closed if anyone adds a new skill or agent that drops
back to the pre-refactor terse shape. The shape is the contract that
keeps the host LLM from hallucinating.
"""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"

# The infra/ category is deterministic Python; its SKILL.md files are
# documentation of handle() contracts, not LLM directives — they are
# intentionally terse.
INFRA_CATEGORY = "infra"

# Sections every LLM-facing SKILL.md must contain (case-sensitive headers).
SKILL_REQUIRED_SECTIONS = [
    "## Purpose",
    "## When to invoke",
    "## Procedure",
    "## How to think",
    "## Required inputs",
    "## Output format",
    "## Quality criteria",
    "## Common pitfalls",
    "## Examples",
    "## Stop condition",
    "## Confidence guidance",
]

# Sections every LLM agent spec must contain.
AGENT_REQUIRED_SECTIONS = [
    "## Role",
    "## When to invoke",
    "## Inputs consumed",
    "## Outputs produced",
    "## Skills owned",
    "## Hand-off rules",
    "## Authority and boundaries",
    "## Quality criteria",
    "## Common pitfalls",
    "## Examples",
    "## Confidence guidance",
]

# Hard cap from validate-system.sh.
MAX_SKILL_LINES = 400
MAX_AGENT_LINES = 400


def _llm_skill_files() -> list[pathlib.Path]:
    return [p for p in SKILLS.glob("**/SKILL.md")
            if p.relative_to(SKILLS).parts[0] != INFRA_CATEGORY]


def _llm_agent_files() -> list[pathlib.Path]:
    return [p for p in AGENTS.glob("*.md") if not p.name.startswith("infra-")]


def _has_heading(text: str, base_heading: str) -> bool:
    """Match `## Heading` or `## Heading (anything)` as a line by itself."""
    base = base_heading.lstrip("# ").strip()
    pattern = re.compile(
        rf"^##\s+{re.escape(base)}(\s*\(.*?\))?\s*$", re.MULTILINE,
    )
    return bool(pattern.search(text))


def test_every_llm_skill_has_required_sections():
    """Every non-infra SKILL.md exposes the full directive shape."""
    missing: list[str] = []
    for f in _llm_skill_files():
        text = f.read_text()
        for section in SKILL_REQUIRED_SECTIONS:
            if not _has_heading(text, section):
                missing.append(f"{f.relative_to(ROOT)}: missing '{section}'")
    assert not missing, "Skills missing required sections:\n  " + "\n  ".join(missing)


def test_every_llm_agent_has_required_sections():
    """Every non-infra agent spec exposes the full role-spec shape."""
    missing: list[str] = []
    for f in _llm_agent_files():
        text = f.read_text()
        for section in AGENT_REQUIRED_SECTIONS:
            if not _has_heading(text, section):
                missing.append(f"{f.relative_to(ROOT)}: missing '{section}'")
    assert not missing, "Agents missing required sections:\n  " + "\n  ".join(missing)


def test_skill_files_under_line_cap():
    over = [(f, len(f.read_text().splitlines()))
            for f in SKILLS.glob("**/SKILL.md")]
    over = [(f, n) for f, n in over if n > MAX_SKILL_LINES]
    assert not over, "SKILL.md files exceed cap:\n  " + "\n  ".join(
        f"{f.relative_to(ROOT)}: {n} lines" for f, n in over)


def test_agent_files_under_line_cap():
    over = [(f, len(f.read_text().splitlines()))
            for f in AGENTS.glob("*.md")]
    over = [(f, n) for f, n in over if n > MAX_AGENT_LINES]
    assert not over, "Agent files exceed cap:\n  " + "\n  ".join(
        f"{f.relative_to(ROOT)}: {n} lines" for f, n in over)


def test_every_llm_skill_declares_confidence_floor():
    """The frontmatter must explicitly state confidence_floor."""
    missing: list[str] = []
    for f in _llm_skill_files():
        text = f.read_text()
        if not re.search(r"^confidence_floor:\s*0\.\d+\s*$", text,
                         re.MULTILINE):
            missing.append(str(f.relative_to(ROOT)))
    assert not missing, "Skills missing confidence_floor:\n  " + "\n  ".join(missing)


def test_no_llm_skill_uses_default_floor_below_0_85():
    """The 0.85 floor is the absolute minimum per SPEC.md §3."""
    bad: list[str] = []
    for f in _llm_skill_files():
        text = f.read_text()
        m = re.search(r"^confidence_floor:\s*(0\.\d+)\s*$", text,
                      re.MULTILINE)
        if m and float(m.group(1)) < 0.85:
            bad.append(f"{f.relative_to(ROOT)}: floor={m.group(1)}")
    assert not bad, "Skills below the 0.85 floor:\n  " + "\n  ".join(bad)
