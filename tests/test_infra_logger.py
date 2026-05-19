import json
from datetime import datetime, timezone

from orchestrator.infra import logger as L


def test_save_and_load_plan(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "PLANS_DIR", tmp_path / "plans")
    plan = {"plan_id": "abc-123", "goal": "x", "steps": []}
    L.handle("save-plan", {"plan": plan})
    out = L.handle("load-plan", {"plan_id": "abc-123"})
    assert out["plan"] == plan


def test_log_step_appends_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "AUDIT_DIR", tmp_path / "audit")
    L.handle("log-step", {"record": {
        "plan_id": "p1", "step_id": "s1", "agent": "backend",
        "skill": "implement-endpoint", "inputs": {"a": 1},
        "outputs": {"b": 2}, "confidence": 0.97, "result": "ok",
        "duration_ms": 12,
    }})
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = tmp_path / "audit" / f"{day}.jsonl"
    rec = json.loads(fp.read_text().splitlines()[-1])
    assert rec["agent"] == "backend"
    assert rec["confidence"] == 0.97
    assert rec["inputs_sha256"] and rec["outputs_sha256"]
