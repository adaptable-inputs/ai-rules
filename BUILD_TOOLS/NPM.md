---
applies_to:
  load: "conditional"
  when: "package-lock.json is present"
  tools: ["npm"]
  annex: "NPM.ANNEX.md"
  purpose: "reproducible dependency-management and script-execution rules"
  inherits: ["SECURITY/SECURITY.md", "COMPLIANCE/LICENSES.md", "CI-CD/CI-CD.md"]
---
# NPM

Guidance for AI agents managing Node.js dependencies (npm, Yarn, pnpm).

## Defaults
- SHOULD use one package manager per repository.
- MUST keep a single authoritative lockfile committed.
- MUST pin Node runtime version (`.nvmrc`, `engines`, toolchain config).
- MUST use deterministic install mode in CI (`npm ci`, `pnpm install --frozen-lockfile`, etc.).
- SHOULD keep scripts explicit and side-effect aware.

## Dependency Policy
- SHOULD prefer stable, maintained packages with compatible licenses.
- SHOULD minimize runtime dependencies; avoid redundant utility overlap.
- MUST pin major versions deliberately; upgrade with changelog review.
- SHOULD use overrides/resolutions intentionally and document rationale.

## Script and Workspace Rules
- SHOULD keep package scripts composable and predictable.
- SHOULD avoid scripts that depend on implicit global tools.
- For monorepos, SHOULD keep workspace boundaries explicit.
- SHOULD avoid cross-package script coupling without clear contracts.

## Supply-Chain and Security Guardrails
- MUST NOT commit auth tokens in `.npmrc`.
- MUST use secret-injection in CI for registry credentials.
- MUST enable dependency vulnerability scanning in CI.
- SHOULD verify integrity/signature mechanisms where supported.
- SHOULD avoid automatic postinstall script trust for unknown packages.

## Performance and Reliability
- MUST use caching in CI keyed by lockfile and runtime version.
- SHOULD avoid unnecessary reinstall churn.
- SHOULD keep node_modules out of VCS.
- SHOULD keep install/build logs actionable and fail fast on dependency errors.

## VCS Ignore Additions
Add these when using Node tooling (if not already in baseline ignore list):
- `node_modules/`
- `npm-debug.log*`, `yarn-debug.log*`, `yarn-error.log*`, `pnpm-debug.log*`
- `.npm/`, `.yarn/`, `.pnpm-store/`
- `.pnp.*` (Yarn Plug'n'Play)

## Override Notes
- Specialized package-manager docs MAY narrow manager-specific behavior, but
  lockfile discipline, deterministic installs, and secret/supply-chain safety
  here remain mandatory.
