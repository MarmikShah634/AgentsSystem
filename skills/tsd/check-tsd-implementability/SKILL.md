---
id: check-tsd-implementability
category: tsd
owner_agent: tech-spec-reviewer
inputs:
  - tsd_path: "Absolute path to the assembled TSD markdown"
outputs:
  - findings: "List of {section, kind: 'unimplementable', msg, fix} objects; never rewrites the TSD"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: check-tsd-implementability

## Purpose
For every component contract, determine whether a coding agent could implement it from the text alone, without consulting humans or guessing. Findings only — never edit the TSD.

## When to invoke
Invoke after `check-tsd-completeness`. Do NOT invoke to: judge whether the design is good (architectural review), or to estimate effort.

## Procedure (follow exactly)
1. Read the Component Contracts section.
2. For each component, check:
   a. Every method has a full typed signature (no unresolved `Any`, no missing return type).
   b. Every dependency names a component that exists elsewhere in the TSD.
   c. Every failure mode has a stable code AND a recovery rule.
   d. Every library or external API mentioned appears in the Overview or tech stack; flag any that don't.
   e. Invariants are checkable (testable predicates), not aspirational adjectives.
3. Cross-check Data Contracts: every entity referenced by a component has a JSON Schema; every entity in Data Contracts is reachable from some component.
4. Emit `{section, kind: "unimplementable", msg, fix}` per gap.
5. Do not propose redesigns. Suggest the minimum fix that closes the gap.

## How to think
- "Could a freshly-hired engineer implement this with no Slack access?" If no, flag.
- Adjectives like "robust", "scalable", "fast" are unimplementable until tied to a metric.
- Catch invented libraries: cross-check against `select-tech-stack` output.
- Unbounded recursion of dependencies is a red flag; flag it.

## Required inputs
`tsd_path` must point to a TSD that has at least Component Contracts and Data Contracts sections present.

## Output format
```
{"findings": [{"section": "Component Contracts", "kind": "unimplementable", "msg": "OrderService.place has no return type", "fix": "Declare return type as OrderId | OUT_OF_STOCK"}], "confidence": 0.0}
```

## Quality criteria
Passes if: every untyped signature flagged; every uncoded failure mode flagged; every uncited library flagged; every aspirational invariant flagged.
Fails if: false negatives on missing signatures; redesign suggestions; rewriting the TSD.

## Common pitfalls
- Letting `Any` through "because it's obvious".
- Accepting "should be reliable" as an invariant.
- Missing libraries imported via prose ("we'll use stripe-sdk") that don't appear in the tech stack.
- Reporting style nits instead of implementability gaps.

## Examples
Good: `{section: "Component Contracts", kind: "unimplementable", msg: "Worker.process_job uses redis but redis not in tech stack", fix: "Add redis to select-tech-stack output or replace with the chosen queue"}`.
Bad: `{msg: "I'd refactor this into two components"}` — that's a redesign, not implementability.

## Stop condition
A findings list exists naming every untyped signature, uncoded failure mode, uncited dependency, missing entity reference, and unmeasurable invariant; the TSD was not modified.

## Confidence guidance
Lower when: tech stack ambiguous (≤0.9), failure modes lack codes systemically (≤0.9), signatures use a non-standard syntax that's hard to parse (≤0.9). Required floor 0.95.
