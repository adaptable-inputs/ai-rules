---
applies_to:
  load: "always"
---
# CODE_REVIEW_PLATFORM

Platform-neutral delivery and review workflow contract shared by every code
hosting platform.

## Scope
- Define the protected-branch, merge-authority, and review-thread rules that
  hold regardless of hosting platform.
- Apply this file whenever code is hosted on a platform with branch protection
  and a review workflow.
- This file does not define CI pipeline authoring rules; see `CI-CD/CI-CD.md`.

## Terminology
- "change request" means a pull request (GitHub) or merge request (GitLab).
- "review thread" means a conversation (GitHub) or discussion (GitLab).
- Platform docs map these terms to their native vocabulary and do not restate
  the rules below.

## Semantic Dependencies
- Inherit baseline branch/PR/MR workflow rules from
  `CORE/VERSION_CONTROL_SYSTEM.md`.
- Inherit review quality expectations from `REVIEW/CODE_REVIEW.md`.
- Inherit security/testing/compliance gates from `SECURITY/SECURITY.md`,
  `TEST/TEST.md`, and `COMPLIANCE/COMPLIANCE.md`.
- Platform docs (`CORE/GITHUB.md`, `CORE/GITLAB.md`) specialize this file and do
  not replace baseline VCS workflow requirements.

## Protected Branch Policy (Mandatory)
- MUST treat protected branches as read-only for AI agents.
- MUST NOT push directly to protected branches.
- MUST use dedicated feature branches for implementation work.
- MUST create a change request for any change targeting a protected branch.

## Merge Authority and Merge Gates (Mandatory)
- Change-request creators MUST NOT merge their own change requests.
- The self-merge restriction MAY be bypassed only when all of the following are
  true:
  - The user gives explicit merge instruction for the specific change request.
  - The user explicitly confirms in the current session that they own the target
    repository and that they authorize bypassing the self-merge restriction.
  - MUST you, as an AI agent, treat the user as not a repository owner unless this explicit owner confirmation and
    authorization is present.
- If the above conditions are not met, MUST NOT attempt to merge a change request
  that you created or substantially authored.
- Respect all merge gates; MUST NOT bypass required checks, required reviews,
  approvals, or merge policies.
- MUST NOT use any privileged bypass path to skip required gates.
- MUST NOT merge without explicit user instruction.
- MUST NOT merge a change request while review threads are unresolved.
- MUST if asked to merge with unresolved review threads, stop and ask the user how to proceed because merge is not
  allowed in that state.

## Review Thread Ownership
- Only the author of a review comment MAY resolve that review thread.
- MUST NOT resolve review threads created by other reviewers. A platform doc MAY
  declare an explicit override that permits maintainer resolution under a stated
  downstream policy.
- SHOULD if you authored the comment and the issue is fixed, resolve that review thread.
- Keep review history intact; MUST NOT delete comments to hide unresolved work.

## Change-Request Description Requirements
- MUST when opening a change request, include a short developer-focused implementation summary.
- MUST include files reviewers may skim because they are generated, copied, or standard imports.
- MUST highlight non-obvious logic and explain why it is implemented that way.
- MUST keep scope, validation, and residual risk explicit.
- MUST reuse the general PR/MR summary template from `CORE/VERSION_CONTROL_SYSTEM.md`.

## Code Review Workflow
- MUST apply `REVIEW/CODE_REVIEW.md` severity-first process for every review.
- MUST place comments on precise affected lines, not only on the change-request overview.
- SHOULD use the platform's inline code-suggestion feature for small, localized fixes.
- SHOULD if a requested fix is broader than a local suggestion, offer to implement it in an AI-agent session on the
  existing branch.
- MUST after offering broader implementation help, wait for user confirmation before making branch changes.

## High-Risk Pitfalls
1. Direct pushes to protected branches.
2. Self-merging a change request without the explicit owner-authorized
   exception.
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
- Is work done on a dedicated feature branch targeting a protected branch
  through a change request?
- Were protected-branch and merge-gate rules enforced without bypass?
- Is merge authority valid for the acting user and instruction context?
- Are unresolved review threads blocking merge?
- Are review threads resolved only by their comment authors, or under a declared
  override?
- Does the change-request description include summary, skip candidates, and
  non-obvious rationale?

## Testing Guidance
- Verify branch protection and merge-gate configuration before merge actions.
- Verify required checks and required-review policies are active on the target
  branch.
- Verify review threads are fully resolved by authorized authors before merge.
- Verify change-request descriptions include reviewer-focused summary and risk
  notes.
- Verify no privileged bypass or force-merge path was used.

## Override Notes
- Project-specific governance MAY be stricter. Protected-branch discipline,
  unresolved review threads blocking merge, and merge-by-explicit-request
  behavior remain mandatory and MUST NOT be weakened.
