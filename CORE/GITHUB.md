---
applies_to:
  load: "conditional"
  when: "code is hosted on GitHub"
  tools: ["github"]
  annex: "GITHUB.ANNEX.md"
  purpose: "GitHub-specific delivery and review workflow constraints"
  inherits: ["CORE/CODE_REVIEW_PLATFORM.md"]
---
# GITHUB

Guidance for AI agents using GitHub for branch protection, pull requests, and
review lifecycle rules.

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
