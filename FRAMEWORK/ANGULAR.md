---
applies_to:
  load: "conditional"
  when: "angular.json is present"
  frameworks: ["angular"]
  annex: "ANGULAR.ANNEX.md"
---
# ANGULAR

Guidance for AI agents implementing and reviewing Angular projects.

## Scope
- Define Angular-specific component, template, reactive-state, and runtime rules.
- Apply this file to Angular implementation and review tasks.

## Semantic Dependencies
- Inherit JavaScript/TypeScript baselines from
  `LANGUAGE/JAVASCRIPT/JAVASCRIPT.md` and
  `LANGUAGE/TYPESCRIPT/TYPESCRIPT.md`.
- Inherit HTML/CSS accessibility and semantics from
  `LANGUAGE/HTML/HTML.md` and `LANGUAGE/CSS/CSS.md`.
- Inherit architecture constraints from
  `ARCHITECTURE/CLEAN_ARCHITECTURE.md` and `ARCHITECTURE/REST.md` where
  relevant.
- Inherit cross-cutting constraints from
  `SECURITY/SECURITY.md`, `TEST/TEST.md`, `CORE/LOGGING.md`.

## Defaults
- SHOULD follow Angular style guide conventions.
- SHOULD prefer standalone APIs (`bootstrapApplication`, standalone components,
  function providers) for new code.
- SHOULD prefer `inject()` over constructor parameter injection in new code.
- SHOULD apply these rules by default in generated code and code reviews; deviate only with explicit, project-specific
  rationale.
- Before using version-sensitive or experimental APIs, MUST verify the project's
  Angular major version and choose a supported fallback when needed.
- SHOULD keep components and directives focused on presentation concerns.
- SHOULD prefer signal-based local state and `computed` derivations.
- SHOULD treat signal `effect()` as a controlled escape hatch, not a default tool.
- SHOULD prefer explicit boundaries: component UI logic in components, shared logic in
  services/utilities.

## Structure
- SHOULD organize by feature area, not by technical type folders.
- SHOULD keep components small and focused; prefer one main concept per file.
- SHOULD keep related files together (`.ts`, template, styles, and `.spec.ts`).
- SHOULD match file names to the primary identifier and use hyphenated file names.

## Components and Templates
- SHOULD prefer `input()`, `output()`, and `model()` APIs for new components.
- SHOULD mark members initialized by Angular (`input`, `output`, queries) as `readonly` where applicable.
- SHOULD use `protected` for class members that are only read from the template.
- SHOULD name event handlers for the action performed (for example `saveUser()`), not by DOM event name (for example
  `handleClick()`).
- SHOULD keep templates declarative; move complex logic into TypeScript (often `computed`).
- SHOULD prefer `@if`, `@for`, and `@switch` blocks in modern Angular code.
- In every `@for`, SHOULD use a stable `track` expression (`id`/`uuid`), not incidental identity.
- SHOULD use `$index` tracking only for truly static collections that never reorder or change length.
- SHOULD avoid identity tracking (`track item`) except as a last resort.
- SHOULD prefer native granular bindings (`[class.foo]`, `[style.width.px]`) over
  `ngClass` / `ngStyle`.
- SHOULD use `[class]` / `[style]` only when intentionally setting the full attribute.

## State, Signals, and RxJS
- SHOULD keep one clear source of truth; derive secondary state via `computed`.
- SHOULD avoid propagating state changes via `effect()`; use `computed` or explicit
  actions instead.
- SHOULD use RxJS composition operators (`switchMap`, `combineLatest`, `map`, etc.) instead of nested subscriptions.
- SHOULD prefer one reactive model per component/template:
  use `async` pipe for `Observable` view models, read signal view models
  directly, and convert at boundaries with `toSignal()` / `toObservable()`.
- SHOULD avoid mixing `Observable` and signal binding styles in the same template
  unless there is a strong reason.
