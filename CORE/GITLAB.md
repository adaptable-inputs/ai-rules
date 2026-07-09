# GITLAB

Guidance for AI agents using GitLab for branch protection, merge requests, and
review lifecycle rules.

## Scope
- Define GitLab-specific delivery and review workflow constraints.
- Apply this file when the code hosting and review platform is GitLab.
- This file does not define GitLab CI pipeline authoring rules; see
  `CI-CD/CI-CD.md` for CI/CD pipeline and job authoring guidance.

## Semantic Dependencies
- Inherit the full platform contract from `CORE/CODE_REVIEW_PLATFORM.md`.
  Protected-branch policy, merge authority, review-thread ownership, description
  requirements, and review workflow are defined there and are not restated here.
- This file specializes GitLab platform behavior and does not replace baseline
  VCS workflow requirements.

## Terminology Mapping
- "change request" is a merge request (MR).
- "review thread" is a discussion.

## GitLab Specializations
- Respect MR gates, including required checks and required approvals.
- Do not use force-merge behavior to skip required gates.
- Use GitLab code suggestions for small, localized fixes.

## Review Thread Ownership
GitLab applies the baseline in `CORE/CODE_REVIEW_PLATFORM.md` without override:
only the author of a review comment may resolve that discussion. There is no
maintainer-resolution exception on GitLab.

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

## Override Notes
- Project-specific GitLab governance may be stricter. The baseline mandates in
  `CORE/CODE_REVIEW_PLATFORM.md` remain in force; GitLab declares no override.
