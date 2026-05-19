---
id: write-rollout-plan
category: tsd
owner_agent: tech-spec-author
inputs:
  - functional_requirements: "FRs from the PRD; needed to identify what is gated and what is migrated"
outputs:
  - section: "Markdown for the TSD Rollout Plan section (Flags, Canary, Kill switch, Compatibility)"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: write-rollout-plan

## Purpose
Specify exactly how the feature reaches production: which flags gate it, how traffic ramps, how to disable instantly, and how schema and API changes stay backwards-compatible. After this section, deploy and rollback are mechanical.

## When to invoke
Invoke as the final TSD section, after Observability. Do NOT invoke to: write deployment scripts, configure CI/CD, or describe long-term feature deprecation (use a separate sunset plan).

## Procedure (follow exactly)
1. **Feature flags**: list every flag with `name` (stable id), `scope` (`global`|`per-tenant`|`per-user`), `default` (`off`), and the FR it gates.
2. **Canary stages**: an ordered list, each with `percent_traffic`, `min_duration`, `abort_criteria` (metric thresholds tied to Observability metric names from the Observability Spec).
3. **Kill switch**: exact action that disables the feature globally in under 60 seconds. Name the flag or config key used. Document the rollback log message.
4. **Backwards compatibility**: for every data migration list `pre-deploy`, `deploy`, `post-deploy` steps; for every API change document the old shape's deprecation timeline. New columns nullable; renames go through dual-write.
5. Cross-link every abort_criterion to a metric defined in Observability.

## How to think
- If a flag has no kill criterion, it is not a kill switch — it is a wish.
- Canary stages must be monotonic in percent_traffic.
- Migration order matters: add columns before reading them, write to both before switching reads.
- Never delete columns in the same deploy that stops writing them.

## Required inputs
`functional_requirements` must be non-empty. Observability Spec must already define the metrics that abort_criteria reference; if not, STOP and write Observability first.

## Output format
Markdown starting with `## Rollout Plan`, with four subsections: `### Feature Flags`, `### Canary`, `### Kill Switch`, `### Backwards Compatibility`.

## Quality criteria
Passes if: every flag has default off and a gated FR; canary stages have ordered percents with metric-tied abort criteria; kill switch is concrete and fast; every migration step is sequenced.
Fails if: flags without kill criteria; vague "monitor and proceed"; missing rollback for any migration; metrics referenced that don't exist in Observability.

## Common pitfalls
- Defaulting a flag to `on` "because it's safe".
- Using engineer judgement as abort criterion instead of metrics.
- Bundling a rename and a delete into one migration.
- Forgetting to define a kill switch for risky changes.

## Examples
Good: flag `orders.new_pipeline` default off, canary 1%/10%/50%/100% with min_duration 30m and abort if `order_error_rate > 0.5%`; kill switch via LaunchDarkly key set to off; migration adds nullable `new_status` first, dual-write, then cutover.
Bad: "we'll ramp gradually"; no metric thresholds; migration drops and recreates table.

## Stop condition
Section exists with Flags/Canary/Kill Switch/Compatibility populated; every flag has a kill criterion; every migration has an ordered, rollback-safe plan; every abort_criterion references a real metric.

## Confidence guidance
Lower when: Observability metrics not finalized (≤0.7), data migration risk high (≤0.75), kill switch depends on infra that isn't in place (≤0.7), per-tenant flagging not supported by platform (≤0.75). Need ≥0.85.
