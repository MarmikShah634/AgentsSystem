"""infra-logger agent body. Audit trail + plan persistence."""

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


def log_step(record: dict) -> Path:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    full = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "inputs_sha256": _sha256(record.get("inputs", {})),
        "outputs_sha256": _sha256(record.get("outputs", {})),
        **{k: v for k, v in record.items() if k not in ("inputs", "outputs")},
    }
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = AUDIT_DIR / f"{day}.jsonl"
    with fp.open("a") as fh:
        fh.write(json.dumps(full) + "\n")
    return fp


def save_plan(plan: dict) -> Path:
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    fp = PLANS_DIR / f"{plan['plan_id']}.json"
    fp.write_text(json.dumps(plan, indent=2))
    return fp


def load_plan(plan_id: str) -> dict:
    return json.loads((PLANS_DIR / f"{plan_id}.json").read_text())


def handle(skill: str, inputs: dict) -> dict:
    if skill == "log-step":
        return {"written_path": str(log_step(inputs["record"]))}
    if skill == "save-plan":
        return {"path": str(save_plan(inputs["plan"]))}
    if skill == "load-plan":
        return {"plan": load_plan(inputs["plan_id"])}
    raise ValueError(f"infra-logger has no skill '{skill}'")
