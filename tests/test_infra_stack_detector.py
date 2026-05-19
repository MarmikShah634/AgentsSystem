from pathlib import Path

from orchestrator.infra import stack_detector as S


def test_detects_python(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    out = S.handle("detect-stack", {"root": str(tmp_path)})
    assert "python" in out["stacks"]


def test_detects_node(tmp_path: Path):
    (tmp_path / "package.json").write_text("{}")
    out = S.handle("detect-stack", {"root": str(tmp_path)})
    assert "node" in out["stacks"]


def test_detects_nothing(tmp_path: Path):
    assert S.handle("detect-stack", {"root": str(tmp_path)})["stacks"] == []
