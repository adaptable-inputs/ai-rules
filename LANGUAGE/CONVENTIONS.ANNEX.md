---
applies_to:
  load: "annex"
  annex_of: "CONVENTIONS.md"
  tasks: ["review", "test"]
---
# CONVENTIONS - Annex

## High-Risk Pitfalls
1. Project-specific naming that contradicts language standards.
2. Inconsistent acronym casing across files/modules.
3. Generic names that hide domain meaning.
4. Unit-less numeric names causing interpretation errors.
5. Formatter drift from manual edits and inconsistent tool usage.
6. Naming collisions where different concepts share same identifier stem.

## Do / Don't Examples
### 1. Abbreviation Casing
```text
JS/TS/Java example:
Don't: getURL(), parseXML(), userID
Do:    getUrl(), parseXml(), userId

Language-style exception:
If a language/style guide mandates all-caps initialisms, follow that standard.
```

### 2. Unit Clarity
```text
Don't: retryTimeout = 5
Do:    retryTimeoutSeconds = 5
```

### 3. Prefer Semantic Type (Temporal)
```text
Don't: long timeoutMs = 5000;
Do:    Duration timeout = Duration.ofSeconds(5);
```

### 4. Prefer Semantic Type (Non-Temporal)
```text
Don't: String orderId;
Do:    OrderId orderId;
```

### 5. Generic Naming
```text
Don't: process(data)
Do:    processInvoiceBatch(invoiceBatch)
```

## Code Review Checklist for Conventions
- Are language-standard formatting and naming rules followed?
- Are naming decisions descriptive and consistent within module scope?
- Are abbreviations necessary and consistently cased?
- Are booleans/predicates named semantically?
- Are semantic/domain types preferred over raw basic types where feasible?
- Are unavoidable numeric/time fields unit-explicit?
- Are multiline formatting and trailing delimiter rules applied consistently?
- Did refactors keep identifier names aligned across code/comments/docs?
