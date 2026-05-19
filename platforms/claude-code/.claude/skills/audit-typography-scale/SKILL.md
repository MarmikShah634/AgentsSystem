---
id: audit-typography-scale
category: design
owner_agent: designer
inputs:
  - target_path: "absolute path to a component, page, or CSS file containing text styles"
outputs:
  - findings: "array of {area, severity, path, line, msg, fix}"
  - verdict: "'pass' | 'revise'"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: audit-typography-scale

## Purpose
Audit type system for readable measure, sufficient hierarchy via scale ratio, sanctioned font families, and proper line-height. Findings drive frontend fixes.

## When to invoke
Invoke when `target_path` contains text styles (component with typography, global CSS, theme tokens).
Do NOT invoke to: pick fonts from scratch (designer's prerogative), validate icon-only UI, or audit non-text styles.

## Procedure (follow exactly)
1. Parse the file. Locate every text style declaration (font-size, line-height, font-family).
2. For each body-copy block, compute measure (characters per line at intended width). Flag (severity=error) any block outside 65-75ch.
3. Compute the type scale ratio between adjacent steps in the scale. Flag (severity=error) any ratio < 1.25.
4. Inspect font-family declarations. If Inter appears as primary, flag (severity=error). Preferred families: Geist, Outfit, Cabinet Grotesk, Satoshi.
5. Count distinct families. If >2, flag (severity=error).
6. For each body style, line-height < 1.5 → flag warn. For display, line-height > 1.2 → flag warn.
7. Every finding includes path, line, and a concrete `fix`.
8. `verdict = "pass"` iff zero error findings.

## How to think
- Tailwind class `text-base` → resolve to actual rem/px before measuring.
- Measure varies with breakpoint → audit each breakpoint; flag the worst.
- Inter is loaded but unused → not a violation; only primary use counts.
- Three families incl. monospace for code → mono is exempt; count UI families only.

## Required inputs
`target_path` resolves and contains text styles. Empty or non-text file → STOP.

## Output format
```json
{"findings":[
  {"area":"type","severity":"error","path":"src/Article.tsx","line":18,
   "msg":"body measure 92ch exceeds 75ch limit.",
   "fix":"set max-width to `prose` (65ch) on `<article>` wrapper."}],
 "verdict":"revise","confidence":0.0}
```

## Quality criteria
Passes if: every body block measure-checked; scale ratio verified; Inter detected and flagged when primary; family count enforced; line-height rules checked; fixes concrete with path+line.
Fails if: skipped a rule; vague fix; counted mono fonts toward the 2-family cap; verdict pass with error findings present.

## Common pitfalls
- Measuring at default browser width without considering responsive layout.
- Letting Inter pass because "it looks fine".
- Permitting a flat 1.125 scale ("major second") — forbidden.
- Treating display line-height of 1.5 as acceptable.

## Examples
✅ Finding: error, line 22, msg "scale steps 16→18px ratio=1.125 < 1.25", fix "adopt 1.25 ratio: 16→20→25→31".
❌ Anti-pattern: "typography needs work" with no measurements, no specific lines, Inter unflagged.

## Stop condition
Every typography rule evaluated; findings cite path+line+fix; verdict matches error presence.

## Confidence guidance
Lower when: CSS-in-JS dynamic sizes (≤0.75), tokens resolved indirectly (≤0.8), responsive variants unknown (≤0.75). ≥0.85 required.
