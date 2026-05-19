---
id: write-non-functional-requirements
category: prd
owner_agent: prd-author
inputs:
  - functional_requirements
outputs:
  - section
requires_plan: true
emits_confidence: true
---

# Skill: write-non-functional-requirements

## Task

Numbered NFR-1, NFR-2, … covering at minimum:

- Performance (latency, throughput targets)
- Scalability (peak load assumption)
- Security & privacy (data classes, retention)
- Availability (SLO)
- Accessibility (WCAG level)
- Compliance (relevant regs)

Each NFR is a single measurable claim.

## Stop condition

All six categories appear; no claim uses subjective adjectives ("fast",
"secure", "scalable") without a number.
