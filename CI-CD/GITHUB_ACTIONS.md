---
applies_to:
  load: "conditional"
  when: ".github/workflows contains a workflow"
  tools: ["github-actions"]
---
# GITHUB_ACTIONS

Guidance for AI agents implementing and reviewing GitHub Actions CI/CD
workflows.

## Scope
- Define GitHub Actions pipeline design and quality-gate constraints.
- Apply this file to workflow files under `.github/workflows/` and reusable
  workflow definitions.

## Semantic Dependencies
- Inherit CI/CD baseline from `CI-CD/CI-CD.md`.
- Inherit build/security/testing constraints from
  `BUILD_TOOLS/**`, `SECURITY/SECURITY.md`, and `TEST/TEST.md`.
- Inherit VCS workflow requirements from `CORE/VERSION_CONTROL_SYSTEM.md`.

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
- Release workflows are triggered by semantic version tags
  (for example `vMAJOR.MINOR.PATCH`) or explicit release dispatch.
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

## High-Risk Pitfalls
1. Floating action versions introducing unreviewed behavior changes.
2. Broad `GITHUB_TOKEN` permissions across all jobs by default.
3. Optional quality gates on protected branches.
4. Secret leakage through logs or committed workflow config.
5. Release workflows bypassing full validation gates.
6. Fragile cache keys causing stale/corrupt build state.
7. Overly broad trigger rules running deploy jobs unexpectedly.

## Do / Don't Examples
### 1. Action Pinning
```text
Don't: uses: actions/checkout@v4
Do:    uses: actions/checkout@<full-commit-sha>
```

### 2. Token Permissions
```text
Don't: permissions: write-all
Do:    set minimal read/write scopes per workflow/job need.
```

### 3. Release Safety
```text
Don't: publish release artifacts without test/security dependencies.
Do:    enforce full gate chain before publish/deploy.
```

## Code Review Checklist for GitHub Actions
- Are workflow triggers explicit and least-surprise?
- Are stages/gates explicit and complete?
- Are merge/release quality gates enforced?
- Are action versions pinned by full SHA?
- Are token permissions and secret handling least-privilege and safe?
- Are cache/artifact strategies deterministic and safe?
- Is release reproducibility from tag alone guaranteed?

## Testing Guidance
- Validate workflow YAML syntax and execution logic before merge.
- Run workflow changes on PR branches and verify required gates.
- Test release workflow on pre-release tags in staging when possible.
- Test failure scenarios (missing secrets, failing tests, vulnerability gates).
- Verify deploy jobs honor environment protections/required approvals.

## Override Notes
- Project-specific delivery policies MAY add stricter approvals/compliance
  gates, but deterministic quality-gated workflows, least-privilege
  permissions, and secret hygiene remain mandatory.
