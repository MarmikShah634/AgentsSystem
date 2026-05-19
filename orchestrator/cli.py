"""CLI entry point.

Usage:
  python3 -m orchestrator.cli init
  python3 -m orchestrator.cli detect
  python3 -m orchestrator.cli list-agents
  python3 -m orchestrator.cli list-skills
  python3 -m orchestrator.cli validate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.orchestrator import Orchestrator


def _orc() -> Orchestrator:
    return Orchestrator(llm_adapter=lambda *_: {"outputs": {}, "confidence": 1.0})


def cmd_init(_args) -> int:
    root = Path.cwd()
    (root / "logs" / "audit").mkdir(parents=True, exist_ok=True)
    (root / "logs" / "plans").mkdir(parents=True, exist_ok=True)
    print(f"initialised logs/ under {root}")
    return 0


def cmd_detect(_args) -> int:
    res = _orc().invoke("infra-stack-detector", "detect-stack",
                        {"root": str(Path.cwd())})
    print(json.dumps(res, indent=2))
    return 0


def cmd_list_agents(_args) -> int:
    res = _orc().invoke("infra-registry", "list-agents", {})
    for a in sorted(res["agents"], key=lambda a: a["id"]):
        print(f"{a['id']:<22} [{a['kind']}] {a['role']}")
    return 0


def cmd_list_skills(_args) -> int:
    res = _orc().invoke("infra-registry", "list-skills", {})
    for s in sorted(res["skills"], key=lambda s: s["id"]):
        print(f"{s['id']:<32} owner={s['owner_agent']:<22} "
              f"category={s['category']}")
    return 0


def cmd_validate(_args) -> int:
    orc = _orc()
    agents = {a["id"] for a in orc.invoke("infra-registry", "list-agents", {})["agents"]}
    skills = orc.invoke("infra-registry", "list-skills", {})["skills"]
    problems: list[str] = []
    for s in skills:
        if not s["owner_agent"]:
            problems.append(f"skill '{s['id']}' has no owner_agent")
        elif s["owner_agent"] not in agents:
            problems.append(f"skill '{s['id']}' owner '{s['owner_agent']}' unknown")
    if problems:
        for p in problems:
            print(f"FAIL: {p}", file=sys.stderr)
        return 1
    print(f"OK: {len(agents)} agents, {len(skills)} skills, "
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
