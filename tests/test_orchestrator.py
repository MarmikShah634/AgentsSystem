from orchestrator.core.orchestrator import Orchestrator
from orchestrator.infra import planner as P, registry as R


def setup_function(_):
    R.reset_cache()


def _plan():
    return P.build_plan(
        goal="t", owner_agent="planner",
        steps=[
            P.PlanStep("1", "backend", "implement-endpoint", "backend",
                       {"route": "/x"}, ["patch"], [], "2"),
            P.PlanStep("2", "tester", "generate-unit-test", "testing",
                       {}, ["test_file_path"], ["1"], None),
        ],
    )


def test_run_step_ok():
    def adapter(a, s, i):
        return {"outputs": {"ok": True}, "confidence": 0.95,
                "touched_paths": []}

    orc = Orchestrator(llm_adapter=adapter)
    plan = _plan()
    r = orc.run_step(plan, plan["steps"][0])
    assert r.ok and r.confidence == 0.95


def test_run_step_escalates_low_confidence():
    captured = {}

    def adapter(a, s, i):
        return {"outputs": {}, "confidence": 0.50, "touched_paths": []}

    def human(p):
        captured["prompt"] = p
        return "deny"

    orc = Orchestrator(llm_adapter=adapter, human_responder=human)
    plan = _plan()
    r = orc.run_step(plan, plan["steps"][0])
    assert not r.ok and r.escalated and "below floor" in captured["prompt"]


def test_run_step_blocks_foreign_agent_skill():
    def adapter(a, s, i):
        return {"outputs": {}, "confidence": 1.0, "touched_paths": []}

    orc = Orchestrator(llm_adapter=adapter)
    plan = _plan()
    plan["steps"][0]["agent"] = "frontend"  # wrong owner
    r = orc.run_step(plan, plan["steps"][0])
    assert not r.ok and "owned by agent" in (r.error or "")


def test_orchestrator_dispatches_to_infra_agents():
    orc = Orchestrator(llm_adapter=lambda *_: {"outputs": {}, "confidence": 1.0})
    out = orc.invoke("infra-registry", "list-agents", {})
    assert any(a["id"] == "designer" for a in out["agents"])
