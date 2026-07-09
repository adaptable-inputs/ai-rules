---
applies_to:
  load: "conditional"
  when: "code is hosted on GitLab"
  tools: ["gitlab"]
  annex: "GITLAB.ANNEX.md"
---
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
- MUST respect MR gates, including required checks and required approvals.
- MUST NOT use force-merge behavior to skip required gates.
- SHOULD use GitLab code suggestions for small, localized fixes.

## Review Thread Ownership
GitLab applies the baseline in `CORE/CODE_REVIEW_PLATFORM.md` without override:
only the author of a review comment MAY resolve that discussion. There is no
maintainer-resolution exception on GitLab.

## Override Notes
- Project-specific GitLab governance MAY be stricter. The baseline mandates in
  `CORE/CODE_REVIEW_PLATFORM.md` remain in force; GitLab declares no override.
