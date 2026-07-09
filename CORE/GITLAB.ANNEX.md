---
applies_to:
  load: "annex"
  annex_of: "GITLAB.md"
  tasks: ["review", "test"]
---
# GITLAB - Annex

## High-Risk Pitfalls
1. Self-merging MRs without the explicit owner-authorized exception.
2. Resolving another reviewer's discussion.
3. Bypassing required MR gates or force-merging.

## Do / Don't Examples
### 1. Merge Discipline
```text
Don't: merge your own MR because pipeline is green.
Do:    wait for explicit merge instruction and enforce all MR gates.
```

### 2. Force Merge
```text
Don't: force-merge past a failing required pipeline.
Do:    fix the pipeline, or ask the user how to proceed.
```

## Code Review Checklist for GitLab Workflow
- Were MR gates enforced without force-merge?
- Are discussion resolutions owned by comment authors?

## Testing Guidance
- Verify branch protection and MR gate configuration before merge actions.
- Verify no force-merge or gate-bypass actions were used.
