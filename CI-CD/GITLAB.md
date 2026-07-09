---
applies_to:
  load: "conditional"
  when: ".gitlab-ci.yml is present"
  tools: ["gitlab-ci"]
  annex: "GITLAB.ANNEX.md"
---
# GITLAB

Guidance for AI agents implementing and reviewing GitLab CI/CD pipelines.

## Scope
- Define GitLab pipeline design and quality-gate constraints.
- Apply this file to `.gitlab-ci.yml`, reusable templates, and release jobs.

## Semantic Dependencies
- Inherit CI/CD baseline from `CI-CD/CI-CD.md`.
- Inherit build/security/testing constraints from
  `BUILD_TOOLS/**`, `SECURITY/SECURITY.md`, and `TEST/TEST.md`.
- Inherit VCS workflow requirements from `CORE/VERSION_CONTROL_SYSTEM.md`.

## Pipeline Defaults
- SHOULD keep pipelines deterministic and fast-fail.
- SHOULD separate stages clearly (lint, build, test, security, package, deploy).
- SHOULD keep job boundaries explicit and cache/artifact strategy intentional.
- SHOULD keep pipeline behavior branch/tag-aware with explicit rules.

## Quality Gates
- MUST treat lint, tests, and security scans as merge/release gates.
- MUST keep required gates non-optional for protected branches.
- SHOULD publish test and coverage reports for review visibility.
- MUST fail pipeline on critical dependency/security findings per policy.

## Release Pipeline Rules
- SHOULD release pipelines are triggered by semantic version tags (for example `vMAJOR.MINOR.PATCH`).
- Release pipelines MUST run full build/test/security checks.
- Release artifacts and reports MUST be reproducible from tag alone.
- SHOULD keep release jobs immutable and auditable.
- SHOULD keep rollback and re-run strategy documented.

## Secrets and Security
- MUST use masked/protected CI variables for credentials.
- MUST NOT echo secrets in job logs.
- MUST restrict deployment jobs to protected branches/tags and required approvals.
- SHOULD pin container images used by CI jobs where possible.

## Caching and Artifacts
- SHOULD use caches for dependency acceleration with safe keys (lockfiles/runtime versions).
- SHOULD use artifacts for reproducible stage handoff, not implicit workspace state.
- SHOULD keep artifact retention policy explicit and cost-aware.

## Observability and Debuggability
- SHOULD keep job logs actionable and concise.
- SHOULD emit clear failure context (what failed, where, likely next action).
- SHOULD track pipeline duration/flakiness trends.
- SHOULD keep flaky tests quarantined and actively remediated.

## Override Notes
- Project-specific delivery policies MAY add stricter approvals/compliance gates,
  but deterministic quality-gated pipelines and secret hygiene remain mandatory.
