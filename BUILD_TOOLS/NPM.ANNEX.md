---
applies_to:
  load: "annex"
  annex_of: "NPM.md"
  tasks: ["review", "test"]
---
# NPM - Annex

## High-Risk Pitfalls
1. Mixing lockfiles/package managers in one repository.
2. Installing with non-frozen mode in CI and drifting dependencies.
3. Committing registry tokens in `.npmrc`.
4. Unreviewed dependency upgrades causing runtime regressions.
5. Hidden script side effects across workspace packages.
6. Ignoring transitive license/security risk.

## Do / Don't Examples
### 1. Reproducible CI
```text
Don't: npm install in CI for release builds.
Do:    npm ci with committed lockfile.
```

### 2. Package Manager Consistency
```text
Don't: package-lock.json and pnpm-lock.yaml in same repo.
Do:    choose one manager and enforce one lockfile.
```

### 3. Credential Safety
```text
Don't: commit .npmrc with auth token.
Do:    inject registry auth at CI runtime only.
```

## Code Review Checklist for Node Package Management
- Is exactly one package manager/lockfile used?
- Is runtime version pinned and CI install deterministic?
- Are dependency additions justified and license/security-reviewed?
- Are scripts explicit and side-effect aware?
- Are registry credentials kept out of source control?
- Are workspace boundaries and dependency graph changes intentional?

## Testing Guidance
- Run install in clean environment to validate lockfile determinism.
- Run vulnerability/license checks in CI.
- Run relevant build/test scripts from fresh install.
- Test workspace script execution for changed packages.
