---
id: dependency-audit
category: review
owner_agent: security
inputs:
  - manifest_path: "path to package.json|requirements.txt|Cargo.toml|go.mod|Gemfile|pom.xml"
  - lockfile_path: "optional path to corresponding lockfile"
  - severity_floor: "optional: low|moderate|high|critical (default: high)"
outputs:
  - findings: "list of {id, severity, path, package, version, fix, advisory_url}"
  - verdict: "pass | changes-requested | block"
  - tool_used: "npm|pip-audit|cargo|govulncheck|bundler-audit|maven|..."
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: dependency-audit

## Purpose
Run the stack's native CVE scanner against project manifests, emit a
normalised vulnerability list, and decide a verdict gated by severity.

## When to invoke
Plan step is `dependency-audit` OR a dependency manifest changed OR before
any `deploy-environment` to production. Run periodically per project policy.

## Procedure (follow exactly)
1. Detect ecosystem by manifest filename:
   - `package.json` / `package-lock.json` → `npm audit --json` (or `pnpm
     audit --json`, `yarn npm audit --json`).
   - `requirements.txt` / `pyproject.toml` / `poetry.lock` → `pip-audit -f
     json` or `poetry export | pip-audit -r -`.
   - `Cargo.toml` / `Cargo.lock` → `cargo audit --json`.
   - `go.mod` → `govulncheck -json ./...`.
   - `Gemfile.lock` → `bundler-audit check --update`.
   - `pom.xml` → `mvn org.owasp:dependency-check-maven:check`.
2. Run scoped to `manifest_path` directory; never run global scans.
3. Parse JSON output. Normalise each advisory to {id, severity, package,
   version, fix, advisory_url}.
4. Filter below `severity_floor` (default `high`).
5. Verdict: any `critical` → `block`. Any `high` with no `fix` available →
   `changes-requested`. Otherwise `pass`.

## How to think
- "fix available" means a patched version exists in the ecosystem registry,
  not just any newer version. Verify before recommending.
- Transitive vs direct: include both; mark `path` field as the dep chain.
- Yanked packages → severity `high` minimum.
- Dev-only dependencies → reduce severity one notch unless RCE.

## Required inputs
`manifest_path` exists and is readable. If `lockfile_path` is implied by
ecosystem and missing, STOP and ask — unlocked audits are unreliable.

## Output format
```json
{
  "findings": [
    {"id":"GHSA-7fhm-mqm4-2wp7","severity":"high","path":"axios>follow-redirects",
     "package":"follow-redirects","version":"1.15.3","fix":"1.15.4",
     "advisory_url":"https://github.com/advisories/GHSA-7fhm-mqm4-2wp7"}
  ],
  "verdict": "changes-requested",
  "tool_used": "npm",
  "confidence": 0.96
}
```

## Quality criteria
Pass: every finding has id+severity+package+version; tool_used recorded;
verdict matches severity distribution; transitive paths included.
Fail: missing advisory ids, fabricated CVE numbers, ignoring "no fix"
cases, scanning wrong directory.

## Common pitfalls
- Running `npm audit fix` automatically — out of scope for this skill.
- Reporting deprecation warnings as vulnerabilities.
- Failing silently when network is unavailable — must STOP and signal.
- Mixing dev and prod severities without marking which is which.

## Examples
✅ `pip-audit` reports `PYSEC-2024-48` in `requests<2.32.0`, fix `2.32.0`,
severity `high`, verdict `changes-requested`.
❌ Reporting `npm audit` warning about `low` severity prototype pollution
when severity_floor is `high` (should be filtered out).

## Stop condition
Tool exited successfully (or errored explicitly recorded); every finding
normalised; verdict set per severity policy.

## Confidence guidance
Native tool ran fresh against locked manifest ≥0.97; stale lockfile or no
lockfile ≤0.8 (escalate); partial output ≤0.6. Floor 0.95 — below it,
default to `changes-requested` and escalate.
