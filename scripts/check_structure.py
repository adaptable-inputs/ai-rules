#!/usr/bin/env python3
"""Enforce the structural invariants AI-RULES/STRUCTURE.md declares.

markdownlint checks formatting and lychee checks that links resolve. Neither
catches a *missing* link, a category with no index, or malformed frontmatter.
This script does.

Exit 0 on success, 1 on any violation.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Files that are legitimately unreachable from AI.md.
LINK_ALLOWLIST = {
    "AI.md",                        # the entry point itself
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "AGENTS_TEMPLATE.md",
    ".github/copilot-instructions.md",  # loaded implicitly by GitHub
}

# Consumed verbatim by an external tool; frontmatter would leak into its prompt.
FRONTMATTER_EXEMPT = {".github/copilot-instructions.md"}

VALID_LOAD = {"always", "entry", "index", "conditional", "task", "setup", "never"}
CONDITIONAL_KEYS = {"languages", "frameworks", "libraries", "tools", "when"}

# Docs whose normative bullets have been converted to explicit obligation
# keywords. This list only grows. Adding a file here locks it: a new
# keyword-less imperative in a normative section fails the build.
# See CORE/NORMATIVE_LANGUAGE.md.
KEYWORD_CONVERTED = {
    "ARCHITECTURE/CIRCUIT_BREAKER.md",
    "ARCHITECTURE/CLEAN_ARCHITECTURE.md",
    "ARCHITECTURE/CQRS.md",
    "ARCHITECTURE/EVENT_DRIVEN_ARCHITECTURE.md",
    "ARCHITECTURE/GRAPHQL.md",
    "ARCHITECTURE/MICROSERVICE.md",
    "ARCHITECTURE/N_PLUS_1.md",
    "ARCHITECTURE/REST.md",
    "BUILD_TOOLS/BUN.md",
    "BUILD_TOOLS/GRADLE.md",
    "BUILD_TOOLS/MAVEN.md",
    "BUILD_TOOLS/NPM.md",
    "CI-CD/GITHUB_ACTIONS.md",
    "CI-CD/GITLAB.md",
    "COMPLIANCE/DORA.md",
    "COMPLIANCE/EPRIVACY_TTDSG.md",
    "COMPLIANCE/EU_AI_ACT.md",
    "COMPLIANCE/GDPR_BDSG.md",
    "COMPLIANCE/LICENSES.md",
    "COMPLIANCE/NIS2_KRITIS.md",
    "CORE/CODE_REVIEW_PLATFORM.md",
    "CORE/CONFLUENCE.md",
    "CORE/CORE.md",
    "CORE/GITHUB.md",
    "CORE/GITLAB.md",
    "CORE/JIRA.md",
    "CORE/LOGGING.md",
    "CORE/NORMATIVE_LANGUAGE.md",
    "CORE/RULE_DEPENDENCY_TREE.md",
    "CORE/VERSION_CONTROL_SYSTEM.md",
    "DESIGN/AOP.md",
    "DESIGN/CLEAN_CODE.md",
    "DESIGN/COGNITIVE_COMPLEXITY.md",
    "DESIGN/EARLY_RETURN.md",
    "DESIGN/GOF_DESIGN_PATTERNS.md",
    "DESIGN/SOLID.md",
    "FRAMEWORK/ANGULAR.md",
    "FRAMEWORK/IONIC.md",
    "FRAMEWORK/PRIMEFACES.md",
    "FRAMEWORK/REACT.md",
    "FRAMEWORK/SPRING_BOOT.md",
    "FRAMEWORK/SVELTE.md",
    "FRAMEWORK/TAILWIND_CSS.md",
    "INFRASTRUCTURE/ANSIBLE.md",
    "INFRASTRUCTURE/AWS.md",
    "INFRASTRUCTURE/AZURE.md",
    "INFRASTRUCTURE/CLOUDFORMATION.md",
    "INFRASTRUCTURE/DOCKER.md",
    "INFRASTRUCTURE/GCP.md",
    "INFRASTRUCTURE/HELM.md",
    "INFRASTRUCTURE/INFRA_AS_CODE.md",
    "INFRASTRUCTURE/ISTIO.md",
    "INFRASTRUCTURE/KUBERNETES.md",
    "INFRASTRUCTURE/PULUMI.md",
    "INFRASTRUCTURE/TERRAFORM.md",
    "LANGUAGE/CONVENTIONS.md",
    "LANGUAGE/CSS/CSS.md",
    "LANGUAGE/C_SHARP/C_SHARP.md",
    "LANGUAGE/GO/GO.md",
    "LANGUAGE/HTML/HTML.md",
    "LANGUAGE/JAVA/EFFECTIVE_JAVA.md",
    "LANGUAGE/JAVA/JAVA.md",
    "LANGUAGE/JAVASCRIPT/JAVASCRIPT.md",
    "LANGUAGE/KOTLIN/KOTLIN.md",
    "LANGUAGE/PHP/PHP.md",
    "LANGUAGE/PYTHON/PYTHON.md",
    "LANGUAGE/READABILITY.md",
    "LANGUAGE/RUBY/RUBY.md",
    "LANGUAGE/RUST/RUST.md",
    "LANGUAGE/SHELL/SHELL.md",
    "LANGUAGE/SQL/SQL.md",
    "LANGUAGE/SWIFT/SWIFT.md",
    "LANGUAGE/TYPESCRIPT/TYPESCRIPT.md",
    "LANGUAGE/YAML/YAML.md",
    "LIBRARY/GUAVA.md",
    "LIBRARY/JAVA_MONEY.md",
    "LIBRARY/JAXB.md",
    "LIBRARY/JEST.md",
    "LIBRARY/JOOQ.md",
    "LIBRARY/JPA.md",
    "LIBRARY/JUNIT.md",
    "LIBRARY/KAFKA.md",
    "LIBRARY/LOMBOK.md",
    "LIBRARY/MAPSTRUCT.md",
    "LIBRARY/MOCKITO.md",
    "LIBRARY/PLAYWRIGHT.md",
    "LIBRARY/RESILIENCE4J.md",
    "LIBRARY/SELENIUM.md",
    "PLAN/PLAN.md",
    "PROGRAMMING/PROGRAMMING.md",
    "REVIEW/CODE_REVIEW.md",
    "SECURITY/SECURITY.md",
    "TEST/TEST.md",
}

# "Xcode: `DerivedData/`, ..." - a label introducing a list, not a rule.
LABEL_BULLET = re.compile(r"^[A-Z][\w /.+-]{0,32}:")

# A normative bullet opens with a bare imperative verb. Noun phrases
# ("External API contracts...", "Tests executed...") are list items, and
# third-person verbs ("Inherits...") are statements of fact. Neither is an
# obligation. "Scope" and "Override" are deliberately absent: both appear as
# section names ("Scope and applicability", "Override notes ...") far more often
# than as rule verbs, and produced false positives.
# Extend this list when a new rule verb appears.
IMPERATIVE_VERBS = frozenset("""
Add Align Alert Apply Assess Avoid Be Block Bound Centralize Choose Classify
Collect Commit Compose Configure Control Cover Create Declare Define Delete Deny
Depend Design Diff Disable Distinguish Document Emit Encode Enforce Ensure
Escalate Evaluate Expose Extract Fail Flag Follow Gate Handle Highlight Ignore
Implement Include Inherit Interpret Introduce Isolate Keep Limit Link Log
Maintain Make Map Mark Merge Minimize Mix Mock Name Normalize Optimize Pin Place
Prefer Preserve Prevent Prioritize Propagate Provide Publish Push Put Quarantine
Reassess Redact Reduce Rely Remove Rename Replace Reply Report Require Reset
Resolve Respect Restrict Return Reuse Review Rotate Run Separate Set Ship Split
Start Store Strengthen Support Swallow Throw Track Treat Update Use Validate
Verify Weaken Wrap
""".split())

KEYWORD = re.compile(r"\b(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\b")
TOP_BULLET = re.compile(r"^[-*] (.*)$")
# Headings whose bullets state facts, dependencies, or review questions.
DESCRIPTIVE_PREFIXES = (
    "Scope", "Semantic Dependencies", "Purpose", "Files", "Role in the Ruleset",
    "Terminology", "Authoring Notes", "Override Notes", "Layer Details",
    "Code Review Checklist", "Testing Guidance", "High-Risk", "Do / Don",
    "Keywords", "Default Force", "Conflicts", "Applying Keywords",
    "Validation Notes", "Authoring Checklist",
)

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def md_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


NON_CATEGORY_DIRS = {"scripts", "node_modules"}


def category_dirs() -> list[Path]:
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
        and d.name not in NON_CATEGORY_DIRS
        and any(d.rglob("*.md"))
    )


def check_indexes() -> None:
    """Every category dir has an index named after the directory."""
    for d in category_dirs():
        idx = d / f"{d.name}.md"
        if not idx.exists():
            fail(f"missing category index: {rel(idx)}")


def check_ai_md_lists_dirs() -> None:
    """AI.md names every category directory."""
    ai = (ROOT / "AI.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^## ([A-Z_][A-Z0-9_-]*)$", ai, re.M))
    on_disk = {d.name for d in category_dirs()}
    for name in sorted(on_disk - listed):
        fail(f"category on disk but not listed in AI.md: {name}/")
    for name in sorted(listed - on_disk - {"Loading Protocol"}):
        fail(f"category listed in AI.md but absent on disk: {name}/")


def check_no_orphans() -> None:
    """Every md file is reachable via a markdown link from some other file."""
    linked: set[str] = set()
    for p in md_files():
        for target in re.findall(r"\]\(([^)#]+\.md)[^)]*\)", p.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://")):
                continue
            resolved = (p.parent / target).resolve()
            try:
                linked.add(resolved.relative_to(ROOT).as_posix())
            except ValueError:
                pass
    for p in md_files():
        r = rel(p)
        if r in LINK_ALLOWLIST or r in linked:
            continue
        fail(f"orphaned file, not linked from anywhere: {r}")


def check_frontmatter() -> None:
    """Every md file carries a well-formed applies_to block."""
    for p in md_files():
        r = rel(p)
        if r in FRONTMATTER_EXEMPT:
            continue
        src = p.read_text(encoding="utf-8")
        if not src.startswith("---\n"):
            fail(f"missing frontmatter: {r}")
            continue
        end = src.find("\n---\n", 3)
        if end == -1:
            fail(f"unterminated frontmatter: {r}")
            continue
        raw = src[4:end]
        try:
            doc = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            fail(f"invalid YAML frontmatter in {r}: {exc}")
            continue
        if not isinstance(doc, dict) or "applies_to" not in doc:
            fail(f"frontmatter missing applies_to: {r}")
            continue
        a = doc["applies_to"]
        load = a.get("load")
        if load not in VALID_LOAD:
            fail(f"invalid load={load!r} in {r} (expected one of {sorted(VALID_LOAD)})")
            continue
        if load == "conditional" and not (CONDITIONAL_KEYS & set(a)):
            fail(f"load: conditional needs a selector or when clause: {r}")
        if load == "never" and not a.get("reason"):
            fail(f"load: never needs a reason: {r}")
        if load == "setup" and not a.get("when"):
            fail(f"load: setup needs a when clause: {r}")
        for g in a.get("globs", []) or []:
            if not isinstance(g, str):
                fail(f"glob parsed as {type(g).__name__}, quote it: {r}")


def load_of(rel_path: str) -> str | None:
    p = ROOT / rel_path
    if not p.exists():
        return None
    src = p.read_text(encoding="utf-8")
    if not src.startswith("---\n"):
        return None
    end = src.find("\n---\n", 3)
    try:
        return yaml.safe_load(src[4:end])["applies_to"]["load"]
    except Exception:
        return None


def check_preflight_readable() -> None:
    """Files the setup preflight must read cannot be marked never-load.

    AGENTS_TEMPLATE.md lists target-version docs an agent MUST read before any
    subtree command. Marking one of them `load: never` makes the ruleset
    self-contradictory: required to read, forbidden to read.
    """
    tpl = ROOT / "AGENTS_TEMPLATE.md"
    if not tpl.exists():
        fail("AGENTS_TEMPLATE.md is missing")
        return
    text = tpl.read_text(encoding="utf-8")
    m = re.search(r"Read target-version docs:\n((?:\s*-\s*`[^`]+`\n)+)", text)
    if not m:
        fail("AGENTS_TEMPLATE.md: could not find the 'Read target-version docs' list")
        return
    named = re.findall(r"`([^`]+)`", m.group(1))
    if not named:
        fail("AGENTS_TEMPLATE.md: target-version doc list is empty")
    for rel_path in named:
        load = load_of(rel_path)
        if load is None:
            fail(f"preflight names {rel_path}, which has no readable frontmatter")
        elif load == "never":
            fail(f"preflight requires reading {rel_path}, but it is marked load: never")


def check_keyword_ratchet() -> None:
    """Converted docs may not regain a keyword-less normative imperative.

    Only top-level bullets are examined. Nested bullets are usually conditions
    under a lead-in ("...only when all of the following are true:"), and a
    condition is not an obligation.
    """
    for rel_path in sorted(KEYWORD_CONVERTED):
        p = ROOT / rel_path
        if not p.exists():
            fail(f"KEYWORD_CONVERTED names {rel_path}, which does not exist")
            continue
        lines = p.read_text(encoding="utf-8").split("\n")
        section = ""
        fence = False
        for n, line in enumerate(lines, 1):
            if line.startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            h = re.match(r"^#+\s+(.*)$", line)
            if h:
                section = h.group(1).strip()
                continue
            m = TOP_BULLET.match(line)
            if not m:
                continue
            # A bullet may wrap. Join its continuation lines before looking for
            # a keyword, or a SHOULD on the second line reads as absent.
            text = m.group(1)
            k = n  # 1-indexed; lines[k] is the line after this bullet
            while k < len(lines):
                nxt = lines[k]
                if not nxt.strip() or TOP_BULLET.match(nxt) or nxt.lstrip().startswith(("#", "```", "-", "*")):
                    break
                text += " " + nxt.strip()
                k += 1
            if KEYWORD.search(text):
                continue
            if section.startswith(DESCRIPTIVE_PREFIXES):
                continue
            # A bullet ending in ':' introduces nested content; a "Label:" bullet
            # introduces a list. Neither is an obligation.
            if text.rstrip().endswith(":") or LABEL_BULLET.match(text):
                continue
            # "If coverage targets are not met, document gaps" is a rule whose
            # verb sits after the condition. Look past the leading clause.
            probe = text
            lead = re.match(r"(?:If|When|For|Once|After|During|In)\b[^,]*, (.+)$", probe)
            if lead:
                probe = lead.group(1)
                probe = probe[0].upper() + probe[1:] if probe else probe
            # An imperative opens with a bare verb. "Follow-up issue refs" is a
            # noun phrase, so reject a hyphenated continuation.
            w = re.match(r"([A-Z][a-z]+)(-?)", probe)
            if not w or w.group(2) == "-" or w.group(1) not in IMPERATIVE_VERBS:
                continue
            fail(f"{rel_path}:{n}: normative bullet has no obligation keyword "
                 f"(file is in KEYWORD_CONVERTED): {text[:60]!r}")


def main() -> int:
    check_indexes()
    check_ai_md_lists_dirs()
    check_no_orphans()
    check_frontmatter()
    check_preflight_readable()
    check_keyword_ratchet()
    if errors:
        print(f"structure check FAILED with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    n = len(md_files())
    print(f"structure check passed: {n} files, {len(category_dirs())} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
