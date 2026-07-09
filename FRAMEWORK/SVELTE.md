---
applies_to:
  load: "conditional"
  when: "svelte.config.js is present"
  frameworks: ["svelte"]
  annex: "SVELTE.ANNEX.md"
---
# SVELTE

Guidance for AI agents implementing and reviewing Svelte projects.

## Scope
- Define Svelte-specific component, reactivity, and state-management rules.
- Apply this file to Svelte/SvelteKit implementation and review tasks.

## Semantic Dependencies
- Inherit JavaScript baseline from `LANGUAGE/JAVASCRIPT/JAVASCRIPT.md`.
- Apply `LANGUAGE/TYPESCRIPT/TYPESCRIPT.md` as an additional parent when the
  Svelte codebase uses TypeScript.
- Inherit HTML/CSS accessibility and semantics from
  `LANGUAGE/HTML/HTML.md` and `LANGUAGE/CSS/CSS.md`.
- Inherit cross-cutting constraints from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

## Defaults
- SHOULD keep components focused and small.
- SHOULD prefer explicit props/events/store boundaries over hidden cross-component
  coupling.
- SHOULD keep business logic outside template markup when complexity grows.
- SHOULD prefer derived/reactive values for view state over duplicated mutable state.

## Reactivity and State Rules
- SHOULD keep one source of truth for each state concern.
- SHOULD avoid cascading reactive statements that create implicit update loops.
- SHOULD use stores for cross-component/shared state.
- SHOULD keep component-local state local unless there is clear sharing need.
- SHOULD avoid mutating shared objects in-place without explicit intent.

## Side Effects and Lifecycle
- SHOULD keep setup/teardown side effects explicit in lifecycle hooks.
- For dependency-driven side effects, SHOULD use controlled reactive blocks (`$:` in Svelte 3/4, or `$effect` when using
  Svelte 5+ runes) and avoid uncontrolled reactive side-effect chains.
- SHOULD clean up subscriptions/listeners/timers in teardown paths.
- SHOULD avoid running heavy side effects during rendering paths.
- SHOULD guard browser-only APIs when SSR/hydration is relevant.

## Template and Accessibility
- SHOULD prefer semantic HTML and accessible controls.
- SHOULD ensure keyboard/focus behavior for interactive elements.
- SHOULD keep template expressions simple; extract complex logic into script section.
- SHOULD avoid duplicated conditional fragments when component extraction improves
  readability.

## Performance Baseline
- SHOULD avoid unnecessary store subscriptions and broad reactive dependencies.
- SHOULD use keyed each-blocks for stable list updates.
- SHOULD keep expensive computations memoized/derived outside repeated render logic.
- SHOULD split large components by feature boundary.

## Override Notes
- Project-specific SvelteKit conventions MAY add routing/data-loading rules, but
  reactivity clarity, cleanup safety, and accessibility constraints remain
  mandatory.
