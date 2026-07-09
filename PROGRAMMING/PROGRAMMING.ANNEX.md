---
applies_to:
  load: "annex"
  annex_of: "PROGRAMMING.md"
  tasks: ["review", "test"]
---
# PROGRAMMING - Annex

## High-Risk Pitfalls
1. Implementing without reading semantic parent rules.
2. Broad refactors bundled with feature changes.
3. Shipping behavior changes without tests.
4. Adding dependencies without compatibility/license review.
5. Silent security regressions due to missing boundary validation.
6. Incomplete change summaries hiding operational risk.

## Do / Don't Examples
### 1. Scope Control
```text
Don't: rewrite unrelated modules while fixing one endpoint bug.
Do:    keep fix scoped, create follow-up issue for broader refactor.
```

### 2. Verification
```text
Don't: merge behavior change with no tests or rationale.
Do:    add/adjust tests and report executed checks.
```

### 3. Dependency Introduction
```text
Don't: add convenience library without evaluation.
Do:    justify necessity, review license/security, and document impact.
```

## Code Review Checklist for Programming Tasks
- Does implementation align with semantic parent docs?
- Is change scope minimal and intentional?
- Are security/validation/error-handling boundaries correct?
- Are tests sufficient and relevant?
- Are dependency/tooling changes justified?
- Is change summary complete and actionable?

## Testing Guidance
- Follow full testing policy in `TEST/TEST.md`.
- Ensure changed behavior is covered by automated tests.
- Include negative/error-path tests for boundary logic.
- Include performance-sensitive checks where applicable.
