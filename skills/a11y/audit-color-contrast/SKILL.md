---
id: audit-color-contrast
category: a11y
owner_agent: accessibility-auditor
inputs:
  - target_path: "absolute path to the page, component, or design token file"
  - viewport: "optional viewport size; default 1280x800"
outputs:
  - findings: "list of {wcag, severity, path, msg, fix}"
  - verdict: "pass|block"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: audit-color-contrast

## Purpose
Audit `target_path` against WCAG 2.2 success criteria 1.4.3 (Contrast
Minimum) and 1.4.11 (Non-Text Contrast). Emit findings only — never
modify code. Anti-hallucination: every flagged pair must include the
two measured colour values and the computed ratio.

## When to invoke
Plan step requests accessibility audit AND the target renders text or
UI affordances AND design tokens or computed styles are inspectable.
Do NOT invoke for: server-rendered API responses, raw data files, or
images without overlaid text.

## Procedure (follow exactly)
1. Enumerate every text-on-background pair in the target. For
   components, resolve tokens (CSS vars, Tailwind classes, theme
   objects) to concrete hex/rgb.
2. Compute relative luminance per WCAG formula, then contrast ratio
   `(L1 + 0.05) / (L2 + 0.05)`.
3. Apply thresholds:
   - Body text (<18pt, <14pt-bold): ratio ≥ 4.5:1.
   - Large text (≥18pt or ≥14pt-bold): ratio ≥ 3:1.
   - UI components / graphical objects (icons, focus rings, form
     borders): ≥ 3:1 against adjacent colour.
4. For each failing pair emit a finding with `wcag` set to "1.4.3" or
   "1.4.11", severity `error`, the offending selector/component
   path, both colour values, the measured ratio, and a concrete fix.
5. Run every check — partial audit is not an audit. Even if the first
   token fails, continue.

## How to think
- Token resolves to `currentColor` → resolve via cascade; if
  ambiguous, lower confidence and flag.
- Gradient background → test the worst-case stop.
- Hover/focus states → audit each state separately.
- Disabled controls → WCAG exempts them; note but do not block.
- Text over image → require minimum overlay or text-shadow; flag if
  absent.

## Required inputs
`target_path` must resolve to inspectable markup or tokens.

## Output format
```json
{"findings": [
   {"wcag": "1.4.3", "severity": "error",
    "path": "components/Button.tsx > .primary",
    "msg": "Body text #777 on #eee = 2.6:1 (need 4.5:1)",
    "fix": "Darken text token to #595959 (4.6:1) or lighten bg."}],
 "verdict": "block", "confidence": 0.97}
```

## Quality criteria
Pass: every text-on-bg pair examined; every failing pair includes
both colours + ratio + fix; verdict `block` iff any severity=error.
Fail: missing colour values; ratios rounded misleadingly (always show
to 1 decimal); silently skipping states.

## Common pitfalls
- Comparing token name to token name instead of resolved colour.
- Ignoring opacity — alpha-blend against the parent bg first.
- Using sRGB hex with non-WCAG formula.
- Reporting "looks fine" without a number.

## Examples
Pass:
```html
<button class="bg-blue-700 text-white">Save</button>
<!-- #1d4ed8 on #ffffff = 8.6:1 ✅ -->
```
Fail:
```html
<button class="bg-gray-200 text-gray-400">Save</button>
<!-- #9ca3af on #e5e7eb = 1.9:1 ❌ → finding emitted -->
```

## Stop condition
All pairs inspected; findings emitted with ratios; verdict set; no
source files modified.

## Confidence guidance
Tokens fully resolved = 0.97; one indirection guessed ≤0.92;
gradient/image bg approximated ≤0.9; missing state coverage ≤0.85.
Must be ≥0.95 to emit.
