---
applies_to:
  load: "conditional"
  when: "build.gradle or build.gradle.kts is present"
  tools: ["gradle"]
---
# GRADLE

Guidance for AI agents implementing and reviewing Gradle builds.

## Scope
- Define Gradle-specific reproducibility, dependency/plugin, and CI controls.
- Apply this file to Gradle build scripts and multi-module build design.

## Semantic Dependencies
- Inherit build-layer baseline from `BUILD_TOOLS/BUILD_TOOLS.md`.
- Inherit security/compliance constraints from
  `SECURITY/SECURITY.md` and `COMPLIANCE/LICENSES.md`.
- Inherit CI expectations from `CI-CD/CI-CD.md`.

## Defaults
- SHOULD use Gradle Wrapper (`gradlew`, `gradlew.bat`, `gradle/wrapper/*`).
- MUST pin plugin and dependency versions explicitly.
- SHOULD prefer Kotlin DSL for new builds unless project standard is Groovy DSL.
- SHOULD keep build scripts declarative and deterministic.

## Dependency and Plugin Management
- SHOULD centralize versions via version catalogs or clear convention mechanism.
- SHOULD avoid dynamic versions (`latest.release`, `+`) in production builds.
- SHOULD keep plugin management explicit.
- SHOULD keep dependency constraints clear in multi-module projects.

## Task and Build Logic Design
- SHOULD keep custom tasks small and deterministic.
- SHOULD avoid heavy imperative logic in build scripts when plugins/conventions are
  more maintainable.
- SHOULD isolate build logic into a convention plugin when the same logic is needed by more than one module.
- SHOULD keep task inputs/outputs declared for caching correctness.

## Performance and Caching
- SHOULD use configuration cache/build cache intentionally and keep builds compatible.
- SHOULD avoid tasks with hidden side effects that break caching.
- SHOULD keep build scans/metrics to identify bottlenecks in CI.
- SHOULD keep parallelism settings explicit and environment-aware.

## Multi-Module Governance
- SHOULD keep module boundaries explicit and acyclic.
- SHOULD avoid broad allprojects/subprojects mutation patterns that hide coupling.
- SHOULD keep dependency direction aligned with architecture boundaries.

## Security and Supply Chain
- MUST use trusted repositories and explicit repository declarations.
- MUST keep credentials out of committed files.
- MUST scan dependencies/plugins for vulnerabilities and license compliance.
- MUST treat custom plugin code as production code for review/security.

## VCS Ignore Additions
Add these when using Gradle (if not already covered by baseline ignores):
- `.gradle/`
- `build/`

Do not ignore wrapper scripts or wrapper JAR required for builds.

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

## Override Notes
- Project convention plugins MAY add stricter rules, but wrapper usage,
  deterministic versioning, and secure supply-chain controls remain mandatory.
