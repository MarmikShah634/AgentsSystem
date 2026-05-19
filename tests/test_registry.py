import pytest

from orchestrator.core.registry import Registry


@pytest.fixture(scope="module")
def reg():
    return Registry().load()


def test_all_agents_load(reg):
    expected = {
        "requirements", "architect", "planner", "coder", "tester",
        "reviewer", "security", "docs", "devops", "deployer",
    }
    assert expected.issubset(reg.agents.keys())


def test_every_skill_has_known_owner(reg):
    for sid, skill in reg.skills.items():
        owner = skill.meta.get("owner_agent")
        assert owner in reg.agents, f"skill {sid} owner '{owner}' not found"


def test_assert_ownership_rejects_foreign_agent(reg):
    # Pick any skill and confirm non-owner is rejected.
    sid, skill = next(iter(reg.skills.items()))
    foreign = next(a for a in reg.agents if a != skill.meta["owner_agent"])
    with pytest.raises(PermissionError):
        reg.assert_ownership(foreign, sid)
