---
id: write-executive-summary
category: prd
owner_agent: prd-author
inputs:
  - stakeholder_input: "free-form notes from PM/sponsor describing audience, value, and urgency"
outputs:
  - section: "markdown for the Executive Summary section of docs/prd/<slug>.md (single paragraph, <=120 words)"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-executive-summary

## Purpose
Draft the Executive Summary section of the PRD: one short paragraph that tells a busy reader what is being built, for whom, and why now. No goals, no metrics, no scope, no solution detail — strictly the elevator pitch.

## When to invoke
Invoke during PRD authoring once stakeholder input exists and personas + problem statement are at least drafted. Order in the PRD is fixed: Executive Summary is section 1.

Do NOT invoke to: list goals (use write-goals-and-non-goals), define metrics (use write-success-metrics), or describe users in depth (use write-user-personas).

## Procedure (follow exactly)
1. Read `stakeholder_input` end to end.
2. Identify three nouns: WHAT (the thing being built), WHO (primary audience), WHY-NOW (the catalyst or urgency).
3. If any of the three is missing or speculative, STOP and lower confidence; record the gap as a comment in the section (HTML comment) and do not invent.
4. Draft one paragraph in this shape:
   `<WHAT> is a <one-line descriptor> for <WHO>. It <one-line value>. We are building it now because <WHY-NOW>.`
5. Trim to <=120 words. Hard cap.
6. Remove any goals, metrics, scope, or implementation references.

## How to think
- WHY-NOW absent -> do not invent a market trend; flag and lower confidence.
- Audience too broad ("everyone") -> narrow using stakeholder_input or flag.
- Tempted to bullet -> resist; this section is exactly one paragraph.
- Tempted to mention tech -> remove; that belongs in the TSD.

## Required inputs
`stakeholder_input` must be a non-empty string. If missing, STOP and ask human.

## Output format
{
  "section": "## Executive Summary\n\n<paragraph>\n",
  "confidence": 0.0
}

## Quality criteria
Passes if: section starts with `## Executive Summary`; one paragraph; <=120 words; mentions WHAT, WHO, WHY-NOW; no bullets; no metrics; no tech.
Fails if: multi-paragraph; bullet list; >120 words; missing any of the three nouns without an explicit gap comment; mentions implementation choices.

## Common pitfalls
- Restating the problem statement verbatim.
- Sneaking goals in as "the summary".
- Vague audience ("users will love it").
- Marketing adjectives ("revolutionary", "best-in-class").

## Examples
Good:
## Executive Summary

QuizLoop is a weekly-quiz delivery tool for K-8 math teachers in 1:1 device classrooms. It lets a teacher schedule a quiz once and see class-average mastery the next morning, replacing the spreadsheet-and-paper workflow most teachers still use. We are building it now because the district's new mastery-based grading policy takes effect next school year.

Bad:
## Executive Summary

We will build a great app using React and Postgres that has many features including dashboards, notifications, and exports. Users love quizzes. The market is huge. (no WHO specifics, mentions tech, marketing tone, multiple sentences of fluff)

## Stop condition
One paragraph emitted under `## Executive Summary`; word count <=120; WHAT/WHO/WHY-NOW present or gaps explicitly commented; confidence reported.

## Confidence guidance
Lower confidence when:
- WHY-NOW is weak or assumed -> <= 0.7
- Audience is broader than stakeholder_input supports -> <= 0.7
- Stakeholder input is contradictory -> <= 0.65
- Word count had to be cut aggressively, losing nuance -> <= 0.8
Confidence >= 0.85 is required to proceed without human review.
