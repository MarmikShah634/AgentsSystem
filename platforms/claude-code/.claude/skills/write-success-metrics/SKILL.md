---
id: write-success-metrics
category: prd
owner_agent: prd-author
inputs:
  - goals: "markdown of the Goals subsection (already drafted)"
outputs:
  - section: "markdown for the Success Metrics section, one or more metrics per goal"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-success-metrics

## Purpose
For each goal, declare 1–2 quantitative metrics with baseline, target, measurement window, and instrumentation source. Metrics turn outcomes into a contract you can verify post-launch.

## When to invoke
Invoke as PRD section 7, after Goals are drafted. Every metric must trace to exactly one goal.

Do NOT invoke to: write goals (use write-goals-and-non-goals), define NFR perf targets (those are SLOs in NFRs), or list out-of-scope items.

## Procedure (follow exactly)
1. Parse `goals` to a list.
2. For each goal, propose 1–2 metrics. Prefer rates and ratios over totals; vanity totals are forbidden.
3. For each metric, populate four fields:
   a. Baseline — current value with the date it was measured.
   b. Target — desired value with the window it must hold over.
   c. Window — measurement period (e.g. "rolling 30 days").
   d. Source — exact instrumentation source (event name, dashboard URL, SQL query name). Never "TBD".
4. If a baseline is unknown, write `Baseline: unknown (instrument first)` and lower confidence; do NOT invent numbers.
5. Format each metric under its parent goal using the canonical template.

## How to think
- Tempted to use a total ("signups") -> convert to a rate ("weekly active teachers / total teachers").
- Target with no window -> the metric is unfalsifiable; add a window.
- Source is generic ("analytics") -> name the event or query; "analytics" is not a source.
- Goal lacks an obvious metric -> push back; flag as open question rather than invent.
- One metric covers multiple goals -> attribute it to the primary goal; do not duplicate.

## Required inputs
`goals` non-empty markdown. If missing, STOP and route to write-goals-and-non-goals.

## Output format
{
  "section": "## Success Metrics\n\n- Goal: <goal>\n  - Metric: <name>\n  - Baseline: <value (date)>\n  - Target: <value>\n  - Window: <period>\n  - Source: <event / dashboard / query>\n",
  "confidence": 0.0
}

## Quality criteria
Passes if: every goal has >=1 metric; every metric has all four populated fields; no vanity totals; targets are numeric; sources are specific instruments.
Fails if: a goal has zero metrics; any field reads "TBD"; targets are qualitative; metric is a total without a denominator; baseline is fabricated.

## Common pitfalls
- "Increase engagement" with no definition.
- Targets without windows ("reach 1000 users") — by when, over what period?
- Baselines invented to look reasonable.
- Using DAU/MAU as a metric for a B2B teacher tool with weekly cadence.

## Examples
Good:
## Success Metrics

- Goal: Reduce teacher weekly grading time from ~4h to <30min.
  - Metric: Median self-reported weekly grading minutes per active teacher.
  - Baseline: 240 min (2026-04 survey, n=58).
  - Target: <=30 min.
  - Window: rolling 4 weeks.
  - Source: in-app weekly survey `teacher_time_survey_v1`.

Bad:
- Goal: Make teachers happy.
  - Metric: Happiness. (undefined)
  - Baseline: TBD. (invented gap)
  - Target: High. (qualitative)
  - Source: analytics. (generic)

## Stop condition
Every goal has at least one metric with all four fields concrete or explicitly flagged; section header is `## Success Metrics`; confidence reported.

## Confidence guidance
Lower confidence when:
- Any baseline is unknown / uninstrumented -> <= 0.7
- Source is a yet-to-be-built event -> <= 0.75
- Goal-to-metric link is indirect -> <= 0.7
- Target chosen without stakeholder sign-off -> <= 0.75
Confidence >= 0.85 is required to proceed without human review.
