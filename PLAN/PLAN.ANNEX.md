---
applies_to:
  load: "annex"
  annex_of: "PLAN.md"
  tasks: ["review", "test"]
---
# PLAN - Annex

## High-Risk Pitfalls
1. Plans that leave critical decisions to implementation time.
2. Ignoring semantic dependency order.
3. Missing verification criteria or measurable "done" definition.
4. Oversized steps with hidden complexity.
5. No rollback strategy for risky changes.
6. Untracked assumptions that later break execution.
7. Shallow research that misses better options or known constraints.

## Do / Don't Examples
### 1. Step Quality
```text
Don't: "Update docs and fix related stuff"
Do:    "Rewrite LANGUAGE/JAVA/JAVA.md with sections A/B/C; add tests X/Y"
```

### 2. Verification Clarity
```text
Don't: "Run tests"
Do:    "Run markdownlint for touched docs and report pass/fail output"
```

### 3. Dependency Order
```text
Don't: update framework child docs before parent language constraints.
Do:    update parent baselines first, then child specializations.
```
