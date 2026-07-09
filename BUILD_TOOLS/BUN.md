---
applies_to:
  load: "conditional"
  when: "bun.lockb is present"
  tools: ["bun"]
  annex: "BUN.ANNEX.md"
  purpose: "Bun-specific dependency/install behavior and compatibility controls"
  inherits: ["BUILD_TOOLS/NPM.md", "SECURITY/SECURITY.md", "COMPLIANCE/LICENSES.md"]
---
# BUN

Guidance for AI agents using Bun as package manager/runtime tooling.

## Defaults
- SHOULD use one package manager per repository; do not mix lockfiles.
- MUST commit the Bun lockfile for reproducible installs (format/name depends on Bun version, for example `bun.lock` or
  `bun.lockb`).
- SHOULD keep Bun version pinned in project/tooling config.
- SHOULD validate Bun compatibility with required ecosystem tooling before adoption.

## Install and Lockfile Behavior
- SHOULD use deterministic install behavior in CI.
- SHOULD prefer `bun install --frozen-lockfile` (or equivalent reproducible mode) for
  release pipelines.
- SHOULD use `bun install --lockfile-only` only when intentionally updating lock metadata.
- SHOULD keep node_modules excluded from VCS.

## Lifecycle Script and Trust Model
- Bun dependency lifecycle script behavior differs from npm ecosystem defaults.
- SHOULD configure trusted dependencies explicitly in `bunfig.toml` via `trustedDependencies` when lifecycle scripts are
  required.
- MUST NOT blanket-trust all dependency scripts.
- SHOULD validate build/install outcome for packages requiring postinstall steps.

## Compatibility Guardrails
- SHOULD verify package manager features needed by monorepo/workspace setup.
- SHOULD validate CI images/runners include expected Bun version.
- SHOULD keep fallback path documented if Bun compatibility blocks delivery.
- SHOULD avoid mixing Bun runtime assumptions into scripts intended for Node-only
  environments without explicit checks.

## Security and Credential Handling
- MUST NOT commit registry credentials/tokens.
- MUST use CI secret injection for registry auth.
- MUST scan dependencies and lockfile for vulnerabilities.
- SHOULD keep trusted dependency policy minimal and auditable.

## VCS Ignore Additions
Add these when using Bun (if not already covered by baseline ignore rules):
- `node_modules/`

## Override Notes
- If project MUST interoperate with npm-specific workflows, document explicit
  compatibility boundaries and keep deterministic lockfile/security controls.
