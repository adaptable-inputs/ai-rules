---
applies_to:
  load: "conditional"
  when: "the project tracks issues in Jira"
  tools: ["jira"]
  annex: "JIRA.ANNEX.md"
  purpose: "Jira-specific ticket-authoring, update, and summary-output rules"
  inherits: ["CORE/VERSION_CONTROL_SYSTEM.md", "TEST/TEST.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md"]
---
# JIRA

Guidance for AI agents creating and updating Jira tickets and Jira summaries.

## General Jira Guidance
- Keep ticket intent explicit: problem, scope, acceptance criteria, and validation focus.
- SHOULD keep descriptions structured and scannable; avoid large prose blocks.
- SHOULD keep acceptance criteria testable and observable.
- SHOULD keep language factual and implementation-neutral where possible.
- MUST link related code-delivery artifacts (branch, PR/MR, release notes) when reporting status.

## Ticket Description Edit Policy (Mandatory)
- MUST NOT edit descriptions of existing Jira tickets unless explicitly requested by the user, Product Owner, or another
  authorized requester.
- Without explicit request, MUST NOT rewrite or "improve" existing ticket descriptions.
- Without explicit request, MUST add clarifications/status in comments only.
- If a description appears wrong or incomplete, SHOULD propose changes in a comment and wait for explicit approval
  before editing the description.
- When explicit edit approval exists, SHOULD keep changes minimal, preserve original intent, and record what changed in
  a comment.

## Jira Ticket Description Templates
Use these templates when creating new Jira tickets or when explicitly asked to rewrite a description.

### 1. Story / Feature Template
```md
## Goal

## Problem Statement

## Scope
- In:
- Out:

## Acceptance Criteria
- [ ] AC1
- [ ] AC2

## Dependencies

## Risks

## PO Notes

## QA Notes
```

### 2. Bug Template
```md
## Problem Statement

## Impact
- Users affected:
- Severity:

## Reproduction Steps
1.
2.
3.

## Expected Result

## Actual Result

## Scope
- In:
- Out:

## Acceptance Criteria
- [ ] AC1
- [ ] AC2

## PO Notes

## QA Notes
```

### 3. Technical Debt / Refactor Template
```md
## Motivation

## Current Pain

## Scope
- In:
- Out:

## Success Criteria
- [ ] SC1
- [ ] SC2

## Risks and Mitigations

## Validation Plan

## PO Notes

## QA Notes
```

### 4. Spike / Research Template
```md
## Question to Answer

## Context

## Scope
- In:
- Out:

## Deliverables
- [ ] Decision summary
- [ ] Options considered
- [ ] Recommended next step

## Timebox

## PO Notes

## QA Notes
```

## Jira Summary Templates (Mandatory Fields)
- SHOULD keep implementation bullets short and non-detailed.
- SHOULD include all MRs/PRs in every delivery summary; do not omit partial or supporting merge requests.
- MUST include PO and QA guidance on what to validate.

### 1. Single-Ticket Delivery Summary
```md
## Delivery Summary
- Ticket: <JIRA-KEY>
- Status: <Done/In Review/Blocked>
- MRs/PRs:
  - <MR/PR-1 URL>
  - <MR/PR-2 URL>
- Implemented:
  - Short sentence 1.
  - Short sentence 2.
- Acceptance Criteria Status:
  - AC1: Done/Partial/Blocked
  - AC2: Done/Partial/Blocked
- PO Test Focus:
  - Business outcome to verify.
  - User-flow focus area.
- QA Test Focus:
  - Functional scenarios to test.
  - Negative/edge scenarios to test.
- Open Risks / Follow-ups:
  - Risk or follow-up item.
```

### 2. Multi-MR Consolidated Summary
```md
## Consolidated Implementation Summary
- Ticket: <JIRA-KEY>
- Included MRs/PRs:
  - <MR/PR-1 URL> - one short purpose sentence.
  - <MR/PR-2 URL> - one short purpose sentence.
  - <MR/PR-3 URL> - one short purpose sentence.
- Implemented (short bullets):
  - Short sentence 1.
  - Short sentence 2.
  - Short sentence 3.
- PO Validation Guide:
  - Business behavior expected after rollout.
  - Regression-sensitive area for acceptance.
- QA Validation Guide:
  - Core path checks.
  - Error-path and permission checks.
  - Data integrity checks.
- Residual Risks:
  - Remaining known risk.
```
