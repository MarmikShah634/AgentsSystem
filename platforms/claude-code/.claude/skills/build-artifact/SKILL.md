---
id: build-artifact
category: deploy
owner_agent: devops
inputs:
  - target: "artifact kind: container|wheel|tarball|jar|binary|static"
  - repo_root: "absolute path to repository root"
  - version: "semver or build id to tag the artifact"
  - build_args: "optional map of build-time variables"
outputs:
  - artifact_path: "filesystem path or registry ref to produced artifact"
  - digest: "sha256 (or registry digest) of the artifact"
  - tool_used: "docker|buildah|poetry|pip|cargo|go|mvn|npm|..."
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: build-artifact

## Purpose
Run the project's native build to produce a single artifact of `target`
kind, tagged with `version`, and emit a verifiable digest.

## When to invoke
Plan step is `build` OR a deploy pipeline step requires a fresh artifact.
Run after `lint-check`, `code-review`, and `dependency-audit` succeed.

## Procedure (follow exactly)
1. Detect build tool by repo conventions and `target`:
   - container → `docker build -t <name>:<version> .` (or `buildah bud`).
   - wheel → `python -m build --wheel` or `poetry build -f wheel`.
   - tarball → `python -m build --sdist` or `npm pack`.
   - jar → `mvn package -DskipTests=false` or `gradle build`.
   - binary → `cargo build --release` / `go build -o ./bin/<name>`.
   - static → `npm run build` / `yarn build` / `pnpm build` per scripts.
2. Pass `build_args` through tool-native flags (e.g. `--build-arg`).
3. Verify artifact exists at expected path; compute sha256 (`sha256sum` or
   tool's own digest for registries).
4. Do NOT push to a registry from this skill; pushing is a separate deploy
   step. Container builds stay local unless pipeline policy says otherwise.
5. Surface tool warnings; fail loudly if exit code ≠ 0.

## How to think
- Reproducible build flags (e.g. `SOURCE_DATE_EPOCH`) — honour repo
  conventions; do not invent them.
- Multi-arch container → only if pipeline configures buildx; otherwise host
  arch only.
- Test step embedded in build (mvn) — let it run; do not skip without
  explicit override.
- Dirty git tree → record in metadata; do not block unless policy says so.

## Required inputs
`target`, `repo_root`, `version` non-empty. If build tool is missing, STOP
and signal toolchain gap.

## Output format
```json
{
  "artifact_path": "dist/myapp-1.4.0-py3-none-any.whl",
  "digest": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
  "tool_used": "poetry",
  "confidence": 0.94
}
```

## Quality criteria
Pass: artifact exists; digest matches file; version embedded in artifact
name; build exit code 0; touched_paths confined to build output dir.
Fail: missing digest, wrong version tag, leaving partial artifacts behind,
suppressing non-zero exit code.

## Common pitfalls
- Running `docker build` without `--pull` and silently using stale base
  image — pass `--pull` if pipeline policy requires fresh base.
- Building from dirty workdir without recording git sha.
- Re-tagging a stale artifact instead of rebuilding.
- Forgetting to clean `dist/` before sdist/wheel builds, mixing versions.

## Examples
✅ `docker build -t myapp:1.4.0 .` → digest
`sha256:abc…`, artifact_path `myapp:1.4.0`, tool_used `docker`.
❌ `artifact_path: "dist/myapp.whl"` with no version in filename, no digest.

## Stop condition
Build exited 0; artifact exists and is digestable; metadata recorded;
nothing outside expected build output modified.

## Confidence guidance
Standard build path, clean tree, exit 0 ≥0.95; dirty tree or warnings
≥0.85; unfamiliar toolchain ≤0.75. Floor 0.85.