- When using `toSignal()` / `toObservable()` outside an injection context
  (for example plain utility modules, static functions, or code created outside
  component/service construction), pass an explicit `Injector` option (for
  example `toSignal(source$, { injector })` or
  `toObservable(signalValue, { injector })`) so interop resources are torn down
  correctly.
- For `toSignal()`, `manualCleanup: true` keeps the subscription until the
  source completes and disables destroy-driven teardown.
  Use it only when the source is guaranteed to complete or when you explicitly
  manage lifecycle; otherwise it can leak.
- `toSignal()` surfaces Observable errors through signal reads:
  handle errors in the stream (for example with `catchError`) when you need a
  rendered error state instead of thrown reads.
  Prefer explicit renderable state (`{ status, value, error }`) or a sentinel
  fallback value for template paths.
- Signals created by `toSignal()` do not expose completion state.
  If completion matters (for example to render "done"), model it explicitly in
  stream/state (for example `{ status, value, error }`).
- SHOULD avoid manual subscriptions in components unless an imperative side effect is
  required.
- For imperative subscriptions, MUST use `takeUntilDestroyed()` (or equivalent `DestroyRef` cleanup) to prevent leaks.
- Parameterless `takeUntilDestroyed()` works only in an injection context;
  otherwise pass `DestroyRef` explicitly.
  Example: `stream$.pipe(takeUntilDestroyed(this.destroyRef))` with
  `private readonly destroyRef = inject(DestroyRef)`.
- SHOULD be explicit about lifetime in services: root-provided services can keep subscriptions/effects alive until app
  teardown. These are effectively root effects, while effects tied to component injectors are view-scoped.

## `effect()` Policy
Effects synchronize Angular state with non-reactive or imperative systems.

### Allowed Uses
- Logging/analytics tied to signal changes.
- Synchronizing state to browser storage.
- Integrating with imperative APIs (canvas, charts, third-party widgets).
- Registering imperative behavior not expressible in template syntax.

### Discouraged Uses
- Deriving state from other state (use `computed`).
- Propagating state from one signal/store into another as workflow glue.
- Modeling user intent flow by "watching" state instead of handling the event.
- Coordinating request flows that are better expressed with RxJS pipelines.

### Guardrails
- SHOULD treat `effect()` as the last API choice: prefer `computed()` for derived values and `linkedSignal()` for
  derived-but-overridable values.
- Assume effects can re-run:
  always use `onCleanup` for effect-created resources (timers, listeners,
  subscriptions, observers, and similar handles).
- `effect()` creation requires an injection context:
  outside constructors/field initializers, pass an explicit `Injector`.
- SHOULD prefer `afterRenderEffect`/`afterNextRender` for DOM read/write that MUST
  happen after render.
- `afterRenderEffect` and `afterNextRender` callbacks run only on browser
  platforms, and components are not guaranteed to be hydrated before callbacks
  run; keep DOM access hydration-safe.
- MUST NOT mutate SSR-produced DOM structure in post-render hooks unless
  hydration behavior is intentionally controlled.

## Dependency Injection and Services
- SHOULD keep services focused and composable; avoid "god services".
- SHOULD keep pure transformation logic framework-agnostic where possible.
- SHOULD scope providers intentionally (component/route/root) based on lifetime.
- SHOULD keep cross-cutting HTTP concerns in interceptors, not duplicated in components.
- SHOULD prefer functional interceptors for predictable behavior in complex setups.

## Routing and Data Loading
- SHOULD define route trees per feature and lazy-load feature boundaries with `loadComponent` / `loadChildren`.
- SHOULD use route guards/resolvers where navigation-level guarantees are required.
- SHOULD keep route-level dependencies near routes, using route provider scopes when helpful.
- SHOULD avoid unnecessary deep lazy-loading chains that create navigation waterfalls.

## HTTP and Error Handling
- SHOULD keep HTTP access in data services, not scattered across templates/components.
- For signal-first data loading, MAY use `httpResource` (experimental /
  version-dependent) only after verifying support in the current Angular major,
  and when you explicitly want a resource-style
  loading/error/value state model without ad-hoc subscriptions/interop.
