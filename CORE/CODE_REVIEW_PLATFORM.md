---
applies_to:
  load: "always"
  annex: "CODE_REVIEW_PLATFORM.ANNEX.md"
  purpose: "the protected-branch, merge-authority, and review-thread rules that hold regardless of hosting platform"
  inherits: ["CORE/VERSION_CONTROL_SYSTEM.md", "REVIEW/CODE_REVIEW.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "COMPLIANCE/COMPLIANCE.md", "CORE/GITHUB.md", "CORE/GITLAB.md"]
---
# CODE_REVIEW_PLATFORM

Platform-neutral delivery and review workflow contract shared by every code hosting platform.

## Terminology
- "change request" means a pull request (GitHub) or merge request (GitLab).
- "review thread" means a conversation (GitHub) or discussion (GitLab).
- Platform docs map these terms to their native vocabulary and do not restate the rules below.

## Protected Branch Policy (Mandatory)
- MUST treat protected branches as read-only for AI agents.
- MUST NOT push directly to protected branches.
- MUST use dedicated feature branches for implementation work.
- MUST create a change request for any change targeting a protected branch.

## Merge Authority and Merge Gates (Mandatory)
- Change-request creators MUST NOT merge their own change requests.
- The self-merge restriction MAY be bypassed only when all of the following are true:
  - The user gives explicit merge instruction for the specific change request.
  - The user explicitly confirms in the current session that they own the target
    repository and that they authorize bypassing the self-merge restriction.
  - MUST you, as an AI agent, treat the user as not a repository owner unless this explicit owner confirmation and
    authorization is present.
- If the above conditions are not met, MUST NOT attempt to merge a change request that you created or substantially
  authored.
- Respect all merge gates; MUST NOT bypass required checks, required reviews, approvals, or merge policies.
- MUST NOT use any privileged bypass path to skip required gates.
- MUST NOT merge without explicit user instruction.
- MUST NOT merge a change request while review threads are unresolved.
- If asked to merge with unresolved review threads, MUST stop and ask the user how to proceed because merge is not
  allowed in that state.

## Review Thread Ownership
- Only the author of a review comment MAY resolve that review thread.
- MUST NOT resolve review threads created by other reviewers. A platform doc MAY declare an explicit override that
  permits maintainer resolution under a stated downstream policy.
- If you authored the comment and the issue is fixed, SHOULD resolve that review thread.
- Keep review history intact; MUST NOT delete comments to hide unresolved work.

## Review Evidence
A review is evidence that someone looked, at a particular version. Deleting a thread destroys the evidence, and merging
after a fix push without a fresh review certifies a version nobody reviewed.

- MUST resolve a review thread rather than delete it. A deleted thread removes the record that the finding existed and
  that it was addressed.
- After pushing commits that address review findings, MUST obtain a fresh review of the resulting version before merge.
  An approval names the commit it approved, not the branch.
- MUST link a change request to the issue it closes before merge, so the issue's state follows the merge rather than a
  human remembering to close it.

## Change-Request Description Requirements
- When opening a change request, MUST include a short developer-focused implementation summary.
- MUST include the files reviewers can skim because they are generated, copied, or standard imports.
- MUST highlight non-obvious logic and explain why it is implemented that way.
- MUST keep scope, validation, and residual risk explicit.
- MUST reuse the general PR/MR summary template from `CORE/VERSION_CONTROL_SYSTEM.md`.

## Code Review Workflow
- MUST apply `REVIEW/CODE_REVIEW.md` severity-first process for every review.
- MUST place comments on precise affected lines, not only on the change-request overview.
- SHOULD use the platform's inline code-suggestion feature for small, localized fixes.
- If a requested fix is broader than a local suggestion, SHOULD offer to implement it in an AI-agent session on the
  existing branch.
- After offering broader implementation help, MUST wait for user confirmation before making branch changes.
