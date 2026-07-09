---
applies_to:
  load: "annex"
  annex_of: "GRADLE.md"
  tasks: ["review", "test"]
---
# GRADLE - Annex

## High-Risk Pitfalls
1. Building with system Gradle instead of wrapper.
2. Dynamic dependency/plugin versions causing drift.
3. Hidden task side effects breaking cache reproducibility.
4. Global subprojects mutations creating fragile coupling.
5. Credentials committed in gradle properties/settings.
6. Cyclic module dependencies hidden in large builds.

## Do / Don't Examples
### 1. Wrapper Usage
```text
Don't: gradle build
Do:    ./gradlew build
```

### 2. Version Stability
```text
Don't: implementation("com.example:lib:+")
Do:    implementation("com.example:lib:1.4.2")
```

### 3. Task Determinism
```text
Don't: task reads undeclared env/files and writes random output path.
Do:    task declares inputs/outputs and deterministic behavior.
```

## Code Review Checklist for Gradle
- Is wrapper used and maintained?
- Are dependency/plugin versions deterministic?
- Is build logic maintainable and side-effect controlled?
- Are module boundaries and dependency direction clear?
- Are cache/performance settings compatible with task behavior?
- Are repository credentials and supply-chain controls secure?

## Testing Guidance
- Run wrapper-based clean build in CI.
- Run dependency/conflict checks on version changes.
- Validate configuration-cache/build-cache compatibility for key tasks.
- Test multi-module builds for boundary regressions.
- Run vulnerability/license checks for dependency/plugin updates.
