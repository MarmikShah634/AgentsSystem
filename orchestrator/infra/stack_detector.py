"""infra-stack-detector agent body."""

from __future__ import annotations

from pathlib import Path

SIGNALS = {
    "node":     ["package.json", "pnpm-lock.yaml", "yarn.lock"],
    "python":   ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
    "go":       ["go.mod"],
    "rust":     ["Cargo.toml"],
    "java":     ["pom.xml", "build.gradle", "build.gradle.kts"],
    "dotnet":   ["*.csproj", "*.sln"],
    "ruby":     ["Gemfile"],
    "php":      ["composer.json"],
    "elixir":   ["mix.exs"],
    "swift":    ["Package.swift"],
    "dart":     ["pubspec.yaml"],
    "kotlin":   ["build.gradle.kts"],
    "deno":     ["deno.json", "deno.jsonc"],
    "bun":      ["bun.lockb"],
    "docker":   ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    "terraform": ["*.tf"],
    "k8s":      ["**/kustomization.yaml", "**/helmfile.yaml"],
}


def detect(root: Path | str = ".") -> list[str]:
    root = Path(root)
    found: list[str] = []
    for name, patterns in SIGNALS.items():
        for pat in patterns:
            if any(root.glob(pat)):
                found.append(name)
                break
    return sorted(set(found))


def handle(skill: str, inputs: dict) -> dict:
    if skill == "detect-stack":
        return {"stacks": detect(inputs.get("root", "."))}
    raise ValueError(f"infra-stack-detector has no skill '{skill}'")
