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


def test_handle_skill_dispatch():
    out = confidence.handle("evaluate-confidence",
                            {"confidence": 0.92, "touched_paths": []})
    assert out["decision"]["allowed"] is True


def test_handle_unknown_skill_raises():
    import pytest
    with pytest.raises(ValueError):
        confidence.handle("bogus", {})
