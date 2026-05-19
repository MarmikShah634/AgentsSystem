"""infra-planner agent body. Plan invariant enforcement."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from . import logger as logger_agent

IMPLEMENT_CATEGORIES = {"frontend", "backend"}
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


def enforce_test_pairing(steps: list[PlanStep]) -> None:
    by_id = {s.step_id: s for s in steps}
    for s in steps:
        if s.category in IMPLEMENT_CATEGORIES:
            if not s.test_pair:
                raise PlanInvariantError(
                    f"{s.category} step '{s.step_id}' has no paired test step"
                )
            pair = by_id.get(s.test_pair)
            if not pair or pair.category not in TESTING_CATEGORIES:
                raise PlanInvariantError(
                    f"step '{s.test_pair}' referenced as test pair for "
                    f"'{s.step_id}' is not a testing step"
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
        for d in s.depends_on:
            if d in by_id:
                visit(by_id[d], stack)
        stack.remove(s.step_id)
        visited.add(s.step_id)
        order.append(s)

    for s in steps:
        visit(s, set())
    return order


def build_plan(*, goal: str, owner_agent: str,
               steps: list[PlanStep]) -> dict:
    enforce_test_pairing(steps)
    plan = {
        "plan_id": str(uuid.uuid4()),
        "goal": goal,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "owner_agent": owner_agent,
        "steps": [
            {
                "step_id": s.step_id, "agent": s.agent, "skill": s.skill,
                "category": s.category, "inputs": s.inputs,
                "expected_outputs": s.expected_outputs,
                "depends_on": s.depends_on, "test_pair": s.test_pair,
                "human_gate": s.human_gate,
            }
            for s in steps
        ],
        "human_gates": [s.step_id for s in steps if s.human_gate],
    }
    logger_agent.save_plan(plan)
    return plan


def _coerce_steps(raw: list) -> list[PlanStep]:
    out: list[PlanStep] = []
    for s in raw:
        if isinstance(s, PlanStep):
            out.append(s)
        else:
            out.append(PlanStep(**s))
    return out


def handle(skill: str, inputs: dict) -> dict:
    if skill == "build-plan":
        plan = build_plan(
            goal=inputs["goal"], owner_agent=inputs["owner_agent"],
            steps=_coerce_steps(inputs["steps"]),
        )
        return {"plan": plan}
    if skill == "enforce-test-pairing":
        enforce_test_pairing(_coerce_steps(inputs["steps"]))
        return {}
    if skill == "topological-order":
        ordered = topological_order(_coerce_steps(inputs["steps"]))
        return {"ordered_steps": [s.__dict__ for s in ordered]}
    raise ValueError(f"infra-planner has no skill '{skill}'")
