"""infra-registry agent body."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = ROOT / "agents"
SKILLS_DIR = ROOT / "skills"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    if yaml is not None:
        return yaml.safe_load(raw) or {}
    out: dict = {}
    for line in raw.splitlines():
        if ":" in line and not line.lstrip().startswith("-"):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


@dataclass
class Agent:
    id: str
    path: Path
    meta: dict


@dataclass
class Skill:
    id: str
    path: Path
    meta: dict


@dataclass
class _Cache:
    agents: dict[str, Agent] = field(default_factory=dict)
    skills: dict[str, Skill] = field(default_factory=dict)


_CACHE: _Cache | None = None


def _load() -> _Cache:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    c = _Cache()
    for p in AGENTS_DIR.glob("*.md"):
        meta = _parse_frontmatter(p.read_text())
        aid = meta.get("id") or p.stem
        c.agents[aid] = Agent(id=aid, path=p, meta=meta)
    for p in SKILLS_DIR.glob("**/SKILL.md"):
        meta = _parse_frontmatter(p.read_text())
        sid = meta.get("id") or p.parent.name
        c.skills[sid] = Skill(id=sid, path=p, meta=meta)
    _CACHE = c
    return c


def reset_cache() -> None:
    global _CACHE
    _CACHE = None


def assert_ownership(agent_id: str, skill_id: str) -> None:
    sk = _load().skills.get(skill_id)
    if not sk:
        raise KeyError(f"unknown skill: {skill_id}")
    owner = sk.meta.get("owner_agent")
    if owner and owner != agent_id:
        raise PermissionError(
            f"skill '{skill_id}' is owned by agent '{owner}', not '{agent_id}'"
        )


def handle(skill: str, inputs: dict) -> dict:
    c = _load()
    if skill == "lookup-owner":
        sk = c.skills.get(inputs["skill"])
        return {"owner_agent": sk.meta.get("owner_agent") if sk else None}
    if skill == "list-agents":
        return {"agents": [
            {"id": a.id, "role": a.meta.get("role", ""),
             "kind": a.meta.get("kind", "llm")}
            for a in c.agents.values()
        ]}
    if skill == "list-skills":
        return {"skills": [
            {"id": s.id, "category": s.meta.get("category", ""),
             "owner_agent": s.meta.get("owner_agent", "")}
            for s in c.skills.values()
        ]}
    raise ValueError(f"infra-registry has no skill '{skill}'")
