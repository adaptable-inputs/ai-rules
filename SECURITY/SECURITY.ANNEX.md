---
applies_to:
  load: "annex"
  annex_of: "SECURITY.md"
  tasks: ["review", "test"]
---
# SECURITY - Annex

## High-Risk Pitfalls
1. Accepting user input without strict validation or context-aware encoding.
2. Storing credentials in code/config/scripts, plaintext CI config, or unencrypted/non-secret CI variables instead of
   the platform secret store.
3. Treating client-side checks as sufficient authorization.
4. Overly broad IAM/role permissions in runtime or CI.
5. Ignoring dependency vulnerabilities due to transitive complexity.
6. Returning detailed internal error content to external callers.
7. Logging secrets or sensitive personal data.
8. Disabling security checks for convenience without tracked exceptions.

## Do / Don't Examples
### 1. Authorization Boundary
```text
Don't: trust hidden UI controls or client checks as access control.
Do:    enforce authorization on trusted server-side boundaries.
```

### 2. Input Handling
```text
Don't: build SQL/HTML/shell output from raw user input strings.
Do:    validate at boundaries and use parameterized/context-encoded output.
```

### 3. Secrets and Logs
```text
Don't: log bearer tokens, passwords, or full sensitive payloads.
Do:    redact secrets and log only safe identifiers/reasons.
```

## Code Review Checklist
- Are all external inputs validated at trust boundaries?
- Is every output sink encoded for its own context (HTML body, HTML attribute, URL, JavaScript, CSS, SQL)?
- Are secrets absent from source, logs, snapshots, and examples?
- Is authorization enforced server-side with least-privilege semantics?
- Are dependency additions justified, maintained, and compliant?
- Are failure responses safe and non-leaky?
- Are security-sensitive actions auditable through logs/events?
- Are any security exceptions explicit, bounded, and documented?

## Testing Guidance for Security Risks
- Add negative tests for unauthorized/forbidden access paths.
- Add validation tests for malformed, boundary, and malicious inputs.
- Add tests ensuring sensitive fields are redacted in logs/errors.
- Add regression tests for previously found vulnerabilities.
- Validate dependency scanning and policy checks in CI where available.
- If threat model is high risk, include abuse-case tests for key flows.
