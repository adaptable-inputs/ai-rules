---
applies_to:
  load: "annex"
  annex_of: "REACT.md"
  tasks: ["review", "test"]
---
# REACT - Annex

## Do / Don't Examples

### 1. Derived State
```tsx
// Don't: derive state from props via effect.
function PriceBad({ amount, taxRate }: { amount: number; taxRate: number }) {
  const [total, setTotal] = useState(amount);
  useEffect(() => setTotal(amount * (1 + taxRate)), [amount, taxRate]);
  return <span>{total.toFixed(2)}</span>;
}

// Do: derive during render.
function PriceGood({ amount, taxRate }: { amount: number; taxRate: number }) {
  const total = amount * (1 + taxRate);
  return <span>{total.toFixed(2)}</span>;
}
```

### 2. User Intent
```tsx
// Don't: watch state to trigger an action.
// Bad because user intent is now indirect state coupling and easy to mis-handle.
// Also breaks repeated clicks unless state is reset.
function SaveButtonBad({ onSave }: { onSave: () => Promise<void> }) {
  const [shouldSave, setShouldSave] = useState(false);
  useEffect(() => {
    if (shouldSave) void onSave();
  }, [shouldSave, onSave]);
  return <button onClick={() => setShouldSave(true)}>Save</button>;
}

// Do: perform user-driven side effects in the handler.
function SaveButtonGood({ onSave }: { onSave: () => Promise<void> }) {
  return <button onClick={() => void onSave()}>Save</button>;
}
```

### 3. Stale Interval Closure
```tsx
// Don't: interval callback captures stale "count".
function CounterBad() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setCount(count + 1), 1000);
    return () => clearInterval(id);
  }, []);

  return <span>{count}</span>;
}

// Do: use functional updates for latest state.
function CounterGood() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setCount((current) => current + 1), 1000);
    return () => clearInterval(id);
  }, []);

  return <span>{count}</span>;
}
```

### 4. Async Fetch Race and Cleanup
```tsx
// Don't: allow stale responses to overwrite newer state.
function UserProfileBad({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function loadBad() {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) return;
      const data = (await response.json()) as User;
      setUser(data);
    }

    void loadBad();
  }, [userId]);

  return user ? <ProfileCard user={user} /> : <Spinner />;
}

// Do: cancel stale requests and ignore abort errors.
function UserProfileGood({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    // Prevent stale data from the previous request context.
    setError(null);
    setUser(null);

    async function loadGood() {
      try {
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal,
        });
        if (!response.ok) {
          setError(new Error(`User fetch failed: ${response.status}`));
          return;
        }
        const data = (await response.json()) as User;
        setUser(data);
        setError(null);
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          return;
        }
        setError(
          err instanceof Error ? err : new Error("Unknown user fetch error")
        );
      }
    }

    void loadGood();
    return () => controller.abort();
  }, [userId]);

  if (error) return <span>Failed to loadGood user.</span>;
  return user ? <ProfileCard user={user} /> : <Spinner />;
}
```

### 5. Subscription Cleanup
```tsx
// Don't: subscribe without cleanup.
// Bad because it reads `window` during render and leaks event listeners.
function WindowWidthBad() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    function onResizeBad() {
      setWidth(window.innerWidth);
    }

    window.addEventListener("resize", onResizeBad);
  }, []);

  return <span>{width}</span>;
}

// Do: always pair subscription setup with cleanup.
function WindowWidthGood() {
  const [width, setWidth] = useState(() =>
    typeof window === "undefined" ? 0 : window.innerWidth
  );

  useEffect(() => {
    if (typeof window === "undefined") return;

    function onResizeGood() {
      setWidth(window.innerWidth);
    }

    // Initialize width immediately after mount.
    onResizeGood();
    window.addEventListener("resize", onResizeGood);
    return () => window.removeEventListener("resize", onResizeGood);
  }, []);

  return <span>{width}</span>;
}
```

## Code Review Checklist for Effects
- Does this effect synchronize with an external system?
- Could this logic be derived during render instead?
- Could this logic run in an explicit user event handler instead?
- Is the effect callback synchronous and returning only cleanup or nothing?
- Are all reactive values read by the effect listed in dependencies?
- If dependencies are omitted, is there a documented, safe reason?
- Is setup idempotent under React Strict Mode development re-runs?
- Is cleanup present for every subscription, timer, observer, and listener?
- Does async work abort or ignore stale requests on dependency change?
- Can older async responses overwrite newer state?
- Is render code safe if SSR/hydration exists (no unguarded browser globals)?
- Is there effect chaining that SHOULD be replaced by explicit actions?
- Are inline dependencies causing unnecessary effect churn?
- Would extracting a custom hook reduce duplicated side-effect logic?
- Are lint suppressions for hooks justified and minimal?

## Testing Guidance for Effect-Heavy Code
- Test cleanup on unmount.
- Test cleanup on dependency change.
- Test race handling with fast/slow responses.
- Test that stale async results do not overwrite newer state.
- Test behavior under `StrictMode` for duplicate setup/cleanup safety.
- Test that user-intent side effects happen from handlers, not watcher effects.
- If SSR/hydration is relevant, test render paths that avoid browser globals.
