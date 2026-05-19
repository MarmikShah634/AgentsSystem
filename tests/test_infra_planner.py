import pytest

from orchestrator.infra import planner as P


def _impl(sid, cat="backend", deps=None, pair=None):
    return P.PlanStep(
        step_id=sid, agent=cat, skill=f"implement-{cat}",
        category=cat, inputs={}, expected_outputs=["patch"],
        depends_on=deps or [], test_pair=pair,
    )


def _test(sid, deps=None):
    return P.PlanStep(
        step_id=sid, agent="tester", skill="generate-unit-test",
        category="testing", inputs={}, expected_outputs=["test_file_path"],
        depends_on=deps or [], test_pair=None,
    )


def test_frontend_step_requires_test_pair():
    with pytest.raises(P.PlanInvariantError):
        P.build_plan(goal="g", owner_agent="planner",
                     steps=[_impl("1", cat="frontend")])


def test_backend_step_requires_test_pair():
    with pytest.raises(P.PlanInvariantError):
        P.build_plan(goal="g", owner_agent="planner",
                     steps=[_impl("1", cat="backend")])


def test_pair_must_point_to_testing_step():
    with pytest.raises(P.PlanInvariantError):
        P.build_plan(goal="g", owner_agent="planner",
                     steps=[_impl("1", pair="2"), _impl("2")])


def test_valid_pair_accepted():
    plan = P.build_plan(goal="g", owner_agent="planner",
                        steps=[_impl("1", pair="2"), _test("2", deps=["1"])])
    assert plan["plan_id"] and len(plan["steps"]) == 2


def test_cycle_detected():
    a = _impl("a", deps=["b"], pair="t")
    b = _impl("b", deps=["a"], pair="t")
    t = _test("t")
    with pytest.raises(P.PlanInvariantError):
        P.topological_order([a, b, t])


def test_handle_build_plan():
    out = P.handle("build-plan", {
        "goal": "g", "owner_agent": "planner",
        "steps": [_impl("1", pair="2").__dict__, _test("2", deps=["1"]).__dict__],
    })
    assert out["plan"]["plan_id"]
