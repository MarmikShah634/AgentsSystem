---
id: deploy-environment
category: deploy
owner_agent: deployer
inputs:
  - artifact_path: "filesystem path or registry ref produced by build-artifact"
  - environment: "dev|staging|prod"
  - strategy: "rolling|blue-green|canary|recreate"
  - approval_token: "required for prod; opaque token issued by human"
outputs:
  - release_id: "id of the new release"
  - rollback_ref: "ref needed to roll this deploy back (prior release id)"
  - tool_used: "kubectl|helm|terraform|ecs|gcloud|fly|render|..."
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: deploy-environment

## Purpose
Promote a pre-built artifact to `environment` using a defined strategy.
Always emit a `rollback_ref` to the previous release. Prod is ALWAYS
human-gated.

## When to invoke
Plan step is `deploy` AND artifact exists AND (for prod) approval_token
present. Run after `build-artifact`, `security-scan`, `secret-scan`,
`dependency-audit` succeed.

## Procedure (follow exactly)
1. Verify `artifact_path` exists / is reachable. Compute or read its digest.
2. Verify `environment` matches a known deployment target in repo config
   (helm values, terraform workspace, etc.). Unknown → STOP.
3. For prod: require `approval_token`. Missing or expired → STOP.
4. Record current release id as `rollback_ref` BEFORE deploying:
   - kubectl → `kubectl rollout history deployment/<name> -o json`
   - helm → `helm history <release>`
   - ecs → `aws ecs describe-services` → current taskDefinition arn
   - fly → `flyctl releases`
5. Apply strategy:
   - rolling → tool default (e.g. `kubectl set image`, `helm upgrade`).
   - blue-green → spin new colour, smoke test, switch traffic.
   - canary → release to weighted subset; pause for metric window before
     completing (orchestrator/human decides completion).
   - recreate → only with explicit acknowledgement of downtime.
6. Wait for readiness:
   - kubectl → `kubectl rollout status` with bounded timeout.
   - helm → `--wait --timeout` flag.
7. Smoke-check health endpoint if defined (e.g. `/healthz` returns 200).
8. Emit `release_id` and `rollback_ref`.

## How to think
- Strategy not supported by target → STOP, do not silently downgrade.
- Mid-deploy failure → do NOT auto-rollback from this skill; signal
  failure with `release_id` partial and let `rollback` skill handle it.
- Pending migrations → confirm `run-migration` succeeded first; STOP if
  unknown.
- Config drift detected → flag in output, do not "fix" it here.

## Required inputs
All inputs non-empty for prod; `approval_token` optional for dev. If
strategy is `canary` ensure traffic-shifting infra exists (mesh, ingress).

## Output format
```json
{
  "release_id": "myapp-2026-05-19-1430",
  "rollback_ref": "myapp-2026-05-18-2210",
  "tool_used": "helm",
  "confidence": 0.97
}
```

## Quality criteria
Pass: rollback_ref captured before apply; readiness verified; health check
passed; release_id stable and unique; approval recorded for prod.
Fail: missing rollback_ref, skipping readiness wait, deploying to prod
without approval, swallowing tool errors.

## Common pitfalls
- Tagging an artifact at deploy time instead of using the built digest.
- Using `latest` tag in prod manifests — refuse and STOP.
- Forgetting to scale up canary fully or leaving it half-promoted.
- Confusing "deployment created" with "deployment healthy".

## Examples
✅ `helm upgrade myapp ./chart --set image.tag=1.4.0 --wait` →
release_id `myapp.v23`, rollback_ref `myapp.v22`.
❌ `kubectl apply -f manifest.yaml` returning success while pods are still
CrashLoopBackOff — readiness not verified.

## Stop condition
Release applied; readiness confirmed; health endpoint OK; release_id and
rollback_ref recorded; for prod, approval token logged.

## Confidence guidance
Dev rolling deploy succeeded ≥0.97; staging ≥0.95; prod requires
approval, readiness, and health-check all green to reach 0.95. Floor 0.95.
