---
applies_to:
  load: "conditional"
  when: "build.gradle or build.gradle.kts is present"
  tools: ["gradle"]
  annex: "GRADLE.ANNEX.md"
  purpose: "Gradle-specific reproducibility, dependency/plugin, and CI controls"
  inherits: ["BUILD_TOOLS/BUILD_TOOLS.md", "SECURITY/SECURITY.md", "COMPLIANCE/LICENSES.md", "CI-CD/CI-CD.md"]
---
# GRADLE

Guidance for AI agents implementing and reviewing Gradle builds.

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

## Override Notes
- Project convention plugins MAY add stricter rules, but wrapper usage,
  deterministic versioning, and secure supply-chain controls remain mandatory.
