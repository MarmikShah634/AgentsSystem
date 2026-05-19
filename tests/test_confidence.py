from orchestrator.core.confidence import evaluate


def test_passes_above_floor():
    d = evaluate(confidence=0.95)
    assert d.allowed and not d.needs_human


def test_blocks_below_floor():
    d = evaluate(confidence=0.80)
    assert not d.allowed and d.needs_human and "below floor" in d.reason


def test_sensitive_surface_always_human_gated():
    d = evaluate(confidence=0.99, touched_paths=["infra/main.tf"])
    assert not d.allowed and d.needs_human and "sensitive" in d.reason


def test_secret_path_blocked():
    d = evaluate(confidence=1.0, touched_paths=["app/.env.production"])
    assert not d.allowed and d.needs_human
