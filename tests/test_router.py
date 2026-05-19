from orchestrator.core.planner import PlanStep, build_plan
from orchestrator.core.registry import Registry
from orchestrator.core.router import Router


def test_router_logs_ok_path():
    def adapter(agent, skill, inputs):
        return {"outputs": {"ok": True}, "confidence": 0.95,
                "touched_paths": []}

    reg = Registry().load()
    plan = build_plan(
        goal="t", owner_agent="planner",
        steps=[
            PlanStep("1", "coder", "implement-function", "coding",
                     {"f": 1}, ["patch"], [], "2"),
            PlanStep("2", "tester", "generate-unit-test", "testing",
                     {"t": 1}, ["test_file_path"], ["1"], None),
        ],
    )
    r = Router(reg, adapter)
    res = r.run_step(plan, plan["steps"][0])
    assert res.ok and res.confidence == 0.95


def test_router_escalates_below_floor():
    def low_adapter(agent, skill, inputs):
        return {"outputs": {}, "confidence": 0.50, "touched_paths": []}

    captured = {}

    def human(prompt):
        captured["prompt"] = prompt
        return "deny"

    reg = Registry().load()
    plan = build_plan(
        goal="t", owner_agent="planner",
        steps=[
            PlanStep("1", "coder", "implement-function", "coding",
                     {}, ["patch"], [], "2"),
            PlanStep("2", "tester", "generate-unit-test", "testing",
                     {}, ["test_file_path"], ["1"], None),
        ],
    )
    r = Router(reg, low_adapter, human_responder=human)
    res = r.run_step(plan, plan["steps"][0])
    assert not res.ok and res.escalated
    assert "below floor" in captured["prompt"]


def test_router_blocks_foreign_agent_skill_pair():
    def adapter(agent, skill, inputs):
        return {"outputs": {}, "confidence": 1.0, "touched_paths": []}

    reg = Registry().load()
    plan = build_plan(
        goal="t", owner_agent="planner",
        steps=[
            PlanStep("1", "coder", "implement-function", "coding",
                     {}, ["patch"], [], "2"),
            PlanStep("2", "tester", "generate-unit-test", "testing",
                     {}, ["test_file_path"], ["1"], None),
        ],
    )
    # Mutate the step to refer to the wrong owner agent.
    plan["steps"][0]["agent"] = "tester"
    r = Router(reg, adapter)
    res = r.run_step(plan, plan["steps"][0])
    assert not res.ok and "owned by agent" in (res.error or "")
