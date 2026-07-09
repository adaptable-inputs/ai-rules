---
applies_to:
  load: "annex"
  annex_of: "GITHUB.md"
  tasks: ["review", "test"]
---
# GITHUB - Annex

## High-Risk Pitfalls
1. Self-merging PRs without the explicit owner-authorized exception.
2. Resolving another reviewer's conversation with no explicit policy allowance.
3. Bypassing required checks/reviews using admin override paths.

## Do / Don't Examples
### 1. Merge Discipline
```text
Don't: merge your own PR because checks are green.
Do:    wait for explicit merge instruction and enforce all merge gates.
```

### 2. Admin Bypass
```text
Don't: use admin override to merge past a failing required check.
Do:    fix the check, or ask the user how to proceed.
```

## Code Review Checklist for GitHub Workflow
- Were branch-protection and ruleset gates enforced without admin bypass?
- Are conversation resolutions handled by the review-comment author, or under the override above?

## Testing Guidance
- Verify required checks and required-review policies are active on the target branch.
- Verify no admin-bypass merge path was used.
