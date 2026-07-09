---
applies_to:
  load: "annex"
  annex_of: "MAVEN.md"
  tasks: ["review", "test"]
---
# MAVEN - Annex

## High-Risk Pitfalls
1. Unpinned plugin versions causing non-deterministic builds.
2. Version ranges introducing drift.
3. Profile combinations altering artifact unexpectedly.
4. CI using system Maven instead of wrapper.
5. Credentials committed in settings files.
6. Transitive dependency conflicts unresolved until runtime.

## Do / Don't Examples
### 1. Version Pinning
```text
Don't: <version>[1.0,)</version>
Do:    explicit fixed version (or BOM-managed fixed set).
```

### 2. CI Invocation
```text
Don't: mvn test (system Maven in CI)
Do:    ./mvnw -B clean verify
```

### 3. Plugin Version
```text
Don't: plugin without explicit version.
Do:    plugin with pinned version in pluginManagement/build plugins.
```

## Code Review Checklist for Maven
- Is Maven Wrapper present and used in docs/CI?
- Are dependency/plugin versions pinned and auditable?
- Are profile effects explicit and controlled?
- Are repository/credential settings secure?
- Are license/security checks integrated?
- Are transitive conflicts and exclusions intentional?

## Testing Guidance
- Run clean wrapper-based build in CI and local reproducibility checks.
- Test profile-specific builds used in release/deploy workflows.
- Run dependency tree/conflict inspection for critical changes.
- Run vulnerability/license scan on dependency updates.
