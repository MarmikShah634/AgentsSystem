# Architecture

## 1. Goals

- **End-to-end automation** of the software development lifecycle.
- **One responsibility per component** (skill, agent, hook).
- **Plan-driven execution** — no agent acts without a written plan.
- **Confidence-gated** — human-in-loop below 90% confidence or on sensitive
  surfaces.
- **Provable trail** — every action produces an audit log entry.
- **Portable** — same definitions drive Claude, Cursor, Antigravity, Codex.

## 2. Component Model

```
┌────────────────────────────────────────────────────────────┐
│                       Orchestrator                         │
│   ┌────────────┐  ┌────────┐  ┌──────────┐  ┌──────────┐   │
│   │  Planner   │→ │ Router │→ │Confidence│→ │  Logger  │   │
│   └────────────┘  └────────┘  └──────────┘  └──────────┘   │
│         │             │             │            │         │
└─────────┼─────────────┼─────────────┼────────────┼─────────┘
          ↓             ↓             ↓            ↓
    ┌─────────┐   ┌──────────┐   ┌────────┐  ┌─────────┐
    │ Agents  │   │  Skills  │   │ Hooks  │  │  Logs   │
    │ (roles) │   │ (tasks)  │   │ (life- │  │ (audit) │
    │         │   │          │   │ cycle) │  │         │
    └─────────┘   └──────────┘   └────────┘  └─────────┘
```

### 2.1 Orchestrator (thin coordinator)

The orchestrator itself is ~60 lines of real logic. It does **not** route,
log, gate, plan, or detect anything itself — those are owned by **infra
agents** under `orchestrator/infra/`. The orchestrator's only job is to
`invoke(agent_id, skill_id, inputs)` and wire the infra agents together
in the right order.

| Infra agent | Skills it owns | Python body |
|-------------|----------------|-------------|
| `infra-router` | `route-step` | `orchestrator/infra/router.py` |
| `infra-logger` | `log-step`, `save-plan`, `load-plan` | `orchestrator/infra/logger.py` |
| `infra-confidence` | `evaluate-confidence` | `orchestrator/infra/confidence.py` |
| `infra-stack-detector` | `detect-stack` | `orchestrator/infra/stack_detector.py` |
| `infra-registry` | `lookup-owner`, `list-agents`, `list-skills` | `orchestrator/infra/registry.py` |
| `infra-planner` | `build-plan`, `enforce-test-pairing`, `topological-order` | `orchestrator/infra/planner.py` |

Each infra agent is deterministic (no LLM). The orchestrator dispatches
to them through the same `invoke()` interface as LLM agents — only the
`agent_id.startswith("infra-")` check decides whether to call Python
directly vs. the LLM adapter.

### 2.2 Agents (roles)

Each agent is a markdown spec under `agents/` with YAML frontmatter:

```yaml
---
id: coder
role: "Implementation engineer"
owns:
  - skills/coding/*
hands_off_to:
  - tester
  - reviewer
confidence_floor: 0.90
sensitive_surfaces:
  - infra/**
  - secrets/**
---
```

Agents are **roles**, not workers. Each owns one stage of the lifecycle:

| Agent | Stage |
|-------|-------|
| `requirements` | Capture and validate user stories |
| `architect` | Tech stack + system design |
| `planner` | Decompose goals into ordered tasks |
| `designer` | UI/UX taste, polish, anti-slop, interaction states |
| `frontend` | Implement UI tier (components, pages, client) |
| `backend` | Implement server tier (endpoints, services, data) |
| `tester` | Generate + run tests (unit + Puppeteer) |
| `reviewer` | Code review (style, correctness) |
| `security` | Security scan, secret detection |
| `docs` | Docs, READMEs, changelogs |
| `devops` | Build, CI/CD, infra |
| `deployer` | Release to environments |

Plus the deterministic **infra agents** (`infra-router`, `infra-logger`,
`infra-confidence`, `infra-stack-detector`, `infra-registry`,
`infra-planner`) which back the orchestrator.

### 2.3 Skills (tasks)

A skill does **exactly one task**. Each lives in
`skills/<category>/<skill-name>/SKILL.md` with frontmatter:

```yaml
---
id: implement-function
category: coding
owner_agent: coder
inputs:
  - file_path
  - function_spec
outputs:
  - patch
requires_plan: true
emits_confidence: true
---
```

