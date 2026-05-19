---
id: critique-ui-copy
category: design
owner_agent: designer
inputs:
  - target_path
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: critique-ui-copy

## Task

Apply STYLE.md / impeccable editorial rules to user-facing strings.

## Checklist

1. Open strong — the first sentence states a stance, not a setup.
2. Verbs-first action labels. Banned: "Click here", "Submit", "Learn more".
3. Banned hollow adjectives: "seamless", "robust", "elevate",
   "best-in-class", "powerful", "leverages", "delightful".
4. No em-dashes in product copy (taste convention).
5. Sentence case for buttons; Title Case only for proper nouns.
6. Error messages name the cause and the recovery, not the rule violated.

## Stop condition

Findings list every offending string with its `path`, `line`, and a
concrete rewrite.
