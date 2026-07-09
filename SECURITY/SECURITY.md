---
applies_to:
  load: "always"
  annex: "SECURITY.ANNEX.md"
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

## Override Notes
- Downstream docs MAY specialize controls for framework/runtime specifics, but
  MUST NOT weaken this baseline without explicit, reviewed rationale.