- SHOULD model loading, success, and error states explicitly in UI-facing view models.
- SHOULD handle errors at the boundary where context exists (service/component), and map to actionable user-facing
  state.
- MUST NOT swallow errors silently; either recover with an explicit fallback or
  report/log through the chosen observability path.
- SHOULD keep cross-cutting concerns (auth headers, retries, correlation IDs, standardized error mapping) in
  interceptors.

## Forms
- SHOULD prefer typed reactive forms for medium/large business forms.
- SHOULD prefer `NonNullableFormBuilder` or `{ nonNullable: true }` where null is not
  a valid domain state.
- SHOULD keep validators pure and reusable; place cross-field rules at group level.
- SHOULD avoid server-bound async validation on every keystroke:
  use `updateOn: 'blur'` for field-level checks and `updateOn: 'submit'` when
  validation needs the whole form.
- Remember `form.value` excludes disabled controls; use `getRawValue()` only
  when intentionally including disabled fields.

## Change Detection and Performance
- SHOULD prefer `ChangeDetectionStrategy.OnPush` for reusable or heavy component
  subtrees.
- SHOULD treat `OnPush` inputs as immutable boundaries; replace object references rather than mutating in place.
- SHOULD avoid expensive template calls and repeated allocations during change
  detection.
- SHOULD use stable track keys in list rendering to minimize DOM churn.
- SHOULD use `ChangeDetectorRef.markForCheck()` only when integrating with non-standard update paths.

## Zoneless Notes
- Base zoneless setup on the official Angular guidance for your exact major
  version: `https://angular.dev/guide/zoneless`.
- In projects configured for zoneless change detection, SHOULD use the version-recommended setup (for example helper
  providers like `provideZonelessChangeDetection()` where applicable).
- In Angular versions where zoneless is the default (for example v21+), SHOULD verify `provideZoneChangeDetection()` is
  not unintentionally re-enabling Zone.js semantics.
- SHOULD use `provideZoneChangeDetection()` only when intentionally opting into Zone.js semantics, and keep Zone.js
  runtime/test polyfills configured.
- For SSR with zoneless change detection, SHOULD use `PendingTasks` / `pendingUntilEvent` to ensure required async
  render work finishes before serialization.
- SHOULD remove `NgZone.onStable` / `onMicrotaskEmpty` style "wait for stability" patterns; prefer `afterNextRender` /
  `afterEveryRender` or explicit DOM observers when the DOM is mutated outside Angular.
- In zoneless apps, SHOULD prefer clear Angular change notifications: signals read by templates, template/host
  listeners, `async` pipe, and `markForCheck()` at integration boundaries.
- When committing to zoneless mode and no longer relying on Zone.js semantics, SHOULD remove `zone.js` and
  `zone.js/testing` from build/test polyfills.

## SSR and Hydration Notes
- Keep render paths SSR-safe: no unguarded `window` / `document` reads during
  render.
- SHOULD keep initial server and client markup consistent to avoid hydration mismatch and layout shift.
- SHOULD run browser-only integrations after render/hydration where possible.
- Some lifecycle hooks (for example initialization) run during SSR; do not
  assume "after render" implies "browser".
- SHOULD guard browser-only APIs with platform checks (for example `isPlatformBrowser` / `PLATFORM_ID`) and/or defer DOM
  work with SSR-safe primitives (for example `afterNextRender`).
- SHOULD evaluate third-party DOM-manipulating libraries for hydration compatibility.

## Security
- MUST NOT build Angular templates from user-controlled strings.
- SHOULD prefer template binding over direct DOM APIs.
- If direct DOM interaction is unavoidable, MUST sanitize untrusted values with `DomSanitizer.sanitize` and the correct
  `SecurityContext`.
- MUST treat `bypassSecurityTrust*` as exceptional and document trust boundaries.
- MUST keep Angular updated and use production AOT builds.

## Override Notes
- Project-specific Angular conventions MAY add stricter structure or delivery
  constraints, but reactivity clarity, cleanup safety, and SSR/hydration
  guardrails remain mandatory.
