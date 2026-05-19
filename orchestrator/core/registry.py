"""Registry: discovers agents and skills from the source-of-truth folders."""

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
COMMANDS_DIR = ROOT / "commands"

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _parse_frontmatter(text: str) -> dict:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    raw = m.group(1)
    if yaml is not None:
        return yaml.safe_load(raw) or {}
    # Minimal fallback parser for environments without PyYAML.
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
    body: str


@dataclass
class Skill:
    id: str
    path: Path
    meta: dict
    body: str


@dataclass
class Registry:
    agents: dict[str, Agent] = field(default_factory=dict)
    skills: dict[str, Skill] = field(default_factory=dict)

    def load(self) -> "Registry":
        for p in AGENTS_DIR.glob("*.md"):
            text = p.read_text()
            meta = _parse_frontmatter(text)
            aid = meta.get("id") or p.stem
            self.agents[aid] = Agent(id=aid, path=p, meta=meta, body=text)
        for p in SKILLS_DIR.glob("**/SKILL.md"):
            text = p.read_text()
            meta = _parse_frontmatter(text)
            sid = meta.get("id") or p.parent.name
            self.skills[sid] = Skill(id=sid, path=p, meta=meta, body=text)
        return self

    def skill_owner(self, skill_id: str) -> str | None:
        sk = self.skills.get(skill_id)
        if not sk:
            return None
        return sk.meta.get("owner_agent")

    def assert_ownership(self, agent_id: str, skill_id: str) -> None:
        owner = self.skill_owner(skill_id)
        if owner and owner != agent_id:
            raise PermissionError(
                f"skill '{skill_id}' is owned by agent '{owner}', "
                f"not '{agent_id}'"
            )
