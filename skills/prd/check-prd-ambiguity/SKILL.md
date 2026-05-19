---
id: check-prd-ambiguity
category: prd
owner_agent: prd-reviewer
inputs:
  - prd_path: "absolute path to the PRD file under docs/prd/"
outputs:
  - findings: "list of {section, kind: 'ambiguous', msg, fix} entries, one per offending phrase"
  - verdict: "'pass' if zero ambiguities else 'revise'"
  - readiness_score: "float in [0,1] for this dimension"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: check-prd-ambiguity

## Purpose
Scan the PRD for ambiguous quantifiers, weasel words, and pronouns lacking a referent. Each finding cites the exact phrase and a clarification question. Never rewrite the PRD.

## When to invoke
Invoke after completeness passes. Can run in parallel with check-prd-testability and check-prd-conflicts.

Do NOT invoke to: rewrite ambiguous text (review only), check section presence (use check-prd-completeness), or judge metric quality (use check-prd-metrics-quality).

## Procedure (follow exactly)
1. Read `prd_path`.
2. For each section, scan for these classes of ambiguity:
   a. Vague quantifiers: "some", "many", "few", "several", "various", "multiple" without a number.
   b. Weasel words: "appropriate", "reasonable", "suitable", "as needed", "where possible", "robust", "seamless".
   c. Open-ended enumerations: "etc.", "and so on", "and similar", "...".
   d. Unanchored pronouns: "it", "they", "this", "these", "that" without a clear antecedent in the same sentence or the immediately preceding sentence.
   e. Hedges that change meaning: "typically", "generally", "usually", "often" applied to requirements.
3. For each match, emit a finding with:
   - `section` — heading name where the phrase appears.
   - `kind` — `"ambiguous"`.
   - `msg` — the exact phrase quoted with surrounding 5-10 words for context.
   - `fix` — a one-sentence clarification question (not a rewrite), e.g. "How many is 'several' here — 2, 5, 20?"
4. Verdict `pass` iff zero findings; else `revise`.
5. `readiness_score` = 1.0 - 0.05 * count(findings), floor 0.0.

## How to think
- The same vague word appears 5 times in one paragraph -> emit 5 findings (one per occurrence) so authors fix them all.
- A pronoun whose referent is obvious from prior sentence -> NOT a finding.
- Quoted user research ("teachers said 'it should be easy'") -> NOT a finding; that's source data, not a requirement.
- "etc." inside an Open Questions list -> NOT a finding; the section's purpose is enumerating unknowns.
- NEVER rewrite. The fix is always a clarifying question.

## Required inputs
`prd_path` readable. If missing, STOP and ask human.

## Output format
{
  "findings": [
    {"section": "Functional Requirements", "kind": "ambiguous", "msg": "FR-2: 'support several integrations' — 'several' is vague.", "fix": "How many integrations — name each one or give a count."}
  ],
  "verdict": "pass|revise",
  "readiness_score": 0.0,
  "confidence": 0.0
}

## Quality criteria
Passes if: every section scanned; each finding quotes the exact phrase with context; fix is a clarifying question, not a rewrite; verdict and score consistent.
Fails if: findings omit the phrase quote; rewrites suggested; verdict inconsistent.

## Common pitfalls
- Flagging "it" when antecedent is plain.
- Skipping a section because it "looked clean".
- Misreading domain jargon as weasel words.
- Suggesting a concrete rewrite — the author owns rewrites.

## Examples
Good finding:
{"section": "User Personas", "kind": "ambiguous", "msg": "'teachers often use Chromebooks' — 'often' makes the constraint optional.", "fix": "Is Chromebook the required device, or one of N — list devices and frequency."}

Good finding:
{"section": "Non-Functional Requirements", "kind": "ambiguous", "msg": "'NFR-4: appropriate uptime SLO' — 'appropriate' is undefined.", "fix": "Specify the SLO percentage and measurement window."}

Bad finding:
{"section": "...", "kind": "ambiguous", "msg": "rewrote it to be clearer", "fix": "..."} (rewrites)

## Stop condition
Every section scanned; findings emitted for every offending phrase; verdict and readiness_score consistent; confidence reported.

## Confidence guidance
Lower confidence when:
- Domain jargon resembles weasel words but is precise within the field -> <= 0.9
- Pronoun antecedent is plausible but not certain -> <= 0.9
- The section's intent allows looser language (Open Questions) -> <= 0.9
- Many borderline matches require judgment -> <= 0.85
Confidence >= 0.95 is required to proceed without human review.
