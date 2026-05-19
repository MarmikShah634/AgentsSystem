"""Top-level orchestrator. Wires planner + router + registry + adapter."""

from __future__ import annotations

from typing import Callable

from .planner import PlanStep, build_plan, topological_order
from .registry import Registry
from .router import Router, RuntimeAdapter, StepResult


class Orchestrator:
    def __init__(self, adapter: RuntimeAdapter,
                 human_responder: Callable[[str], str] | None = None):
        self.registry = Registry().load()
        self.router = Router(self.registry, adapter, human_responder)

    def run_plan(self, *, goal: str, owner_agent: str,
                 steps: list[PlanStep]) -> list[StepResult]:
        plan = build_plan(goal=goal, owner_agent=owner_agent, steps=steps)
        ordered = topological_order(steps)
        results: list[StepResult] = []
        for step in ordered:
            plan_step = next(
                s for s in plan["steps"] if s["step_id"] == step.step_id
            )
            r = self.router.run_step(plan, plan_step)
            results.append(r)
            if not r.ok:
                break
        return results
