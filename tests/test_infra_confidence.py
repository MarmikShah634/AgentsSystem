from orchestrator.infra import confidence


def test_passes_above_floor():
    d = confidence.evaluate(confidence=0.95)
    assert d.allowed and not d.needs_human


def test_blocks_below_floor():
    d = confidence.evaluate(confidence=0.80)
    assert not d.allowed and d.needs_human and "below floor" in d.reason


def test_sensitive_path_blocked_even_at_full_confidence():
    d = confidence.evaluate(confidence=1.0, touched_paths=["infra/main.tf"])
    assert not d.allowed and d.needs_human and "sensitive" in d.reason


def test_env_path_blocked():
    d = confidence.evaluate(confidence=1.0, touched_paths=["app/.env.prod"])
    assert not d.allowed and d.needs_human


def test_spec_docs_blocked_for_non_owners():
    for path in ["docs/prd/checkout.md", "docs/tsd/checkout.md",
                 "docs/sprints/2026-q1.md"]:
        d = confidence.evaluate(
            confidence=1.0, touched_paths=[path], actor_agent="backend",
        )
        assert not d.allowed, f"{path} should be sensitive for backend"
        assert d.needs_human


def test_owner_can_write_its_surface():
    """prd-author writing docs/prd/** must not escalate on the surface gate."""
    d = confidence.evaluate(
        confidence=0.95, touched_paths=["docs/prd/checkout.md"],
        actor_agent="prd-author",
    )
    assert d.allowed, f"owner write rejected: {d.reason}"


def test_owner_still_subject_to_confidence_floor():
    """Even the owner can't write their own surface at low confidence."""
    d = confidence.evaluate(
        confidence=0.50, touched_paths=["docs/prd/checkout.md"],
        actor_agent="prd-author",
    )
    assert not d.allowed and "below floor" in d.reason


def test_each_owner_isolated_to_its_surface():
    """prd-author owns docs/prd/** but NOT docs/tsd/**."""
    d = confidence.evaluate(
        confidence=1.0, touched_paths=["docs/tsd/checkout.md"],
        actor_agent="prd-author",
    )
    assert not d.allowed and "sensitive" in d.reason


def test_no_owner_for_secrets_means_always_blocked():
    for actor in ["prd-author", "backend", "deployer", None]:
        d = confidence.evaluate(
            confidence=1.0, touched_paths=["secrets/api.key"],
            actor_agent=actor,
        )
        assert not d.allowed, f"actor={actor} should be blocked from secrets"


def test_handle_skill_dispatch():
    out = confidence.handle("evaluate-confidence",
                            {"confidence": 0.92, "touched_paths": []})
    assert out["decision"]["allowed"] is True


def test_handle_passes_actor_agent_through():
    out = confidence.handle("evaluate-confidence", {
        "confidence": 0.95,
        "touched_paths": ["docs/prd/x.md"],
        "actor_agent": "prd-author",
    })
    assert out["decision"]["allowed"] is True


def test_handle_unknown_skill_raises():
    import pytest
    with pytest.raises(ValueError):
        confidence.handle("bogus", {})
