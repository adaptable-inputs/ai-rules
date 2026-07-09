---
applies_to:
  load: "conditional"
  when: "pom.xml is present"
  tools: ["maven"]
  annex: "MAVEN.ANNEX.md"
  purpose: "Maven-specific reproducibility, dependency, and lifecycle controls"
  inherits: ["BUILD_TOOLS/BUILD_TOOLS.md", "SECURITY/SECURITY.md", "COMPLIANCE/LICENSES.md", "CI-CD/CI-CD.md"]
---
# MAVEN

Guidance for AI agents implementing and reviewing Maven builds.

## Defaults
- SHOULD use Maven Wrapper (`mvnw`, `mvnw.cmd`, `.mvn/wrapper/*`) for reproducible builds.
- SHOULD keep plugin and dependency versions explicitly pinned.
- SHOULD keep build lifecycle predictable and avoid hidden side effects in profiles.
- SHOULD keep parent/BOM usage intentional and documented.

## Dependency and Plugin Management
- SHOULD centralize versions with `dependencyManagement`/BOM when more than one module depends on the same artifact.
- SHOULD avoid floating versions (`LATEST`, `RELEASE`, version ranges) in production
  builds.
- SHOULD keep plugin versions pinned; avoid implicit plugin-version resolution.
- SHOULD minimize duplicate transitive dependency paths and exclusions.

## Profile and Environment Rules
- SHOULD keep profiles explicit and purpose-driven.
- SHOULD avoid profiles that change core artifact semantics unexpectedly.
- SHOULD prefer environment-independent default build; use profiles for explicit
  deployment/runtime variations.
- SHOULD document required profile combinations for release builds.

## Reproducibility and CI
- SHOULD use wrapper in CI, not system Maven.
- SHOULD keep CI build flags deterministic (`-B`, optionally `-ntp` etc.).
- SHOULD ensure clean build paths for release (`clean verify`/project standard).
- SHOULD cache dependencies safely keyed by pom/wrapper/runtime version.

## Security and Supply Chain
- MUST use trusted artifact repositories and explicit mirror config.
- MUST keep repository credentials out of source-controlled settings.
- MUST enable dependency and plugin vulnerability/license checks in CI.
- MUST treat custom plugin executions as code with security review.

## VCS Ignore Additions
Add these when using Maven (if not already covered by baseline ignores):
- `target/`
- `*.class`, `*.war`, `*.ear`
- `pom.xml.tag`, `pom.xml.releaseBackup`, `pom.xml.versionsBackup`,
  `pom.xml.next`
- `release.properties`, `dependency-reduced-pom.xml`,
  `buildNumber.properties`
- `.mvn/timing.properties`

Do not ignore wrapper scripts or wrapper JARs required for build
(for example `.mvn/wrapper/maven-wrapper.jar`).
If a broader ignore pattern includes `*.jar`, add an explicit negation rule
for the wrapper JAR.

## Override Notes
- Project-specific release processes MAY add stricter Maven workflow rules, but
  wrapper usage, deterministic versioning, and supply-chain controls remain
  mandatory.
