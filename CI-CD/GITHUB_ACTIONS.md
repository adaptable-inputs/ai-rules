---
applies_to:
  load: "conditional"
  when: ".github/workflows contains a workflow"
  tools: ["github-actions"]
  annex: "GITHUB_ACTIONS.ANNEX.md"
  purpose: "GitHub Actions pipeline design and quality-gate constraints"
  inherits: ["CI-CD/CI-CD.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "BUILD_TOOLS/**", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# GITHUB_ACTIONS

Guidance for AI agents implementing and reviewing GitHub Actions CI/CD workflows.

## Workflow Defaults
- SHOULD keep workflows deterministic and fail fast.
- SHOULD separate jobs/stages clearly (lint, build, test, security, package, deploy).
- SHOULD keep triggers (`on:`) explicit and minimal by event/branch/path.
- MUST keep permissions explicit with least privilege at workflow and job level.
- MUST pin third-party actions by full commit SHA rather than floating tags.

## Quality Gates
- MUST treat lint, tests, and security scans as merge/release gates.
- MUST keep required gates non-optional for protected branches.
- SHOULD publish test, lint, and coverage reports for review visibility.
- MUST fail workflows on critical dependency/security findings per policy.

## Release Workflow Rules
- SHOULD release workflows are triggered by semantic version tags (for example `vMAJOR.MINOR.PATCH`) or explicit release
  dispatch.
- Release workflows MUST run full build/test/security checks.
- Release artifacts and reports MUST be reproducible from tag alone.
- SHOULD keep release workflows immutable and auditable.
- SHOULD keep rollback and rerun strategy documented.

## Secrets and Security
- MUST use GitHub Secrets/Variables and environment protection rules for credentials.
- MUST NOT print secrets or sensitive payloads in workflow logs.
- SHOULD prefer OIDC-based short-lived cloud credentials over long-lived static keys.
- MUST restrict deploy jobs to protected branches/tags and required approvals.
- MUST keep `GITHUB_TOKEN` permissions minimal; elevate only where required.

## Caching and Artifacts
- SHOULD use caches for dependency acceleration with safe keys (lockfiles/runtime versions).
- SHOULD use artifacts for reproducible cross-job handoff, not implicit workspace assumptions.
- SHOULD keep artifact retention policy explicit and cost-aware.
- SHOULD keep matrix strategies bounded to avoid excessive CI spend/noise.

## Observability and Debuggability
- SHOULD keep workflow/job logs actionable and concise.
- SHOULD emit clear failure context (what failed, where, likely next action).
- SHOULD track workflow duration/flakiness trends.
- SHOULD keep flaky tests/jobs quarantined and actively remediated.
