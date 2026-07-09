---
applies_to:
  load: "annex"
  annex_of: "JIRA.md"
  tasks: ["review", "test"]
---
# JIRA - Annex

## High-Risk Pitfalls
1. Editing an existing ticket description without explicit request.
2. Posting detailed engineering internals instead of short summary bullets.
3. Omitting one or more related MRs/PRs from delivery summaries.
4. Missing PO/QA validation guidance.
5. Marking acceptance criteria complete without evidence.
6. Mixing assumptions and confirmed facts in status updates.

## Do / Don't Examples
### 1. Description Edits
```text
Don't: rewrite Jira description proactively "to make it cleaner".
Do:    keep description unchanged and post clarifications in a comment.
```

### 2. Summary Granularity
```text
Don't: provide long implementation internals in Jira status summary.
Do:    provide short bullets and link MRs/PRs for technical depth.
```

### 3. QA/PO Guidance
```text
Don't: "Ready for test" with no test focus.
Do:    include explicit PO outcomes and QA scenarios to validate.
```

## Code Review Checklist for Jira Updates
- Was existing description editing avoided unless explicitly requested?
- Are created/updated descriptions structured and testable?
- Are all related MRs/PRs listed in the summary?
- Are implementation bullets short and non-detailed?
- Are PO and QA validation hints explicit and actionable?
- Are acceptance criteria statuses traceable to delivered changes?

## Testing Guidance
- Validate every MR/PR link in Jira summaries.
- Validate acceptance criteria status against delivered artifacts.
- Validate PO/QA guidance covers primary and regression-sensitive flows.
- Validate ticket comments distinguish facts, assumptions, and blockers.
