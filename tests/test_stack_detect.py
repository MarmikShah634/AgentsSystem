from pathlib import Path

from orchestrator.core.stack_detect import detect


def test_detects_python(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    assert "python" in detect(tmp_path)


def test_detects_node(tmp_path: Path):
    (tmp_path / "package.json").write_text("{}")
    assert "node" in detect(tmp_path)


def test_detects_nothing(tmp_path: Path):
    assert detect(tmp_path) == []
