---
id: audit-focus-management
category: a11y
owner_agent: accessibility-auditor
inputs:
  - target_path: "absolute path to page or component"
outputs:
  - findings: "list of {wcag, severity, path, msg, fix}"
  - verdict: "pass|block"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.95
---

# Skill: audit-focus-management

## Purpose
Validate visible focus styles, focus movement on open/close of
overlays, and absence of focus traps outside modals. WCAG 2.2 2.4.7
(Focus Visible) and 2.4.11 (Focus Not Obscured, Minimum). Findings
only.

## When to invoke
Plan step requests a11y audit AND target contains focusable elements
or overlay components (modal, drawer, popover, menu).
Do NOT invoke for: purely static text content.

## Procedure (follow exactly)
1. Visible focus indicator on every focusable element:
   - Minimum ≥ 2px outline OR equivalent (background change with
     ≥ 3:1 contrast against adjacent colour).
   - `outline: none` only allowed when paired with a custom focus
     style — flag the bare reset.
2. Focus movement on overlay open:
   - When a dialog/drawer opens, focus MUST move into it (typically
     to the first focusable element or the close button).
   - On close, focus MUST return to the element that triggered the
     open (the invoker).
3. Focus trap:
   - Within an open modal: Tab/Shift+Tab MUST cycle inside.
   - Outside modal contexts: NO trap allowed (no `tabindex` games
     that prevent leaving a section).
4. Focus not obscured (2.4.11): the focused element MUST be at least
   partially visible — flag sticky headers/footers that cover it.
5. `tabindex` rules: only `0` or `-1`; positive values are a
   finding.

## How to think
- CSS `:focus-visible` is preferred over `:focus` — but lacking
  `:focus-visible` is not itself a failure if `:focus` is styled.
- Programmatic `element.focus()` in a `useEffect` is the canonical
  React pattern for overlay focus.
- Returning focus on close requires storing the invoker before open.
- Sticky elements with `position: sticky` + high z-index commonly
  obscure focus near the viewport edge — check.

## Required inputs
Inspectable markup and styles at `target_path`.

## Output format
```json
{"findings": [
   {"wcag": "2.4.7", "severity": "error",
    "path": "globals.css > *:focus",
    "msg": "outline:none with no replacement style",
    "fix": "Add :focus-visible { outline: 2px solid #1d4ed8; }"}],
 "verdict": "block", "confidence": 0.96}
```

## Quality criteria
Pass: focus styles inspected globally and per component; overlay
open/close traced; trap checked inside vs outside modal; findings
specific and actionable.
Fail: accepting `outline: 0` without replacement; not testing return
focus; missing the obscured-focus case.

## Common pitfalls
- Removing browser default outline in a CSS reset and forgetting to
  restore it.
- Focusing the modal container instead of the first interactive
  child (announces nothing).
- Forgetting `inert` on background content while modal is open.
- Trapping focus inside a non-modal popover.

## Examples
Pass:
```css
:focus-visible { outline: 2px solid #1d4ed8; outline-offset: 2px; }
```
```jsx
useEffect(() => { if (open) closeRef.current?.focus(); }, [open]);
```
Fail:
```css
*:focus { outline: none; }   /* no replacement */
```

## Stop condition
Focus styles + overlay focus flow + trap rules + 2.4.11 obscuring
checked; findings emitted; verdict set; no source modified.

## Confidence guidance
Static styles + clear overlay code = 0.97; runtime behaviour inferred
≤0.92; third-party overlay opaque ≤0.88. Must be ≥0.95 to emit.
