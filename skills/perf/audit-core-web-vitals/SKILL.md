---
id: audit-core-web-vitals
category: perf
owner_agent: performance-auditor
inputs:
  - puppeteer_run: "path to a Puppeteer run output containing web-vitals measurements"
  - budgets: "optional overrides; defaults below"
outputs:
  - findings: "list of {metric, measured, budget, severity, path, fix}"
  - verdict: "pass|block"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: audit-core-web-vitals

## Purpose
Compare measured Core Web Vitals from a Puppeteer run against budgets
and emit findings. Findings only. Anti-hallucination: every value
must come from the measurement source (web-vitals JS library,
Lighthouse JSON, or Performance API), never estimated.

## When to invoke
Plan step requests CWV audit AND a Puppeteer run captured LCP, INP,
CLS, TTFB on a representative URL under the project's standard
throttling profile.
Do NOT invoke for: localhost runs without throttling, runs missing
any of the four metrics, or runs against dev builds.

## Procedure (follow exactly)
1. Locate the measurements in `puppeteer_run`. Acceptable sources:
   - `web-vitals` library callbacks serialised to JSON.
   - Lighthouse report `audits.metrics.details.items[0]`.
   - PerformanceObserver entries from the page.
2. Default budgets (override via `budgets`):
   - LCP ≤ 2.5 s (good); 2.5–4 s (needs improvement); > 4 s (poor).
   - INP ≤ 200 ms; 200–500 (NI); > 500 (poor).
   - CLS ≤ 0.1; 0.1–0.25 (NI); > 0.25 (poor).
   - TTFB ≤ 800 ms; 800–1800 (NI); > 1800 (poor).
3. Severity mapping: good = no finding; needs-improvement =
   `warning`; poor = `error`.
4. For each metric not "good" emit a finding with: metric,
   measured (with units), budget, severity, path (URL audited), and
   a fix tied to the specific cause:
   - LCP poor → optimise hero image (`fetchpriority="high"`,
     preconnect, AVIF/WebP, server-side rendering).
   - INP poor → break up long tasks, defer non-critical JS, use
     scheduler.yield.
   - CLS poor → reserve space for media, avoid late-injected
     content, use `font-display: optional`.
   - TTFB poor → cache at edge, reduce server work, enable HTTP/2.
5. Always run all four checks even if the first fails.

## How to think
- Single-run variance can mislead — prefer median of ≥ 5 runs; if
  only one, lower confidence and note it.
- Throttling profile must be documented (CPU 4x, network Slow 4G is
  the standard reference). Without it, results are not comparable.
- INP requires user interactions; pure navigation traces will lack
  it — flag as "not measured" rather than passing.
- CLS is cumulative across the session window — confirm capture
  window matches definition.

## Required inputs
Run output contains LCP, INP, CLS, TTFB with numeric values and the
URL under test.

## Output format
```json
{"findings": [
   {"metric": "LCP", "measured": 3.4, "budget": 2.5,
    "severity": "warning", "path": "https://app.example.com/",
    "fix": "Preload hero image; add fetchpriority=high; serve AVIF."}],
 "verdict": "block", "confidence": 0.96}
```

## Quality criteria
Pass: all four metrics evaluated; values with units; budgets applied;
fixes specific to the metric and its likely cause; verdict matches
worst severity (any error → block).
Fail: missing a metric without flagging it; reporting CLS without a
decimal; suggesting generic "optimise" advice.

## Common pitfalls
- Comparing FCP to LCP budget.
- Treating warning as pass — verdict must reflect both.
- Reporting INP from a navigation-only run.
- Using mobile budgets against desktop run or vice versa.

## Examples
Pass: LCP 1.9 s, INP 120 ms, CLS 0.04, TTFB 410 ms → verdict `pass`.
Fail: LCP 4.6 s (poor), INP 220 ms (NI), CLS 0.32 (poor), TTFB 900 ms
(NI) → four findings, verdict `block`.

## Stop condition
All four metrics evaluated; findings emitted with fixes; verdict
set; no source modified.

## Confidence guidance
Multi-run median + throttling documented = 0.97; single run ≤0.92;
INP missing because no interaction ≤0.88; throttling unknown ≤0.85.
Must be ≥0.95 to emit.
