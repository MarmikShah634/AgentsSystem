import pytest

from orchestrator.infra import registry as R


def setup_function(_):
    R.reset_cache()


def test_lookup_owner_known_skill():
    out = R.handle("lookup-owner", {"skill": "implement-endpoint"})
    assert out["owner_agent"] == "backend"


def test_lookup_owner_unknown_returns_null():
    out = R.handle("lookup-owner", {"skill": "does-not-exist"})
    assert out["owner_agent"] is None


def test_list_agents_includes_split_coder():
    ids = {a["id"] for a in R.handle("list-agents", {})["agents"]}
    assert {"frontend", "backend", "designer"}.issubset(ids)
    assert "coder" not in ids


def test_list_agents_includes_spec_chain():
    ids = {a["id"] for a in R.handle("list-agents", {})["agents"]}
    assert {"prd-author", "prd-reviewer", "tech-spec-author",
            "tech-spec-reviewer", "sprint-planner",
            "sprint-reviewer"}.issubset(ids)


def test_list_agents_includes_auditors():
    ids = {a["id"] for a in R.handle("list-agents", {})["agents"]}
    assert {"accessibility-auditor", "performance-auditor"}.issubset(ids)


def test_list_skills_includes_design_and_infra():
    sids = {s["id"] for s in R.handle("list-skills", {})["skills"]}
    assert "detect-ai-slop-patterns" in sids
    assert "evaluate-confidence" in sids
    assert "scaffold-frontend" in sids
    assert "scaffold-backend" in sids


def test_infra_agents_registered():
    ids = {a["id"] for a in R.handle("list-agents", {})["agents"]}
    expected = {"infra-router", "infra-logger", "infra-confidence",
                "infra-stack-detector", "infra-registry", "infra-planner"}
    assert expected.issubset(ids)


def test_assert_ownership_rejects_foreign():
    with pytest.raises(PermissionError):
        R.assert_ownership("frontend", "implement-endpoint")


def test_unknown_skill_handle_raises():
    with pytest.raises(ValueError):
        R.handle("bogus", {})