A skill can be invoked only via its owner agent. The orchestrator refuses to
route a skill to a non-owner.

### 2.4 Hooks

Hooks are small shell scripts under `hooks/` that fire at lifecycle moments.
They are wired into each platform via `scripts/sync-platforms.sh`.

| Hook | When |
|------|------|
| `pre-task-plan.sh` | Before any task — fails if no plan exists |
| `confidence-gate.sh` | After agent response — fails if confidence<0.90 |
| `post-task-log.sh` | After any task — appends an audit record |
| `post-edit-test.sh` | After code edit — ensures a test exists |
| `pre-commit-test.sh` | Before commit — runs the test suite |
| `pre-deploy-check.sh` | Before deploy — runs security + tests |

### 2.5 Commands

Slash commands in `commands/*.md` are human entry points: `/start-feature`,
`/start-bugfix`, `/ship-it`, `/status`. Each command kicks off a sequence in
the orchestrator.

## 3. Lifecycle Flow

```
1. Human: /start-feature "Add OAuth login"
2. Orchestrator → requirements agent → gather-user-stories skill
   → emits plan + confidence
3. Confidence gate: if <0.90 → ask human; else continue
4. Orchestrator → architect agent → select-tech-stack skill
5. Orchestrator → planner agent → decompose-task skill
   → emits ordered task list (each pairs implementation + test)
6. For each task:
   a. coder agent → implement-function skill
   b. tester agent → generate-unit-test skill
   c. tester agent → generate-puppeteer-test (if UI)
   d. tester agent → run-tests skill
   e. reviewer agent → code-review skill
   f. security agent → security-scan skill
7. docs agent → update-readme + changelog-entry
8. devops agent → build-artifact
9. deployer agent → deploy-environment (human-gated)
```

Each arrow logs to `logs/audit/`. Plans are persisted under `logs/plans/`.

## 4. Plan Schema

```json
{
  "plan_id": "uuid",
  "goal": "string",
  "created_at": "iso8601",
  "owner_agent": "agent-id",
  "steps": [
    {
      "step_id": "1",
      "agent": "coder",
      "skill": "implement-function",
      "inputs": {...},
      "expected_outputs": [...],
      "depends_on": [],
      "test_pair": "step_id_of_test"
    }
  ],
  "human_gates": ["step_id", ...]
}
```

## 5. Audit Log Schema

```json
{
  "ts": "iso8601",
  "plan_id": "uuid",
  "step_id": "1",
  "agent": "coder",
  "skill": "implement-function",
  "inputs_sha256": "...",
  "outputs_sha256": "...",
  "confidence": 0.93,
  "result": "ok|escalated|failed",
  "human_input": null,
  "duration_ms": 1234
}
```

## 6. Platform Adapters

Each platform has a different config shape — see `platforms/<tool>/README.md`.
The sync script reads `agents/`, `skills/`, `commands/`, `hooks/` and writes
into each `platforms/<tool>/` tree in that tool's native format. Users symlink
or copy the relevant `platforms/<tool>/` subtree into their repo.

## 7. Confidence Model

Each agent response **must** include a `confidence` field. The orchestrator
treats responses without `confidence` as `confidence = 0.0` (i.e. always
escalate). The default floor is `0.90`. The floor can be raised per-agent in
the agent's frontmatter.

Sensitive surfaces (`secrets/**`, `infra/**`, `migrations/**`, public API
schemas) are **always** human-gated regardless of confidence.

## 8. Test Pairing Invariant

The `infra-planner` agent's `enforce-test-pairing` skill refuses to emit a
plan where any `frontend/*` or `backend/*` step lacks a paired `testing/*`
step. The `post-edit-test.sh` hook enforces the same invariant at runtime:
edits without a corresponding test trigger an immediate test-generation
step before the next action.

## 9. Tech Agnosticism

The orchestrator never assumes language or framework. It uses:

- File extension + presence of `package.json`/`pyproject.toml`/`go.mod` etc to
  detect the stack.
- A detection map in `orchestrator/core/stack_detect.py`.
- Skills delegate language-specific work to the underlying agent runtime
  (Claude/Cursor/Antigravity/Codex), passing only structured prompts.
