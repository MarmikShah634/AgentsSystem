"""Thin orchestrator. Coordinates infra agents; does no work itself.

Everything that used to live in this module — routing, logging, gating,
planning — is now an infra agent under `orchestrator/infra/`. The
orchestrator's only job is to invoke them in the right order.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from ..infra import (
    confidence as confidence_agent,
    logger as logger_agent,
    planner as planner_agent,
    registry as registry_agent,
    router as router_agent,
    stack_detector as stack_agent,
)

INFRA_AGENTS = {
    "infra-router": router_agent,
    "infra-logger": logger_agent,
    "infra-confidence": confidence_agent,
    "infra-stack-detector": stack_agent,
    "infra-registry": registry_agent,
    "infra-planner": planner_agent,
}


@dataclass
class StepResult:
    step_id: str
    ok: bool
    outputs: dict
    confidence: float
    escalated: bool
    error: str | None = None


class Orchestrator:
    """Thin coordinator. ~60 lines of real logic."""

    def __init__(self, llm_adapter: Callable[[str, str, dict], dict],
                 human_responder: Callable[[str], str] | None = None):
        self.llm_adapter = llm_adapter
        self.human_responder = human_responder or (lambda p: "approve")

    def invoke(self, agent_id: str, skill_id: str, inputs: dict) -> dict:
        if agent_id in INFRA_AGENTS:
            return INFRA_AGENTS[agent_id].handle(skill_id, inputs)
        return self.llm_adapter(agent_id, skill_id, inputs)

    def run_step(self, plan: dict, step: dict) -> StepResult:
        t0 = time.time()
        try:
            routed = self.invoke("infra-router", "route-step", {
                "step": step,
                "llm_adapter": self.llm_adapter,
                "infra_invoke": self.invoke,
            })
            resp = routed["response"]
        except Exception as e:
            self._log(plan, step, {}, 0.0, "failed",
                      duration_ms=int((time.time() - t0) * 1000))
            return StepResult(step["step_id"], False, {}, 0.0, False, str(e))

        confidence = float(resp.get("confidence", 1.0))
        outputs = resp.get("outputs", resp)
        touched = resp.get("touched_paths", [])
        dur = int((time.time() - t0) * 1000)

        gate = self.invoke("infra-confidence", "evaluate-confidence", {
            "confidence": confidence, "touched_paths": touched,
        })["decision"]

        escalated = False
        human_input = None
        if not gate["allowed"]:
            escalated = True
            human_input = self.human_responder(
                f"[HUMAN GATE] {gate['reason']}\nstep: {step['step_id']} "
                f"({step['skill']})\nApprove?"
            )
            if not human_input.strip().lower().startswith("approve"):
                self._log(plan, step, outputs, confidence, "escalated",
                          human_input=human_input, duration_ms=dur)
                return StepResult(step["step_id"], False, outputs,
                                  confidence, True, "denied by human")

        self._log(plan, step, outputs, confidence, "ok",
                  human_input=human_input, duration_ms=dur)
        return StepResult(step["step_id"], True, outputs, confidence,
                          escalated, None)

    def run_plan(self, plan: dict) -> list[StepResult]:
        results: list[StepResult] = []
        for step in plan["steps"]:
            r = self.run_step(plan, step)
            results.append(r)
            if not r.ok:
                break
        return results

    def _log(self, plan, step, outputs, confidence, result,
             human_input=None, duration_ms=0) -> None:
        self.invoke("infra-logger", "log-step", {
            "record": {
                "plan_id": plan["plan_id"], "step_id": step["step_id"],
                "agent": step["agent"], "skill": step["skill"],
                "inputs": step["inputs"], "outputs": outputs,
                "confidence": confidence, "result": result,
                "human_input": human_input, "duration_ms": duration_ms,
            }
        })
