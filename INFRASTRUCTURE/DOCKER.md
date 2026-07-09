---
applies_to:
  load: "conditional"
  when: "a Dockerfile or compose file is present"
  tools: ["docker"]
  globs: ["**/Dockerfile", "**/compose.yaml"]
  annex: "DOCKER.ANNEX.md"
---
# DOCKER

Guidance for AI agents implementing and reviewing Docker containerization.

## Scope
- Define secure, reproducible, and efficient container build/runtime rules.
- Apply this file to Dockerfiles and container runtime configuration.

## Semantic Dependencies
- Inherit security constraints from `SECURITY/SECURITY.md`.
- Inherit build reproducibility constraints from `BUILD_TOOLS/BUILD_TOOLS.md`.
- Inherit infrastructure constraints from `INFRASTRUCTURE/INFRASTRUCTURE.md`.

## Defaults
- SHOULD use multi-stage builds for production images.
- MUST pin base image versions/digests intentionally.
- SHOULD keep runtime images minimal and dependency-scoped.
- SHOULD run as non-root user by default.
- SHOULD keep image build deterministic and cache-friendly.

## Dockerfile Hygiene
- SHOULD order layers for cache efficiency (dependencies before changing sources).
- SHOULD minimize `COPY . .`; copy only required files per stage.
- SHOULD keep build-time and runtime dependencies separated.
- SHOULD use explicit `WORKDIR`, `USER`, and `ENTRYPOINT`/`CMD` semantics.
- SHOULD avoid shell form when exec form is clearer/safer.

## Security Baseline
- MUST NOT bake secrets into images or layers.
- MUST use runtime secret injection and environment-specific provisioning.
- SHOULD remove package-manager caches and temporary build artifacts.
- MUST keep CVE scanning in CI for base and app layers.
- MUST drop unnecessary Linux capabilities at runtime where platform allows.

## Runtime and Operability
- SHOULD add health checks when service behavior allows meaningful probes.
- SHOULD keep graceful shutdown behavior compatible with container orchestration.
- SHOULD log to stdout/stderr for platform aggregation.
- SHOULD keep timezone/locale behavior explicit when domain-critical.

## Performance and Size
- SHOULD keep final image size controlled; remove unused tooling/binaries.
- SHOULD prefer distroless/slim bases when compatibility permits.
- SHOULD avoid unnecessary layer churn that invalidates cache frequently.

## Override Notes
- Kubernetes/Helm/Istio docs MAY define runtime orchestration policies, but
  image hardening and reproducibility constraints here remain mandatory.
