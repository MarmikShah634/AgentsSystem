---
id: write-user-personas
category: prd
owner_agent: prd-author
inputs:
  - stakeholder_input: "free-form notes about user types, contexts, and constraints"
outputs:
  - section: "markdown for the User Personas section, one block per persona"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-user-personas

## Purpose
Describe each distinct user type the product serves. Persona blocks give downstream FR/NFR authors concrete constraints (device, expertise, context) so they don't invent generic "users".

## When to invoke
Invoke as PRD section 4, after Problem Statement and before Functional Requirements. Personas inform FRs and NFRs (e.g. accessibility, device class).

Do NOT invoke to: enumerate user stories (use gather-user-stories), define metrics (use write-success-metrics), or describe internal stakeholders (sponsors, ops) — they are not personas.

## Procedure (follow exactly)
1. Read `stakeholder_input`. Group user references by role.
2. For each distinct role, draft a block with four fields:
   a. Name — role label only (e.g. "K-8 math teacher"), never an invented person's name.
   b. Primary jobs-to-be-done — 1–3 bullets, each starting with a verb.
   c. Constraints — device, network, expertise, regulatory, time pressure. Be specific.
   d. Scenario — one short illustrative paragraph (2–4 sentences) showing the persona using the product in context.
3. Order personas by primacy (the one whose problem the release most directly solves first).
4. If a field has no support in stakeholder_input, mark it `unknown` and lower confidence; do NOT invent demographics.

## How to think
- Tempted to name the persona "Sarah, 34" -> stop; role labels only.
- Constraints feel generic ("uses a computer") -> push for specifics ("Chromebook in 1:1 classroom, district-managed, no admin rights").
- Multiple roles blended into one persona -> split them.
- A role appears in stakeholder_input but isn't served by the release -> mention briefly only if needed for non-goals; do not create a full persona.

## Required inputs
`stakeholder_input` non-empty. If missing or no user references appear, STOP and ask human.

## Output format
{
  "section": "## User Personas\n\n### <Role label>\n- Jobs-to-be-done:\n  - <verb> ...\n- Constraints: <device, context, expertise>\n- Scenario: <2-4 sentence vignette>\n",
  "confidence": 0.0
}

## Quality criteria
Passes if: >=1 persona; every persona has all four fields; constraints are specific; scenario is concrete; no invented demographics.
Fails if: persona named after a person; field marked "various" or "any"; scenarios drift into solution design; internal stakeholders included.

## Common pitfalls
- "Sarah is 34 and loves coffee" — demographic flavor not supported by input.
- Constraints listing every adjective ("busy, motivated, tech-savvy") without specifics.
- Scenario describing the product's features rather than the persona's day.
- Listing five personas to look thorough.

## Examples
Good:
## User Personas

### K-8 math teacher
- Jobs-to-be-done:
  - Assign weekly mastery checks aligned to state standards.
  - Identify students who need reteaching before the next unit.
- Constraints: District-managed Chromebook, intermittent classroom Wi-Fi, no install rights, ~10 min between classes.
- Scenario: During a 10-minute prep period, the teacher opens the tool, picks the standard for the week, schedules the quiz to push Monday morning, and closes the laptop. Tuesday morning she sees which students missed which sub-skill.

Bad:
### Teacher Sarah
- Jobs: uses our app. (no verbs, no JTBD)
- Constraints: busy. (generic)
- Scenario: Sarah loves QuizLoop. (marketing, not a day-in-the-life)

## Stop condition
At least one persona block under `## User Personas`; all four fields filled or explicitly `unknown`; confidence reported.

## Confidence guidance
Lower confidence when:
- Constraints are inferred not stated -> <= 0.75
- Only one user reference exists but you suspect multiple roles -> <= 0.7
- Scenario relies on assumptions about workflow -> <= 0.75
- Stakeholder input contradicts itself on user type -> <= 0.7
Confidence >= 0.85 is required to proceed without human review.
