---
applies_to:
  load: "annex"
  annex_of: "ANGULAR.md"
  tasks: ["review", "test"]
---
# ANGULAR - Annex

## High-Risk Pitfalls
1. State propagation loops using `effect()` or late lifecycle hooks.
2. Nested subscriptions that leak and cause callback pyramids.
3. Missing teardown for subscriptions, timers, or observers.
4. `@for` without stable `track`, causing unnecessary DOM recreation.
5. In-place mutation of `OnPush` inputs, leading to stale UI.
6. Heavy template logic or methods that recompute on every check.
7. Writing to parent state during change detection (`NG0100` class errors).
8. Raw DOM writes (`innerHTML`, `ElementRef`) bypassing sanitization.
9. Component-level duplicated HTTP concerns instead of interceptor/service boundaries.
10. Assuming `HttpClient<T>` generics validate runtime payload shape.
11. Async error paths missing UI state updates, creating stuck spinners.
12. Root-scoped effects/subscriptions with no explicit lifetime strategy.

## Do / Don't Examples

### 1. Derived State with Signals
```ts
// Don't: propagate derived state via effect.
export class InvoiceBad {
  readonly subtotal = signal(100);
  readonly taxRate = signal(0.19);
  readonly total = signal(0);

  constructor() {
    effect(() => {
      this.total.set(this.subtotal() * (1 + this.taxRate()));
    });
  }
}

// Do: derive state with computed.
export class InvoiceGood {
  readonly subtotal = signal(100);
  readonly taxRate = signal(0.19);
  readonly total = computed(() => this.subtotal() * (1 + this.taxRate()));
}
```

### 2. Nested Subscriptions vs Composed Stream
```ts
// Don't: nest subscriptions in components.
export class UserPageBad {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const id = params.get("id");
      if (!id) return;
      this.http.get<User>(`/api/users/${id}`).subscribe((user) => {
        // assign user state
      });
    });
  }
}

// Do: compose with RxJS operators and expose a view-model stream.
export class UserPageGood {
  private readonly route = inject(ActivatedRoute);
  private readonly http = inject(HttpClient);

  readonly user$ = this.route.paramMap.pipe(
    map((params) => params.get("id")),
    filter((id): id is string => id !== null && id.trim().length > 0),
    distinctUntilChanged(),
    switchMap((id) => this.http.get<User>(`/api/users/${id}`)),
  );
}
```

### 3. Manual Subscription Cleanup
```ts
// Don't: subscribe imperatively without teardown.
export class NotificationsBad {
  private readonly bus = inject(NotificationBus);

  constructor() {
    this.bus.stream$.subscribe((message) => {
      console.log(message);
    });
  }
}

// Do: use takeUntilDestroyed for imperative subscriptions.
export class NotificationsGood {
  private readonly bus = inject(NotificationBus);

  constructor() {
    this.bus.stream$
      .pipe(takeUntilDestroyed())
      .subscribe((message) => console.log(message));
  }
}
```

### 4. Stable Tracking in `@for`
```html
<!-- Don't: omit track key; Angular cannot map rows efficiently. -->
@for (item of items()) {
  <app-user-row [user]="item"></app-user-row>
}

<!-- Do: use stable identity. -->
@for (item of items(); track item.id) {
  <app-user-row [user]="item"></app-user-row>
}
```

### 5. OnPush and Immutable Inputs
```ts
// Don't: mutate input object in place.
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProfileCardBad {
  readonly user = input.required<User>();

  uppercaseName(): void {
    this.user().name = this.user().name.toUpperCase();
  }
}

// Do: replace object references across OnPush boundaries.
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProfileCardGood {
  readonly user = input.required<User>();
  readonly userChange = output<User>();

  uppercaseName(): void {
    const current = this.user();
    this.userChange.emit({ ...current, name: current.name.toUpperCase() });
  }
}
```

## Code Review Checklist for Angular
- Is each component focused on presentation, with business logic extracted where sensible?
- Could this state derivation be `computed` instead of `effect()`?
- If `effect()` is used, is there a clear reason it cannot be `computed`/`linkedSignal`?
- Are RxJS/signal boundaries explicit (`toSignal()` / `toObservable()`) where crossing reactive models?
- Is one reactive model used per template, with a clear reason documented when mixing `Observable` and signal styles?
- If `toSignal()` / `toObservable()` are created outside an injection context
  (for example utility modules/static functions), is an explicit `Injector` (or equivalent cleanup strategy) provided?
- Are manual subscriptions avoided or cleaned with `takeUntilDestroyed`?
- If `takeUntilDestroyed()` is parameterless, is the usage site in an injection context?
- Are RxJS flows composed (no nested subscriptions)?
- Do all `@for` loops use stable `track` keys?
- Is `$index` used only for static lists and identity tracking avoided?
- Are `OnPush` boundaries respected with immutable updates?
- Are templates free of heavy logic and unnecessary method calls?
- Are cross-cutting HTTP concerns implemented via interceptors/services?
- Are loading/error states explicit, and are async failures surfaced safely?
- Is direct DOM access avoided or explicitly sanitized?
- For DOM post-render integrations, is `afterRenderEffect` used with hydration caveats considered?
- Are effects/subscriptions in root-provided services intentionally long-lived?
- Is zoneless configuration intentional for the Angular version in use?
- Is code safe for SSR/hydration (no unguarded browser globals in render)?
- Are forms typed, and are async validators performance-aware?
- Are route boundaries lazy-loaded where they improve startup without causing deep waterfalls?

## Testing Guidance for Angular-Specific Risks
- Follow general testing expectations in `TEST/TEST.md`.
- Add focused tests for `effect()` / signal interactions when side effects are intentional.
- Test list rendering updates for stable identity behavior in `@for` blocks.
- Test request cancellation/race behavior for route-driven data loading.
- Test manual subscription teardown on component destroy.
- For root-provided services, test or document lifetime expectations for long-lived subscriptions/effects.
- Test `OnPush` components with immutable input updates.
- Test typed form validators (sync and async), including invalid and edge-case states.
- If using zoneless change detection, ensure tests rely on Angular's scheduling signals instead of manual
  `detectChanges()` defaults.
- If SSR/hydration is relevant, test browser-global guards and hydration-safe render paths.
