---
applies_to:
  load: "always"
---
# SECURITY

Guidance for AI agents implementing and reviewing security-relevant changes.

## Scope
Security is a non-negotiable baseline across all stacks and domains.

## Semantic Dependencies (Upstream Rules)
- Inherits `CORE/CORE.md` and `CORE/RULE_DEPENDENCY_TREE.md` precedence rules.
- Works with `COMPLIANCE/COMPLIANCE.md` and `COMPLIANCE/LICENSES.md` for legal
  and governance constraints.
- Testing expectations are supplemented by `TEST/TEST.md`.

## Security Defaults
- MUST use secure defaults and explicit allow-lists over broad allow-any behavior.
- MUST minimize attack surface: disable unused endpoints, ports, capabilities, and optional integrations by default.
- MUST apply least privilege to identities, tokens, credentials, and runtime roles.
- MUST fail closed on authentication/authorization checks.
- SHOULD prefer defense in depth (multiple controls) over single-point controls.

## Secrets and Credentials
- MUST NOT commit secrets to source control, docs, examples, logs, or test
  snapshots.
- MUST use secret managers or secure runtime injection.
- MUST rotate secrets on exposure, incident, or owner change.
- MUST keep secret scope minimal (short-lived, environment-specific, least-privilege).
- MUST redact secrets in logs, telemetry, and error messages.

## Authentication and Authorization
- MUST treat authentication (identity) and authorization (permissions) as separate controls.
- MUST enforce authorization at trusted boundaries, not only in client/UI paths.
- MUST validate token audience/issuer/expiry and reject malformed claims.
- MUST NOT rely on obscurity (hidden routes, client checks) as access control.
- MUST deny by default when user/role/context is ambiguous.

## Input, Output, and Data Protection
- MUST validate all external input at boundaries (API, file, queue, UI).
- SHOULD normalize and canonicalize inputs before policy checks when relevant.
- MUST use parameterized queries and safe encoders to prevent injection classes.
- MUST encode/escape output according to sink context (HTML, shell, URL, etc.).
- For SQL sinks, MUST use parameterized queries/bind variables as the primary defense rather than string escaping.
- MUST classify sensitive data and apply minimization, masking, and retention limits.

## Dependency and Supply-Chain Hygiene
- SHOULD prefer mature dependencies with active maintenance and clear ownership.
- MUST pin versions and commit lock files where the ecosystem supports it.
- MUST track vulnerability advisories and patch high/critical findings quickly.
- MUST require explicit justification for new runtime dependencies.
- SHOULD validate provenance/signatures where tooling supports it.

## Error Handling and Observability
- MUST NOT expose stack traces, internal identifiers, or secret material to
  untrusted callers.
- MUST return safe, actionable error responses without leaking internals.
- MUST log security-relevant events (auth failures, policy denials, suspicious activity) with safe redaction.
- MUST ensure security logging itself cannot crash request paths.

## High-Risk Pitfalls
1. Accepting user input without strict validation or context-aware encoding.
2. Storing credentials in code/config/scripts, plaintext CI config, or
   unencrypted/non-secret CI variables instead of the platform secret store.
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
- Is every output sink encoded for its own context (HTML body, HTML attribute,
  URL, JavaScript, CSS, SQL)?
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

## Override Notes
- Downstream docs MAY specialize controls for framework/runtime specifics, but
  MUST NOT weaken this baseline without explicit, reviewed rationale.
