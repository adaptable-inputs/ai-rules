---
applies_to:
  load: "annex"
  annex_of: "CONFLUENCE.md"
  tasks: ["review", "test"]
---
# CONFLUENCE - Annex

## High-Risk Pitfalls
1. Writing Confluence content without explicit user instruction.
2. Treating implied requests as write authorization.
3. Applying non-revertible content changes.
4. Rewriting or deleting wiki history.
5. Deleting wiki pages directly or by automation.
6. Attempting to honor user requests that violate the non-overridable no-delete rule.

## Do / Don't Examples
### 1. Default Interaction
```text
Don't: update a Confluence page just because related code changed.
Do:    keep Confluence read-only unless user explicitly asks to write.
```

### 2. Delete Requests
```text
Don't: delete a Confluence page after receiving a direct instruction.
Do:    deny deletion and instruct the user to delete the page manually.
```

### 3. Revertibility and History
```text
Don't: apply a change that cannot be reverted or removes page history.
Do:    deny non-revertible changes and keep history intact for rollback.
```

## Code Review Checklist for Confluence Rules
- Is Confluence treated as read-only unless explicit write request exists?
- Are non-revertible change requests denied?
- Is wiki history preserved (no rewrite/squash/purge actions)?
- Are all delete actions denied without exception?
- Does the implementation avoid ambiguous implied write permissions?
- Is user messaging explicit when denying non-overridable delete requests?

## Testing Guidance
- Test that read-only behavior is the default path.
- Test that explicit write requests are required before any Confluence update.
- Test that non-revertible change requests are rejected.
- Test that history-rewrite or history-delete actions are rejected.
- Test that delete requests are rejected even with explicit user instruction.
- Test that denial messaging clearly instructs user-managed deletion.
