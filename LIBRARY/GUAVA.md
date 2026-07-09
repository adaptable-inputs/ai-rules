---
applies_to:
  load: "conditional"
  when: "guava is a declared dependency"
  libraries: ["guava"]
  annex: "GUAVA.ANNEX.md"
---
# GUAVA

Guidance for AI agents implementing and reviewing Guava usage.

## Scope
- Define when to use Guava utilities versus JDK/native alternatives.
- Apply this file to Java utility, collections, and helper API decisions.

## Semantic Dependencies
- Inherit Java baseline from `LANGUAGE/JAVA/JAVA.md`.
- Inherit design/readability constraints from `DESIGN/CLEAN_CODE.md` and
  `LANGUAGE/READABILITY.md`.

## Defaults
- SHOULD prefer JDK standard library when equivalent functionality exists, except for
  the Guava-specialized cases below.
- SHOULD use Guava intentionally where it adds clear value.
- SHOULD prefer immutable collections (`ImmutableList`, `ImmutableMap`) for shared or
  exposed state.
- If Guava is available, SHOULD prefer Guava cache types (`Cache`, `LoadingCache`) over using `ConcurrentMap` as a
  cache.
- If Guava is available, SHOULD prefer Guava immutable collections over Java immutable collections when returning
  collections from public APIs.
- SHOULD prefer Guava immutable collections for API return values when callers MAY
  probe with nulls (`contains(null)`); Java immutable collections are null
  hostile and MAY throw.
- SHOULD keep Guava usage consistent; avoid mixed utility ecosystems without reason.

## API Usage Rules
- SHOULD use `Preconditions` for argument/state validation where clarity improves.
- SHOULD prefer `java.util.Optional` over Guava Optional in modern code.
- SHOULD use Guava cache utilities with explicit size/expiry policy.
- MUST NOT model caches as plain `ConcurrentMap` when Guava is already available.
- For public API collection returns, SHOULD use `ImmutableList`/`ImmutableSet`/ `ImmutableMap` (or return interfaces
  backed by those types) instead of JDK immutable collection factories.
- SHOULD avoid hidden performance costs from repeated immutable-copy churn.

## Dependency and Migration Guardrails
- SHOULD avoid introducing Guava solely for trivial helpers.
- SHOULD minimize hard coupling to rarely-used Guava APIs when JDK alternatives are viable.
- SHOULD keep migration path in mind for future Java baseline upgrades.

## Override Notes
- Project-specific utility standards MAY restrict Guava usage further.
- Baseline rule: prefer standard library first, Guava second with clear value.
- Explicit specialization in this doc: when Guava is available, prefer Guava
  Cache over `ConcurrentMap` for caching and prefer Guava immutable collections
  over JDK immutable collections for public API returns.
