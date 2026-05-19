"""Audit logger. Append-only JSONL under logs/audit/<date>.jsonl."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = ROOT / "logs" / "audit"
PLANS_DIR = ROOT / "logs" / "plans"


def _sha256(obj) -> str:
    blob = json.dumps(obj, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()


def log_step(
    *,
    plan_id: str,
    step_id: str,
    agent: str,
    skill: str,
    inputs: dict,
    outputs: dict,
    confidence: float,
    result: str,
    human_input: str | None = None,
    duration_ms: int = 0,
) -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "plan_id": plan_id,
        "step_id": step_id,
        "agent": agent,
        "skill": skill,
        "inputs_sha256": _sha256(inputs),
        "outputs_sha256": _sha256(outputs),
        "confidence": confidence,
        "result": result,
        "human_input": human_input,
        "duration_ms": duration_ms,
    }
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = AUDIT_DIR / f"{day}.jsonl"
    with fp.open("a") as fh:
        fh.write(json.dumps(record) + "\n")


def save_plan(plan: dict) -> Path:
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    pid = plan["plan_id"]
    fp = PLANS_DIR / f"{pid}.json"
    fp.write_text(json.dumps(plan, indent=2))
    return fp


def load_plan(plan_id: str) -> dict:
    fp = PLANS_DIR / f"{plan_id}.json"
    return json.loads(fp.read_text())
