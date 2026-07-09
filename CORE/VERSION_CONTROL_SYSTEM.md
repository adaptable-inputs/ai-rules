---
applies_to:
  load: "always"
---
# VERSION_CONTROL_SYSTEM

Guidance for version control system usage (Git and others).

## Commit Messages
- MUST include the ticket or issue identifier and ticket/issue title
  (or a concise equivalent summary aligned with that title).
- Example format: `<ticket-or-issue-id> <ticket-or-issue-title>: <change>`.
- MAY add optional context about what changed and why when it improves clarity.
- MUST mark breaking changes explicitly.

## Branch and PR/MR Workflow
- MUST follow this execution order for implementation concerns:
  `plan -> dedicated branch -> implement -> PR/MR -> review -> merge (if permitted, typically by maintainers)`.
- MUST link each implementation concern to one issue/ticket and keep branch/PR/MR scope aligned to that single concern.
- MUST create a dedicated branch for each new concern being implemented (usually one issue/ticket).
- MUST keep each branch scoped to that single concern.
- SHOULD push successful intermediate states to VCS so progress stays recoverable.
- MUST NOT push knowingly non-working code unless this is explicitly requested.
- MUST create a PR/MR for implementation work before reporting completion when you have access to GitHub, GitLab, or a
  similar review system.
- When opening a PR/MR, MUST auto-detect the target branch from downstream-project rules when available; otherwise ask
  which target branch to use and suggest the most likely one.
- If you cannot create the branch or PR/MR due to permission/tooling constraints, MUST stop and report `BLOCKED` with
  the concrete reason instead of bypassing the workflow.
- When merge permission is not available, the hand-off point is a review-ready PR/MR and completion SHOULD be reported
  via the completion status contract.

## PR/MR and Issue Tracker Summaries
- When creating a PR/MR, MUST include an implementation summary aimed at code reviewers.
- If you have access to the review platform, MUST add that summary directly to the PR/MR description or comment thread.
- MUST also provide a short bullet-point summary on the linked issue/ticket for Product Owners, Code Reviewers, and
  Testers/QA.
- If you have access to the issue tracker, MUST add that summary directly to the linked issue/ticket.

## Completion Status Contract
- Final delivery for implementation work MUST include:
  - `Plan:`
  - `Issue/Ticket:`
  - `Branch:` (or `Branch: BLOCKED` / `Branch: N/A` when branch creation is not
    possible; explain the reason under `BLOCKED: <reason>`)
  - `PR/MR:` (or `BLOCKED: <reason>` when the PR/MR and/or branch cannot be
    created)
  - `Validation:`
- MUST use platform-neutral `PR/MR` wording in shared guidance.

## PR/MR Review Comment Handling
- MUST evaluate every review comment and explicitly judge whether it is valid or not for the current scope.
- MUST reply to every review comment with a respectful, concrete response. Do not leave actionable comments unanswered.
- If the comment is valid:
  - MUST apply the fix in the same PR/MR unless it widens the PR's stated scope.
  - MUST if not fixed immediately, create or link a follow-up issue/ticket and explain why deferral is acceptable.
- If the comment is not valid, MUST explain the reasoning with project-specific context and keep the tone factual and
  professional.
- Once the comment is addressed, MUST mark the relevant review thread as resolved, but first check downstream project
  rules for ownership (for example whether the author or reviewer is expected to mark threads resolved).
- MUST NOT mark a review thread or conversation resolved by deleting discussion; keep decisions auditable in the comment
  thread.

### PR/MR Summary Template (Code Reviewer Audience)
```md
## Implementation Summary
- Scope:
- Key changes:
- Non-goals:

## Review Focus
- Generated/copied files and standard imports that can be skimmed:
- Non-obvious code paths and rationale:

## Validation
- Tests executed:
- Manual checks:
- Residual risks:
```

### Issue Tracker Summary Template (PO/Reviewer/QA Audience)
```md
- Delivered:
- Acceptance criteria status:
- Validation status:
- QA notes / test focus:
- Open risks or follow-ups:
```

## Dependency Lock Files
- MUST commit dependency lock files for the package managers used by the project
  (for example `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`).
- MUST NOT add ignore rules that exclude required lock files from VCS.
- In CI, MUST install dependencies from lock files in frozen/immutable mode when supported by the package manager.
- Exceptions MAY be made only when explicitly documented
  (for example, intentionally published libraries that choose not to commit lock files).

## Ignore File
- MUST maintain a VCS ignore file in the repository root (for Git: `.gitignore`).
- SHOULD keep the ignore list minimal but practical to prevent VCS pollution and protect sensitive files.
- SHOULD start from a baseline set, then add one entry per tool or build output the project actually produces.
- MUST remove or override entries if the repository intentionally versions those files.

### Minimal Must-Have Ignores
Secrets
- `.env`, `.env.*` (except `.env.example`)
- `.envrc`
- `*.key`, `*.pem`, `*.p12`, `*.pfx`
- `*.jks`, `*.keystore`

OS and editor noise
- `.DS_Store`, `Thumbs.db`, `Desktop.ini`
- `*.swp`, `*.swo`, `*~`
- `.idea/`, `.vscode/`

Build output, dependencies, caches, logs
- `target/`, `build/`, `dist/`, `out/`
- `node_modules/`
- `.gradle/`
- `__pycache__/`, `*.pyc`, `.pytest_cache/`
- `.npm/`, `.yarn/`, `.pnpm-store/`
- `coverage/`, `.nyc_output/`, `htmlcov/`
- `*.log`, `logs/`
- `tmp/`, `*.tmp`, `*.cache`
- `*.class`

## Language/Framework/Library/Build Tool Additions
- If a language/framework/library/build tool doc includes a "VCS Ignore Additions" section, MUST add those patterns when
  using it.
- MUST keep additions scoped to generated output and local tooling noise.
- MUST NOT ignore files that are meant to be versioned for reproducible builds.

## IDE/Tooling Additions
Apply only when the tool is used:
- Xcode: `DerivedData/`, `*.xcworkspace`, `*.xcuserdatad`, `*.xcuserdata/`, `*.xcuserstate`, `*.xccheckout`
- Visual Studio: `.vs/`, `*.suo`, `*.user`, `*.userosscache`, `*.sln.docstates`, `*.VC.db`, `*.VC.opendb`
- Android Studio: `*.iml`, `local.properties`, `captures/`, `.externalNativeBuild/`
  (plus `.idea/`, `.gradle/`, `build/` if not already)

## Safeguards
- MUST NOT commit secrets; rotate and remove them from history if exposed.
- MUST review ignore rules when adding new tools to avoid accidental leaks.
