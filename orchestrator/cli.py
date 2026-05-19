"""CLI entry point. Wraps the orchestrator with a tiny argparse interface.

Usage:
  python3 orchestrator/cli.py init
  python3 orchestrator/cli.py detect
  python3 orchestrator/cli.py list-agents
  python3 orchestrator/cli.py list-skills
  python3 orchestrator/cli.py validate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.registry import Registry
from .core.stack_detect import detect


def cmd_init(_args) -> int:
    root = Path.cwd()
    (root / "logs" / "audit").mkdir(parents=True, exist_ok=True)
    (root / "logs" / "plans").mkdir(parents=True, exist_ok=True)
    print(f"initialised logs/ under {root}")
    return 0


def cmd_detect(_args) -> int:
    print(json.dumps({"stacks": detect(Path.cwd())}, indent=2))
    return 0


def cmd_list_agents(_args) -> int:
    reg = Registry().load()
    for aid, agent in sorted(reg.agents.items()):
        print(f"{aid:<14} {agent.meta.get('role', '')}")
    return 0


def cmd_list_skills(_args) -> int:
    reg = Registry().load()
    for sid, skill in sorted(reg.skills.items()):
        print(f"{sid:<36} owner={skill.meta.get('owner_agent', '?')}")
    return 0


def cmd_validate(_args) -> int:
    reg = Registry().load()
    problems: list[str] = []
    for sid, skill in reg.skills.items():
        owner = skill.meta.get("owner_agent")
        if not owner:
            problems.append(f"skill '{sid}' has no owner_agent")
        elif owner not in reg.agents:
            problems.append(f"skill '{sid}' owner '{owner}' is unknown")
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1
    print(f"OK: {len(reg.agents)} agents, {len(reg.skills)} skills, "
          f"all ownership valid")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(func=cmd_init)
    sub.add_parser("detect").set_defaults(func=cmd_detect)
    sub.add_parser("list-agents").set_defaults(func=cmd_list_agents)
    sub.add_parser("list-skills").set_defaults(func=cmd_list_skills)
    sub.add_parser("validate").set_defaults(func=cmd_validate)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
