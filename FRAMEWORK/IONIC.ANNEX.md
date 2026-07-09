---
applies_to:
  load: "annex"
  annex_of: "IONIC.md"
  tasks: ["review", "test"]
---
# IONIC - Annex

## High-Risk Pitfalls
1. Direct plugin calls spread across page components.
2. Navigation race conditions that update disposed screens.
3. Missing fallback behavior for unavailable native capabilities.
4. Over-requesting permissions at app start.
5. Large first-load bundles from eager feature imports.
6. Unvalidated deep-link parameters used for navigation decisions.

## Do / Don't Examples
### 1. Native Plugin Access Boundary
```ts
// Don't: call plugins directly from page components.
export class CameraPageBad {
  async takePhoto(): Promise<void> {
    const result = await Camera.getPhoto({ quality: 80 });
    this.preview = result.webPath ?? "";
  }
}

// Do: isolate plugin access in a service boundary.
export class CameraService {
  async takePhoto(): Promise<string | null> {
    const result = await Camera.getPhoto({ quality: 80 });
    return result.webPath ?? null;
  }
}
```

### 2. Route-Triggered Async Safety
```ts
// Don't: ignore stale async updates during route switches.
// Bad because a resolved promise from a left view still writes to `orders`.
class OpenOrdersPageBad {
  orders: Order[] = [];
  constructor(private ordersApi: OrdersApi) {}

  ionViewWillEnter(): void {
    this.ordersApi.loadOpenOrders().then((orders) => {
      this.orders = orders;
    });
  }
}

// Do: cancel/ignore stale work on view leave.
class OpenOrdersPageGood {
  orders: Order[] = [];
  private alive = false;
  constructor(private ordersApi: OrdersApi) {}

  ionViewWillEnter(): void {
    this.alive = true;
    void this.ordersApi.loadOpenOrders().then((orders) => {
      if (!this.alive) return;
      this.orders = orders;
    });
  }

  ionViewDidLeave(): void {
    this.alive = false;
  }
}
```

### 3. Platform Checks
```ts
// Don't: scatter platform checks across UI code.
if (Capacitor.getPlatform() === "android") { /* ... */ }
if (Capacitor.getPlatform() === "ios") { /* ... */ }

// Do: centralize platform branching in one adapter.
export function isNativeMobile(): boolean {
  const platform = Capacitor.getPlatform();
  return platform === "ios" || platform === "android";
}
```

## Code Review Checklist for Ionic
- Are Ionic UI components used consistently before custom replacements?
- Are native plugin calls isolated behind service/adapter boundaries?
- Are permission prompts minimal and user-action driven?
- Are route/lifecycle side effects cancel-safe?
- Are web/device fallbacks defined for native capability gaps?
- Are deep-link/external-intent inputs validated?
- Are first-screen load and interaction paths performance-aware?

## Testing Guidance
- Follow general testing policy in `TEST/TEST.md`.
- Test route transitions for stale async updates and teardown safety.
- Test native-capability fallbacks on web and unsupported device contexts.
- Test permission-denied flows and user recovery paths.
- Test deep-link validation and unauthorized navigation protection.
- Test list-heavy screens on low-end device emulation for responsiveness.
