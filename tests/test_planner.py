import pytest

from orchestrator.core.planner import (
    PlanInvariantError,
    PlanStep,
    build_plan,
    topological_order,
)


def _coding_step(sid, deps=None, pair=None):
    return PlanStep(
        step_id=sid, agent="coder", skill="implement-function",
        category="coding", inputs={}, expected_outputs=["patch"],
        depends_on=deps or [], test_pair=pair,
    )


def _testing_step(sid, deps=None):
    return PlanStep(
        step_id=sid, agent="tester", skill="generate-unit-test",
        category="testing", inputs={}, expected_outputs=["test_file_path"],
        depends_on=deps or [], test_pair=None,
    )


def test_build_plan_requires_test_pair_for_coding():
    with pytest.raises(PlanInvariantError):
        build_plan(goal="g", owner_agent="planner",
                   steps=[_coding_step("1")])


def test_build_plan_rejects_pair_pointing_to_non_test():
    with pytest.raises(PlanInvariantError):
        build_plan(goal="g", owner_agent="planner",
                   steps=[_coding_step("1", pair="2"),
                          _coding_step("2")])


def test_build_plan_accepts_valid_pair():
    plan = build_plan(goal="g", owner_agent="planner",
                      steps=[_coding_step("1", pair="2"),
                             _testing_step("2", deps=["1"])])
    assert plan["plan_id"]
    assert len(plan["steps"]) == 2


def test_topological_order_detects_cycle():
    a = _coding_step("a", deps=["b"], pair="t")
    b = _coding_step("b", deps=["a"], pair="t")
    t = _testing_step("t")
    with pytest.raises(PlanInvariantError):
        topological_order([a, b, t])
