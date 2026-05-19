"""Deterministic LLM adapter stub for tests."""

from __future__ import annotations


def stub_adapter(agent_id: str, skill_id: str, inputs: dict) -> dict:
    return {
        "outputs": {"stub": True, "agent": agent_id, "skill": skill_id,
                    "echo": inputs},
        "confidence": 0.95,
        "touched_paths": [],
    }
