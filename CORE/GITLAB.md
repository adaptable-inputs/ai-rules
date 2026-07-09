---
applies_to:
  load: "conditional"
  when: "code is hosted on GitLab"
  tools: ["gitlab"]
  annex: "GITLAB.ANNEX.md"
  purpose: "GitLab-specific delivery and review workflow constraints"
  inherits: ["CORE/CODE_REVIEW_PLATFORM.md"]
---
# GITLAB

Guidance for AI agents using GitLab for branch protection, merge requests, and
review lifecycle rules.

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
