"""infra-router agent body. Deterministic dispatch + ownership check."""

from __future__ import annotations

from typing import Callable

from . import registry as registry_agent

# A runtime adapter for LLM agents:
#   adapter(agent_id, skill_id, inputs) ->
#     {"outputs": {...}, "confidence": float, "touched_paths": [str, ...]}
LLMAdapter = Callable[[str, str, dict], dict]


def route_step(step: dict, llm_adapter: LLMAdapter,
               infra_invoke: Callable[[str, str, dict], dict]) -> dict:
    registry_agent.assert_ownership(step["agent"], step["skill"])
    if step["agent"].startswith("infra-"):
        return infra_invoke(step["agent"], step["skill"], step["inputs"])
    return llm_adapter(step["agent"], step["skill"], step["inputs"])


def handle(skill: str, inputs: dict) -> dict:
    if skill == "route-step":
        return {"response": route_step(
            inputs["step"], inputs["llm_adapter"], inputs["infra_invoke"],
        )}
    raise ValueError(f"infra-router has no skill '{skill}'")
