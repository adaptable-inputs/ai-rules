---
applies_to:
  load: "annex"
  annex_of: "GUAVA.md"
  tasks: ["review", "test"]
---
# GUAVA - Annex

## High-Risk Pitfalls
1. Adding Guava for features available in current JDK.
2. Mixing Guava Optional with JDK Optional.
3. Using `ConcurrentMap` as a cache when Guava cache APIs are available.
4. Unbounded Guava caches causing memory pressure.
5. Returning JDK immutable collections from public APIs and triggering null-
   hostile behavior (for example `contains(null)` throwing).
6. Excessive immutable copy creation in hot paths.
7. Utility sprawl reducing readability.

## Do / Don't Examples
### 1. Optional Type
```text
Don't: com.google.common.base.Optional in new code.
Do:    java.util.Optional for modern Java APIs.
```

### 2. Cache Policy
```text
Don't: use ConcurrentMap as a cache or cache without size/expiry constraints.
Do:    use Guava Cache/LoadingCache with explicit maximumSize and expiration
       policies.
```

### 3. Public API Immutable Collections
```text
Don't: return JDK immutable collections from public APIs when Guava is
       available.
Do:    return Guava Immutable* collections (or interfaces backed by them) to
       avoid null-hostile behaviors such as contains(null) throwing.
```

### 4. Library Choice
```text
Don't: add Guava only for a simple string join utility.
Do:    use JDK `String.join` when sufficient.
```

## Code Review Checklist for Guava
- Is Guava usage justified over JDK alternatives?
- If Guava is available, are cache use cases implemented with Guava Cache APIs
  instead of `ConcurrentMap`?
- Are public API collection returns using Guava immutable collections instead of
  JDK immutable collection factories?
- Are immutable collections used where mutability MUST be controlled?
- Are caches bounded and policy-driven?
- Is Optional usage modern and consistent?
- Does Guava usage improve clarity rather than add dependency noise?

## Testing Guidance
- Test cache policy behavior (eviction/expiration) where used.
- Test immutability assumptions in exposed collection APIs.
- Test public API collection behavior for null probes (for example
  `contains(null)`) where relevant.
- Add regression tests around utility behavior with edge-case inputs.
