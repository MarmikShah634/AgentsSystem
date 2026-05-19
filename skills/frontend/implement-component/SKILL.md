---
id: implement-component
category: frontend
owner_agent: frontend
inputs:
  - component_name: "PascalCase identifier, e.g. UserCard"
  - props_schema: "TypeScript interface or JSON Schema for the component's props"
  - file_path: "absolute path where the component file should live"
  - design_ref: "Figma node URL or design-system token reference"
outputs:
  - patch: "unified diff of changes"
  - touched_paths: "list of files modified or created"
  - rationale: "1-3 sentences"
  - confidence: "float in [0,1]"
requires_plan: true
emits_confidence: true
confidence_floor: 0.85
---

# Skill: implement-component

## Purpose
Author one reusable presentational UI component that accepts the declared props and renders deterministically. No data fetching, no global state, no business logic — pure rendering plus local interaction (hover, focus, disclosure).

## When to invoke
Invoke when the plan step says implement a component AND a paired unit/Storybook test step exists AND the design reference is non-empty. Reject if the spec demands network calls, route knowledge, or auth state — those belong in `implement-page`.

## Procedure (follow exactly)
1. Resolve `file_path`. If a component already exists there, STOP and ask human (probably `refactor-frontend`).
2. Define the props type from `props_schema` exactly. Required vs optional must match. Do not add props that aren't in the schema.
3. Implement rendering using the project's existing UI primitives (design system, Tailwind tokens, CSS modules — whatever is already in use). Do not introduce a new styling system.
4. Render loading, empty, and error states ONLY if a corresponding prop or slot is declared. Otherwise stay pure.
5. Local state (hover, expanded) → use the framework's idiomatic hook/composable (`useState`, `ref`, `signal`). Never a global store.
6. Accessibility: every interactive element keyboard-reachable; semantic HTML preferred over `role` attributes; alt text from props.
7. Run the paired unit test / Storybook story for each prop shape. If it fails, fix the component, never the test.

## How to think
- Prop semantics ambiguous → STOP and ask human; do not guess.
- Looks like a page (calls fetch, reads route) → reject and request `implement-page`.
- Visual token missing from design system → reuse the closest token and note in `rationale`; do not invent colors/spacing.
- Memoization → only with profiling evidence in the plan, otherwise omit.

## Required inputs
All four fields non-empty. `props_schema` must enumerate every prop with type and required-flag.

## Output format
{"patch": "unified diff", "touched_paths": ["src/components/UserCard/UserCard.tsx", "src/components/UserCard/UserCard.test.tsx"], "rationale": "1-3 sentences", "confidence": 0.0}

## Quality criteria
Passes if: props match schema exactly; component is a pure function of props; no imports from `api/`, `store/`, `router/`; unit tests cover every prop variant; a11y lint clean.
Fails if: fetches data; reads global state; mutates props; introduces a new dependency; ships untyped `any` props.

## Common pitfalls
- Importing `fetch`/`axios` inside a component. Forbidden — pass data via props.
- Inline styles where design tokens exist. Use the token.
- `useEffect` for derivation. Compute during render.
- Spreading `...props` onto root DOM. Be explicit about which props pass through.

## Examples
React/TS:
```tsx
type UserCardProps = { name: string; avatarUrl?: string; onClick?: () => void };
export function UserCard({ name, avatarUrl, onClick }: UserCardProps) {
  return (
    <button onClick={onClick} className="card">
      {avatarUrl ? <img src={avatarUrl} alt="" /> : <span aria-hidden>?</span>}
      <span>{name}</span>
    </button>
  );
}
```

Anti-pattern:
```tsx
export function UserCard({ id }: { id: string }) {
  const [user, setUser] = useState<any>();           // wrong layer
  useEffect(() => { fetch(`/api/u/${id}`).then(r => r.json()).then(setUser); }, [id]);
  return <div style={{ color: '#ff0066' }}>{user?.name}</div>;  // hard-coded color
}
```

## Stop condition
Component file exists at `file_path`; paired test asserts every prop variant; tests pass; no file outside `touched_paths` modified.

## Confidence guidance
Lower when: design ref ambiguous (≤0.75), prop semantics underspecified (≤0.7), new file in unfamiliar folder (≤0.8), a11y unclear (≤0.8). Floor 0.85 to proceed.
