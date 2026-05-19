---
id: tune-motion-physics
category: design
owner_agent: designer
inputs:
  - target_path: "absolute path to a component, animation config, or motion-bearing stylesheet"
outputs:
  - findings: "array of {area, severity, path, line, msg, fix}"
  - verdict: "'pass' | 'revise'"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: tune-motion-physics

## Purpose
Audit animations against the taste-skill motion budget: only compositable properties, calibrated spring defaults, bounded durations, no rogue infinite loops, and full reduced-motion support.

## When to invoke
Invoke when `target_path` contains motion declarations (CSS transitions, keyframes, Framer Motion configs, GSAP timelines, etc.).
Do NOT invoke to: audit static layout (use evaluate-spacing-rhythm), interaction states (use enforce-interaction-states), or design tokens.

## Procedure (follow exactly)
1. Parse motion declarations. List each animation's target property, duration, easing, loop count, and reduced-motion handling.
2. Rule M1 — Animate only `transform` and `opacity`. Flag (severity=error) animations of `width`, `height`, `top`, `left`, `margin`, `padding`, `box-shadow`, `filter` (except justified hover-glow), `background-color` for large areas.
3. Rule M2 — Spring defaults `stiffness: 100, damping: 20`. Custom values without a comment justifying them → flag warn.
4. Rule M3 — UI transition durations between 150ms and 400ms inclusive. Outside → flag error. Page transitions may go to 600ms with justification.
5. Rule M4 — No `iteration-count: infinite` outside loading indicators. Flag error.
6. Rule M5 — Every animation has a `prefers-reduced-motion: reduce` fallback (zero or sub-100ms). Missing → flag error.
7. Each finding includes a concrete `fix` (e.g., "replace `height: auto` keyframe with `transform: scaleY(1)` + `transform-origin: top`").
8. `verdict = "pass"` iff zero error findings.

## How to think
- Animation animates `filter: blur` for a hero parallax → considered justified if scoped and brief; flag warn not error.
- Spring physics specified as a preset (e.g., Framer "gentle") → treat as custom; require a justification comment.
- Loading spinner with `animation: spin 1s infinite` → exempt from M4.
- Transition exists in CSS but is also overridden in JS → audit the runtime value.

## Required inputs
`target_path` non-empty and contains motion. No motion in file → STOP with note "no motion to audit".

## Output format
```json
{"findings":[
  {"area":"motion","severity":"error","path":"src/Drawer.tsx","line":58,
   "msg":"animates `width` from 0 to 320px (layout thrash).",
   "fix":"animate `transform: translateX(-100%) → 0` on a fixed-width container."}],
 "verdict":"revise","confidence":0.0}
```

## Quality criteria
Passes if: every motion declaration audited against M1-M5; flags include path+line+fix; verdict respects error presence.
Fails if: missed property in M1 list; allowed non-Fibonacci spring presets without justification; ignored reduced-motion; vague fix.

## Common pitfalls
- Allowing `height` animation because "it's just an accordion".
- Skipping M5 because the project doesn't have any reduced-motion testing.
- Treating `transition-all` as compliant — audit the resolved properties.
- Calling all springs "default" without checking the values.

## Examples
✅ Finding: error, line 58, msg "animates width (layout thrash)", fix "use translateX on fixed-width container".
❌ Anti-pattern: "motion feels janky" with no property names or fixes.

## Stop condition
Every motion declaration evaluated against M1-M5; findings carry path+line+fix; verdict matches.

## Confidence guidance
Lower when: motion library APIs not fully parsable (≤0.75), reduced-motion handling unverifiable from source (≤0.7), heavy GSAP timelines (≤0.8). ≥0.85 required.
