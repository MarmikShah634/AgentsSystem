---
id: security-scan
category: review
owner_agent: security
inputs:
  - patch
outputs:
  - findings
requires_plan: true
emits_confidence: true
---

# Skill: security-scan

## Task

Static analysis for OWASP Top 10 categories in the patch. Use the
project's native tool if present (semgrep, bandit, gosec, etc.); else
checklist-based review.
