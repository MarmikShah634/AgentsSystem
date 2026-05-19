import json
from datetime import datetime, timezone

from orchestrator.core import logger as L


def test_save_and_load_plan(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "PLANS_DIR", tmp_path / "plans")
    plan = {"plan_id": "abc-123", "goal": "x", "steps": []}
    L.save_plan(plan)
    loaded = L.load_plan("abc-123")
    assert loaded == plan


def test_log_step_appends_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(L, "AUDIT_DIR", tmp_path / "audit")
    L.log_step(
        plan_id="p1", step_id="s1", agent="coder",
        skill="implement-function", inputs={"a": 1},
        outputs={"b": 2}, confidence=0.97, result="ok", duration_ms=12,
    )
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = tmp_path / "audit" / f"{day}.jsonl"
    record = json.loads(fp.read_text().splitlines()[-1])
    assert record["agent"] == "coder"
    assert record["confidence"] == 0.97
    assert record["inputs_sha256"] and record["outputs_sha256"]
