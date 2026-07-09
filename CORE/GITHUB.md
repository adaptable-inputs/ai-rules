---
applies_to:
  load: "conditional"
  when: "code is hosted on GitHub"
  tools: ["github"]
  annex: "GITHUB.ANNEX.md"
---
# GITHUB

Guidance for AI agents using GitHub for branch protection, pull requests, and
review lifecycle rules.

## Scope
- Define GitHub-specific delivery and review workflow constraints.
- Apply this file when code hosting and review platform is GitHub.
- This file does not define GitHub Actions pipeline authoring rules; see
  `CI-CD/CI-CD.md` for CI/CD pipeline and workflow authoring guidance.

## Semantic Dependencies
- Inherit the full platform contract from `CORE/CODE_REVIEW_PLATFORM.md`.
  Protected-branch policy, merge authority, review-thread ownership, description
  requirements, and review workflow are defined there and are not restated here.
- This file specializes GitHub platform behavior and does not replace baseline
  VCS workflow requirements.

## Terminology Mapping
- "change request" is a pull request (PR).
- "review thread" is a conversation.

## GitHub Specializations
- MUST respect branch-protection and ruleset gates, including required status checks and required reviews.
- MUST NOT use admin bypass behavior to skip required gates.
- SHOULD use GitHub code suggestions for small, localized fixes.

## Explicit Override: Review Thread Ownership
`CORE/CODE_REVIEW_PLATFORM.md` permits only a comment's author to resolve its
review thread. On GitHub this file overrides that default as follows:
- SHOULD prefer the review-comment author to resolve their own conversation when
  possible.
- A maintainer MAY resolve another reviewer's conversation only when downstream
  policy explicitly allows maintainer resolution, or the reviewer has explicitly
  confirmed resolution in the current review context.

This override loosens the baseline. It applies to GitHub only and does not
extend to any other platform doc.

## Override Notes
- Project-specific GitHub governance MAY be stricter. The baseline mandates in
  `CORE/CODE_REVIEW_PLATFORM.md` remain in force except for the review-thread
  ownership override declared above.
