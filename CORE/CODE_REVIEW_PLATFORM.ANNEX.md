---
applies_to:
  load: "annex"
  annex_of: "CODE_REVIEW_PLATFORM.md"
  tasks: ["review", "test"]
---
# CODE_REVIEW_PLATFORM - Annex

## High-Risk Pitfalls
1. Direct pushes to protected branches.
2. Self-merging a change request without the explicit owner-authorized exception.
3. Resolving another reviewer's review thread without a declared override.
4. Merging while review threads are unresolved.
5. Bypassing required checks, reviews, or gates through a privileged path.
6. Change-request descriptions that hide generated files or non-obvious logic.

## Do / Don't Examples
### 1. Protected Branches
```text
Don't: push fix commits directly to a protected main branch.
Do:    create a feature branch and open a change request into it.
```

### 2. Merge Discipline
```text
Don't: merge your own change request because checks are green.
Do:    wait for explicit merge instruction and enforce all merge gates.
```

### 3. Review Thread Ownership
```text
Don't: resolve a review thread you did not author.
Do:    reply with the fix, then let the comment author resolve it.
```

## Code Review Checklist
- Is work done on a dedicated feature branch targeting a protected branch through a change request?
- Were protected-branch and merge-gate rules enforced without bypass?
- Is merge authority valid for the acting user and instruction context?
- Are unresolved review threads blocking merge?
- Are review threads resolved only by their comment authors, or under a declared override?
- Does the change-request description include summary, skip candidates, and non-obvious rationale?

## Testing Guidance
- Verify branch protection and merge-gate configuration before merge actions.
- Verify required checks and required-review policies are active on the target branch.
- Verify review threads are fully resolved by authorized authors before merge.
- Verify change-request descriptions include reviewer-focused summary and risk notes.
- Verify no privileged bypass or force-merge path was used.
