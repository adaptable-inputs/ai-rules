---
applies_to:
  load: "conditional"
  when: "react is a dependency in package.json"
  frameworks: ["react"]
  annex: "REACT.ANNEX.md"
  purpose: "React-specific component, rendering, and side-effect rules"
  inherits: ["LANGUAGE/JAVASCRIPT/JAVASCRIPT.md", "LANGUAGE/TYPESCRIPT/TYPESCRIPT.md", "LANGUAGE/HTML/HTML.md", "LANGUAGE/CSS/CSS.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "CORE/LOGGING.md"]
---
# REACT

Guidance for AI agents implementing and reviewing React projects.

## Defaults
- SHOULD use functional components and hooks.
- SHOULD keep components small and focused.
- SHOULD prefer composition over inheritance.
- SHOULD treat `useEffect` as a controlled escape hatch, not a default tool.

## Naming Conventions
- This section only defines React-specific naming rules.
- React components: `PascalCase` (for example `UserProfileCard`).
- Custom hooks: `camelCase` with `use` prefix (for example `useUserProfile`).
- Non-React symbol naming follows general TypeScript conventions.

## State and Data
- SHOULD keep state minimal and local where possible.
- SHOULD avoid prop drilling by introducing context sparingly.
- SHOULD avoid unnecessary re-renders; memoize only when it matters.
- SHOULD derive values during render when possible.
- SHOULD prefer framework/server data-loading primitives over client `useEffect` fetching.

## Testing
- SHOULD follow general testing expectations in `TEST/TEST.md`.
- SHOULD use this file's effect-specific checklist and tests for `useEffect` behavior.

## `useEffect` Policy
Effects keep non-React systems in sync; keep React-only derivations in render.

Use `useEffect` when your component MUST connect, subscribe, schedule, observe, or cancel external work.

### Allowed Uses
- Subscriptions: WebSocket, event emitters, browser event listeners.
- Timers and observers.
- Network requests that truly belong on the client.
- Imperative APIs or third-party widgets.

### Discouraged Uses
- Deriving render data from props/state.
- Triggering user intent by "watching state" instead of handling the event.
- Copying props to local state and trying to keep them in sync.
- Business logic that can run directly in reducers or handlers.

## Quick Decision Guide
- Need a value only for rendering: derive in render with plain expressions or `useMemo` if expensive.
- Need to react to user intent (click, submit, change): run side effects in the event handler.
- Need to subscribe to an external store: prefer `useSyncExternalStore`.
- Need setup/cleanup for an external system: use `useEffect`.

## SSR and Hydration Notes
- `useEffect` does not run during server rendering.
- If SSR/hydration is possible, SHOULD avoid `window` / `document` reads during render.
- SHOULD guard browser-only logic in effects or safe initializers.

## High-Risk `useEffect` Pitfalls
1. Derived state effects: `setState(f(props))` in an effect adds extra renders and can loop.
2. Dependency ping-pong: unstable object/function dependencies retrigger effects continuously.
3. Stale closures: async callbacks and listeners read outdated values from old renders.
4. Missing cleanup: subscriptions, timers, and observers continue after unmount/dep changes.
5. Async race conditions: older requests resolve later and overwrite newer state.
6. Strict Mode surprises in development: non-idempotent setup causes duplicate side effects.
7. Effect chains: effect A sets state to trigger effect B, creating fragile temporal coupling.

## Safer Patterns and Alternatives
- SHOULD keep effects small and single-purpose.
- SHOULD co-locate setup and cleanup in the same effect.
- Keep effect callbacks synchronous: never mark the effect callback `async`; use an inner async function.
- Effect callbacks MAY return only cleanup or nothing.
- SHOULD keep dependency arrays honest; do not suppress `react-hooks/exhaustive-deps` without a documented reason.
- If adding a dependency causes a loop, SHOULD redesign the flow instead of deleting the dependency.
- SHOULD use functional state updates to avoid stale closure bugs in intervals/callbacks.
- SHOULD use refs for mutable, non-render state that SHOULD NOT retrigger rendering.
- SHOULD extract repeated side-effect behavior into focused custom hooks.
- For subscription-style state (for example window size), SHOULD prefer custom hooks based on `useSyncExternalStore`.
- SHOULD avoid effect chains: use one cohesive effect, or model flow with explicit actions/reducer/state machine.
- SHOULD handle non-abort async errors explicitly (state/reporting); do not `throw` from fire-and-forget async effect
  tasks. Throwing inside async effect tasks often becomes an unhandled rejection outside React error boundaries.
- If your React version supports `useEffectEvent`, SHOULD use it for non-reactive callback reads instead of stale
  closure workarounds.
- SHOULD use `useLayoutEffect` only for DOM read/write that MUST run before paint.
- `useLayoutEffect` MAY warn in SSR; prefer `useEffect` unless pre-paint DOM reads/writes are required.

## Dependency Rules
- MUST NOT mark an effect callback `async`; create an inner async function.
- Effect callbacks return either cleanup or nothing.
- If an effect reads a reactive value, SHOULD include it in dependencies.
- If adding a dependency breaks behavior, SHOULD fix the design; do not hide the dep.
- SHOULD avoid inline object/function dependencies unless they are intentionally unstable.
- SHOULD stabilize dependencies only at true boundaries (`useMemo` / `useCallback`).
- MUST NOT disable `react-hooks/exhaustive-deps` globally.
- SHOULD enable `eslint-plugin-react-hooks` with `rules-of-hooks` and `exhaustive-deps`.
