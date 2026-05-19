"""Router: dispatches plan steps to the right agent/skill via the host runtime.

The router is intentionally a thin coordinator. It validates ownership, calls
the registered runtime adapter (Claude/Cursor/Antigravity/Codex), then funnels
the response through the confidence gate and logger.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from .confidence import GateDecision, evaluate, prompt_human
from .logger import log_step
from .registry import Registry

# A runtime adapter is any callable matching this contract:
#   adapter(agent_id, skill_id, inputs) -> {"outputs": {...},
#                                           "confidence": float,
#                                           "touched_paths": [str, ...]}
RuntimeAdapter = Callable[[str, str, dict], dict]


@dataclass
class StepResult:
    step_id: str
    ok: bool
    outputs: dict
    confidence: float
    escalated: bool
    error: str | None = None


class Router:
    def __init__(self, registry: Registry, adapter: RuntimeAdapter,
                 human_responder: Callable[[str], str] | None = None):
        self.registry = registry
        self.adapter = adapter
        self.human_responder = human_responder or (lambda prompt: "approve")

    def run_step(self, plan: dict, step: dict) -> StepResult:
        try:
            self.registry.assert_ownership(step["agent"], step["skill"])
        except PermissionError as e:
            log_step(
                plan_id=plan["plan_id"],
                step_id=step["step_id"],
                agent=step["agent"],
                skill=step["skill"],
                inputs=step["inputs"],
                outputs={},
                confidence=0.0,
                result="failed",
                human_input=None,
                duration_ms=0,
            )
            return StepResult(step["step_id"], False, {}, 0.0, False, str(e))

        if step.get("human_gate"):
            self.human_responder(
                f"[HUMAN GATE] step {step['step_id']} ({step['skill']}) is "
                f"flagged as human-gated. Approve?"
            )

        t0 = time.time()
        try:
            resp = self.adapter(step["agent"], step["skill"], step["inputs"])
        except Exception as e:
            log_step(
                plan_id=plan["plan_id"],
                step_id=step["step_id"],
                agent=step["agent"],
                skill=step["skill"],
                inputs=step["inputs"],
                outputs={},
                confidence=0.0,
                result="failed",
                duration_ms=int((time.time() - t0) * 1000),
            )
            return StepResult(step["step_id"], False, {}, 0.0, False, str(e))

        dur = int((time.time() - t0) * 1000)
        confidence = float(resp.get("confidence", 0.0))
        outputs = resp.get("outputs", {})
        touched = resp.get("touched_paths", [])

        decision: GateDecision = evaluate(
            confidence=confidence,
            touched_paths=touched,
        )

        escalated = False
        human_input = None
        if not decision.allowed:
            escalated = True
            human_input = self.human_responder(
                prompt_human(decision, {"step": step, "outputs": outputs})
            )
            if not human_input.strip().lower().startswith("approve"):
                log_step(
                    plan_id=plan["plan_id"],
                    step_id=step["step_id"],
                    agent=step["agent"],
                    skill=step["skill"],
                    inputs=step["inputs"],
                    outputs=outputs,
                    confidence=confidence,
                    result="escalated",
                    human_input=human_input,
                    duration_ms=dur,
                )
                return StepResult(step["step_id"], False, outputs,
                                  confidence, True, "denied by human")

        log_step(
            plan_id=plan["plan_id"],
            step_id=step["step_id"],
            agent=step["agent"],
            skill=step["skill"],
            inputs=step["inputs"],
            outputs=outputs,
            confidence=confidence,
            result="ok",
            human_input=human_input,
            duration_ms=dur,
        )
        return StepResult(step["step_id"], True, outputs, confidence,
                          escalated, None)
