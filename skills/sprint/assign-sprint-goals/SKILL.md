---
id: assign-sprint-goals
category: sprint
owner_agent: sprint-planner
inputs:
  - sprints: "array of {sprint_id, story_ids, total_points}"
outputs:
  - sprint_goals: "array of {sprint_id, goal} with one single-clause sentence per sprint"
  - rationale: "1-3 sentences explaining how goals were derived from story themes"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: assign-sprint-goals

## Purpose
Write one declarative sentence per sprint that names the shippable outcome end-of-sprint. The goal is the test for whether the sprint succeeded; vague goals hide failure.

## When to invoke
Invoke when `sprints` is finalized AND every sprint has its story_ids resolved with narratives accessible.
Do NOT invoke to: write release notes, define KPIs, or summarize backlog state.

## Procedure (follow exactly)
1. For each sprint, read every story's narrative.
2. Identify the dominant user-visible outcome (the one that, if shipped alone, would justify the sprint).
3. Draft a single-clause sentence: subject = the user or system, verb = the new capability, object = the artifact shipped. Present tense after sprint end ("Users can sign up with email and password.").
4. Reject any goal containing "and", "plus", semicolons, or multiple verbs — split intent is a failure mode.
5. Reject vague verbs: "make progress", "improve", "work on", "explore", "investigate".
6. Verify ≥70% of the sprint's points contribute directly to the stated goal; if not, rewrite or surface a finding.

## How to think
- Sprint contains two unrelated themes → the sprint was badly packed; flag and propose a smaller goal covering the larger theme.
- Goal would require "and" → split the sprint or pick the dominant theme; never compromise with conjunction.
- All stories are infrastructure → the goal still names a user-visible or operator-visible capability ("Operators can roll back deployments").
- Sprint exists only to unblock the next sprint → still name the concrete artifact ("Schema migrations run on staging without downtime").

## Required inputs
`sprints` with story narratives accessible. Missing narratives → STOP and ask for hydrated input.

## Output format
```json
{"sprint_goals":[
  {"sprint_id":"SP1","goal":"Users can sign up and verify their email."}],
 "rationale":"SP1's 4 stories all target the signup flow.",
 "confidence":0.0}
```

Note: the example above intentionally illustrates the forbidden "and" — in production output, that goal must be split or rewritten as "Users can complete email-verified signup."

## Quality criteria
Passes if: every sprint has exactly one goal; no goal contains "and"/";"/multi-clause structure; no vague verbs; ≥70% of points support the goal.
Fails if: multi-clause goal; vague verb; goal restates the sprint id; goal lists artifacts instead of outcomes.

## Common pitfalls
- Joining two themes with "and".
- Saying "Make progress on auth" — vague.
- Listing technologies ("Ship the Postgres migration") instead of outcomes.
- Hiding scope by under-specifying ("Improve onboarding").

## Examples
✅ "Users can complete email-verified signup." Single clause, user-visible, ties to ≥70% of sprint points.
❌ Anti-pattern: "Improve auth and start payments." — two clauses, vague verb, unfocused.

## Stop condition
Every sprint has exactly one single-clause goal; no banned verbs; ≥70% of points support the goal.

## Confidence guidance
Lower when: sprint contains mixed themes (≤0.75), stories lack user-visible outcomes (≤0.7), >40% of points are infra (≤0.8). ≥0.85 required.
