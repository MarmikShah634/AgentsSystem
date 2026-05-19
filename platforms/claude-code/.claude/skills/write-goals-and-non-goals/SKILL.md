---
id: write-goals-and-non-goals
category: prd
owner_agent: prd-author
inputs:
  - problem_statement: "markdown of the Problem Statement section already drafted"
outputs:
  - section: "markdown for the Goals & Non-Goals section with two bulleted lists"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-goals-and-non-goals

## Purpose
Emit the Goals and Non-Goals section: two bulleted lists that bound the release. Goals are the outcomes the release MUST achieve. Non-Goals are explicitly out-of-scope outcomes adjacent enough that reviewers might otherwise assume them in.

## When to invoke
Invoke as PRD section 3, after Problem Statement is drafted. Goals must be traceable to the problem's harm.

Do NOT invoke to: list features (goals are outcomes, not features), define metrics (use write-success-metrics), or enumerate non-functional constraints (use write-non-functional-requirements).

## Procedure (follow exactly)
1. Parse `problem_statement` to identify the harm.
2. Draft Goals:
   a. Each goal begins with a verb (Reduce, Enable, Increase, Eliminate).
   b. Each goal names an observable outcome tied to the harm.
   c. Avoid technology, UI, or feature names.
   d. 3–7 goals typical; fewer if scope is narrow.
3. Draft Non-Goals:
   a. Each non-goal is something a reviewer might reasonably assume IS in scope.
   b. Each non-goal includes a one-line rationale ("deferred to vNext", "covered by feature X", "not legal yet", "explicit founder decision").
   c. At least one non-goal is required; silence implies "anything goes".
4. Cross-check: no item appears in both lists; no non-goal contradicts a goal.

## How to think
- Goal looks like a feature ("ship the quiz scheduler") -> rewrite as outcome ("teachers can schedule weekly quizzes in one step").
- Non-goal feels obvious ("we won't build an OS") -> drop; only include genuinely adjacent items reviewers might assume.
- Goal lacks tie to harm -> drop or move to "nice to have" (which means: drop).
- Tempted to qualify a goal with metric numbers -> push numbers to success metrics; keep goals as outcomes.

## Required inputs
`problem_statement` markdown non-empty. If absent or empty, STOP and route back to write-problem-statement.

## Output format
{
  "section": "## Goals & Non-Goals\n\n### Goals\n- <verb>...\n\n### Non-Goals\n- <item> — <rationale>\n",
  "confidence": 0.0
}

## Quality criteria
Passes if: both subsections present and non-empty; every goal starts with a verb and is an outcome; every non-goal carries a rationale; no overlap; no contradictions with the problem statement.
Fails if: empty non-goals list; goals that are features or tech choices; non-goals without rationale; duplicated items.

## Common pitfalls
- Listing the product itself as a goal ("ship QuizLoop").
- Vague goals ("improve teacher experience").
- Non-goals that are silly or strawmen ("we won't build a spaceship").
- Drifting into metrics ("increase DAU by 20%") — those belong in metrics, not goals.

## Examples
Good:
## Goals & Non-Goals

### Goals
- Reduce teacher weekly grading time from ~4h to <30min.
- Enable teachers to schedule a recurring quiz in one action.
- Surface per-student mastery without manual spreadsheet work.

### Non-Goals
- Building a student-facing analytics dashboard — deferred to vNext.
- Supporting non-math subjects — covered by sibling product Math-only scope.
- Offering offline mode — district networks meet uptime SLA.

Bad:
### Goals
- Use React. (tech choice, not outcome)
- Make teachers happy. (not observable)

### Non-Goals
- We will not solve world hunger. (strawman)

## Stop condition
`### Goals` and `### Non-Goals` both populated under `## Goals & Non-Goals`; every goal observable, every non-goal has rationale; confidence reported.

## Confidence guidance
Lower confidence when:
- Problem statement harm was qualitative -> <= 0.75
- More than 7 candidate goals — likely scope creep -> <= 0.7
- Non-goals feel speculative without stakeholder grounding -> <= 0.75
- Any goal could be read as a feature rather than outcome -> <= 0.8
Confidence >= 0.85 is required to proceed without human review.
