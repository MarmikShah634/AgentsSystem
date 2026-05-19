"""Planner: turns a goal into a structured plan and enforces invariants.

The planner does NOT call an LLM directly here — that is delegated to the
host agent runtime (Claude/Cursor/Antigravity/Codex). This module:

  - normalises plans into the canonical schema
  - enforces the test-pairing invariant
  - assigns step ids, computes dependency order
  - persists the plan via logger.save_plan
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from .logger import save_plan

CODING_CATEGORIES = {"coding"}
TESTING_CATEGORIES = {"testing"}


@dataclass
class PlanStep:
    step_id: str
    agent: str
    skill: str
    category: str
    inputs: dict
    expected_outputs: list[str]
    depends_on: list[str]
    test_pair: str | None = None
    human_gate: bool = False


class PlanInvariantError(Exception):
    pass


def build_plan(*, goal: str, owner_agent: str, steps: list[PlanStep]) -> dict:
    enforce_test_pairing(steps)
    plan = {
        "plan_id": str(uuid.uuid4()),
        "goal": goal,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner_agent": owner_agent,
        "steps": [
            {
                "step_id": s.step_id,
                "agent": s.agent,
                "skill": s.skill,
                "category": s.category,
                "inputs": s.inputs,
                "expected_outputs": s.expected_outputs,
                "depends_on": s.depends_on,
                "test_pair": s.test_pair,
                "human_gate": s.human_gate,
            }
            for s in steps
        ],
        "human_gates": [s.step_id for s in steps if s.human_gate],
    }
    save_plan(plan)
    return plan


def enforce_test_pairing(steps: list[PlanStep]) -> None:
    """Every coding step must have a paired testing step."""
    step_index = {s.step_id: s for s in steps}
    for s in steps:
        if s.category in CODING_CATEGORIES:
            if not s.test_pair:
                raise PlanInvariantError(
                    f"coding step '{s.step_id}' has no paired test step"
                )
            pair = step_index.get(s.test_pair)
            if not pair or pair.category not in TESTING_CATEGORIES:
                raise PlanInvariantError(
                    f"step '{s.test_pair}' referenced as test pair "
                    f"for '{s.step_id}' is not a testing step"
                )


def topological_order(steps: list[PlanStep]) -> list[PlanStep]:
    by_id = {s.step_id: s for s in steps}
    visited: set[str] = set()
    order: list[PlanStep] = []

    def visit(s: PlanStep, stack: set[str]) -> None:
        if s.step_id in visited:
            return
        if s.step_id in stack:
            raise PlanInvariantError(f"cyclic dependency at '{s.step_id}'")
        stack.add(s.step_id)
        for dep in s.depends_on:
            if dep in by_id:
                visit(by_id[dep], stack)
        stack.remove(s.step_id)
        visited.add(s.step_id)
        order.append(s)

    for s in steps:
        visit(s, set())
    return order
