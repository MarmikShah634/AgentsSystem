"""Stub runtime adapter used for local tests of the orchestrator.

Real adapters delegate to the host (Claude/Cursor/Antigravity/Codex) by
shelling out to the respective CLI; this stub returns a deterministic
high-confidence response so end-to-end orchestrator wiring can be tested
without an LLM in the loop.
"""

from __future__ import annotations


def stub_adapter(agent_id: str, skill_id: str, inputs: dict) -> dict:
    return {
        "outputs": {"stub": True, "agent": agent_id, "skill": skill_id,
                    "echo": inputs},
        "confidence": 0.95,
        "touched_paths": [],
    }
