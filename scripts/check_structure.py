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

VALID_LOAD = {"always", "entry", "index", "conditional", "task", "setup", "never",
              "annex"}

# Classes an agent reads during ordinary project work. `setup` and `never` are
# read only when bootstrapping or maintaining ai-rules itself; `annex` is gated
# on the task.
LOADED_CLASSES = {"always", "entry", "index", "conditional", "task"}

# An annex holds only illustrative material. Between them these four sections
# contained 3 obligations across 1,563 bullets, and those were relocated before
# the split. Nothing else may live here, or a rule would hide outside the load.
ANNEX_SECTIONS = ("Do / Don't Examples", "High-Risk Pitfalls",
                  "Code Review Checklist", "Testing Guidance")
CONDITIONAL_KEYS = {"languages", "frameworks", "libraries", "tools", "when"}

# Docs whose normative bullets have been converted to explicit obligation
# keywords. This list only grows. Adding a file here locks it: a new
# keyword-less imperative in a normative section fails the build.
# See CORE/NORMATIVE_LANGUAGE.md.
KEYWORD_CONVERTED = {
    # Category indexes and the entry point. They were converted last, after the
    # restatement sections were removed and only real rules remained.
    "AI.md",
    "ARCHITECTURE/ARCHITECTURE.md",
    "BUILD_TOOLS/BUILD_TOOLS.md",
    "CI-CD/CI-CD.md",
    "COMPLIANCE/COMPLIANCE.md",
    "DESIGN/DESIGN.md",
    "FRAMEWORK/FRAMEWORK.md",
    "INFRASTRUCTURE/INFRASTRUCTURE.md",
    "LANGUAGE/LANGUAGE.md",
    "LIBRARY/LIBRARY.md",
    "REVIEW/REVIEW.md",
    "CORE/DEPENDENCY_SELECTION.md",
    "TEST/GUARDS.md",
    "TEST/WITHHELD_SUITES.md",
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
# Hyphenated verbs. Everything else with a hyphen ("Follow-up issue refs") is a
# noun phrase.
HYPHEN_VERBS = frozenset({"Co-locate", "Rate-limit", "Time-box", "Fail-fast"})

IMPERATIVE_VERBS = frozenset("""
Add Alert Align Allow Apply Assess Associate Assume Avoid Backfill Batch Be
Block Bound Cache Call Capture Centralize Check Choose Classify Clean Clone
Close Collect Combine Commit Compose Configure Control Convert Coordinate
Correlate Cover Create Declare Define Delete Deny Depend Deprecate Derive
Design Diff Disable Distinguish Document Drop Emit Enable Encode Enforce
Ensure Escalate Evaluate Export Expose Extract Fail Favor Fetch Fix Flag Focus
Follow Gate Generate Group Guard Handle Highlight Identify Ignore Implement
Include Inherit Inject Instrument Integrate Interpret Introduce Isolate Keep
Limit Link Log Maintain Make Map Mark Match Merge Minimize Mix Mock Model
Monitor Move Name Normalize Optimize Order Organize Paginate Parameterize Pass
Perform Pick Pin Place Prefer Preserve Prevent Prioritize Profile Promote
Propagate Propose Protect Provide Publish Push Put Quarantine Query Raise Rate
Reassess Reconstruct Record Redact Redesign Reduce Reject Release Rely Remove
Rename Replace Reply Report Require Reserve Reset Resolve Respect Restrict
Retrieve Retry Return Reuse Review Rotate Route Run Sanitize Scan Select
Separate Set Ship Specify Split Stabilize Start Store Strengthen Stub Support
Swallow Test Throw Timebox Track Treat Update Use Validate Verify Version
Watch Weaken Wrap
""".split())

KEYWORD = re.compile(r"\b(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\b")
TOP_BULLET = re.compile(r"^[-*] (.*)$")
# Headings whose bullets state facts, dependencies, or review questions.
DESCRIPTIVE_PREFIXES = (
    "Scope", "Semantic Dependencies", "Purpose", "Files", "Role in the Ruleset",
    "Terminology", "Authoring Notes", "Override Notes", "Layer Details",
    "Code Review Checklist", "Testing Guidance", "High-Risk", "Do / Don",
    "Keywords", "Default Force", "Conflicts", "Applying Keywords",
    "Validation Notes", "Authoring Checklist", "Plan Review Checklist",
    "Review Checklist", "Discouraged Uses", "Allowed Uses",
    "Appropriate AOP Use Cases", "Deep Technical Docs", "Pure Index Docs",
    "Redundancy and Override Policy", "Decision-Complete Plan Requirements",
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


def _applies_to(p: Path):
    """Parse frontmatter, or None. check_frontmatter reports the bad YAML."""
    src = p.read_text(encoding="utf-8")
    if not src.startswith("---\n"):
        return None
    end = src.find("\n---\n", 3)
    if end == -1:
        return None
    try:
        doc = yaml.safe_load(src[4:end])
    except yaml.YAMLError:
        return None
    if not isinstance(doc, dict):
        return None
    return doc.get("applies_to")


def annex_targets() -> set[str]:
    """Files named by another doc's `annex:` frontmatter field."""
    out = set()
    for p in md_files():
        if rel(p) in FRONTMATTER_EXEMPT:
            continue
        a = _applies_to(p)
        if not a:
            continue
        if a.get("annex"):
            out.add((p.parent / a["annex"]).resolve().relative_to(ROOT).as_posix())
    return out


def check_annex_contract() -> None:
    """An annex points back at its parent and holds only illustrative sections."""
    for p in md_files():
        if not p.name.endswith(".ANNEX.md"):
            continue
        r = rel(p)
        src = p.read_text(encoding="utf-8")
        a = _applies_to(p)
        if not a:
            continue  # already reported by check_frontmatter
        parent = p.parent / a.get("annex_of", "")
        if not parent.exists():
            fail(f"{r}: annex_of points at a missing file")
            continue
        pa = _applies_to(parent)
        if not pa:
            continue
        if pa.get("annex") != p.name:
            fail(f"{rel(parent)}: does not declare annex: {p.name!r}")
        for line in src.split("\n"):
            m = re.match(r"^## (.*)$", line)
            if m:
                sec = re.sub(r"\s+(for|in)\s+.*$", "", m.group(1)).strip()
                if not sec.startswith(ANNEX_SECTIONS):
                    fail(f"{r}: section {m.group(1)!r} does not belong in an annex")


def check_no_orphans() -> None:
    """Every md file is reachable via a markdown link from some other file."""
    linked: set[str] = set(annex_targets())
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
        if load == "annex":
            if not a.get("annex_of"):
                fail(f"load: annex needs annex_of: {r}")
            if not a.get("tasks"):
                fail(f"load: annex needs tasks: {r}")
        for g in a.get("globs", []) or []:
            if not isinstance(g, str):
                fail(f"glob parsed as {type(g).__name__}, quote it: {r}")
        # Semantic dependencies live here, not in prose. A broken parent
        # reference silently detaches a doc from its precedence chain.
        for t in a.get("inherits", []) or []:
            if not isinstance(t, str):
                fail(f"inherits entry parsed as {type(t).__name__}, quote it: {r}")
                continue
            target = ROOT / t[:-3] if t.endswith("/**") else ROOT / t
            if not target.exists():
                fail(f"{r}: inherits {t!r}, which does not exist")
        if "purpose" in a and not str(a["purpose"]).strip():
            fail(f"{r}: purpose is empty")
        # MANIFEST.md selects a conditional or task doc by its purpose, so a
        # missing one leaves an agent no basis to decide. `always` docs load
        # unconditionally and need none.
        if a.get("load") in {"conditional", "task"} and not a.get("purpose"):
            fail(f"{r}: load: {a['load']} requires a purpose; MANIFEST.md selects on it")


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


# Shapes that CORE/RULE_DEPENDENCY_TREE.md Core Principles already state once.
# A bullet matching OVERRIDE_KEEP declares a real override and is exempt.
OVERRIDE_KEEP = re.compile(
    r"\bexcept\b|\bnon-overridable\b|takes precedence|fallback only|"
    r"Explicit specialization|MUST also satisfy|^-\s*(If|When)\b", re.I)
OVERRIDE_PERMISSION = re.compile(
    r"\bMAY\b(?:(?!\bMUST\b).){0,200}?\b(be stricter|vary|specialize|narrow|refine|add|"
    r"prescribe|define|extend|impose|require|adjust|change|restrict|cover)\b", re.I | re.S)
OVERRIDE_CONCESSION = re.compile(
    r"\bremain(s)? (mandatory|in force|authoritative)\b|\bMUST keep\b|\bMUST still\b|"
    r"\bMUST remain compatible\b|\bMUST NOT (weaken|reduce|be weakened)\b|"
    r"stricter policy always wins", re.I)
OVERRIDE_PURPOSE = re.compile(r"^-\s*(This file\b|Baseline rule:)", re.I)


def check_override_notes() -> None:
    """`## Override Notes` may only describe an override the doc declares.

    Three bullet shapes are redundant with Core Principles, and the first two
    are self-contradicting: prose cannot grant a force the rule's own keyword
    withholds, and "specialized docs MAY be stricter" is stated once, globally.

    - permission: "Framework docs MAY narrow this baseline"
    - concession: "...but these constraints remain mandatory" / "MUST keep"
    - purpose:    "This file is the Java baseline" (now frontmatter `purpose`)

    `## Specialization Contract` was the index-doc spelling of the same thing.
    """
    for p in md_files():
        if p.name.endswith(".ANNEX.md"):
            continue
        meta = _applies_to(p)
        if not meta:
            continue
        text = p.read_text(encoding="utf-8")
        if re.search(r"^## Specialization Contract\b", text, re.M):
            fail(f"{rel(p)}: '## Specialization Contract' restates "
                 f"CORE/RULE_DEPENDENCY_TREE.md Core Principles; state the "
                 f"doc-specific rule under its own heading instead")
        # Loaded on every task that opened an index, and saying nothing the
        # frontmatter and RULE_DEPENDENCY_TREE.md do not already say.
        for banned, why in (("Role in the Ruleset", "restates RULE_DEPENDENCY_TREE.md layering"),
                            ("Scope Boundary", "restates the `purpose` frontmatter field"),
                            ("Authoring Notes", "is maintainer guidance; it belongs in AI-RULES/STRUCTURE.md")):
            if re.search(rf"^## {re.escape(banned)}\b", text, re.M):
                fail(f"{rel(p)}: '## {banned}' {why}")
        if meta.get("load") not in {"always", "conditional", "task"}:
            continue
        body = re.search(r"^## Override Notes\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not body:
            continue
        for raw in re.findall(r"^- .*(?:\n  \S.*)*", body.group(1), re.M):
            bullet = "- " + " ".join(raw[2:].split())
            if OVERRIDE_KEEP.search(bullet):
                continue
            for name, pat in (("purpose", OVERRIDE_PURPOSE),
                              ("permission", OVERRIDE_PERMISSION),
                              ("concession", OVERRIDE_CONCESSION)):
                if pat.search(bullet):
                    fail(f"{rel(p)}: Override Notes bullet restates the global "
                         f"{name} rule: {bullet[:60]}...")
                    break


# AI.md states the one legitimate use of this phrasing, as a prohibition.
EXHAUSTIVE_READ = re.compile(
    r"read(ing)? the complete ai-rules ruleset|complete ai-rules ruleset\" means|"
    r"MUST NOT skip reachable Markdown files|^## Ruleset Read Gate|"
    r"re-reads the complete ai-rules|complete-ruleset-read|"
    r"read every Markdown file", re.I | re.M)


def check_no_exhaustive_read() -> None:
    """No loaded doc may order an agent to read the ruleset exhaustively.

    Three task overlays once carried a `Ruleset Read Gate (Mandatory)` telling
    the agent to read every Markdown file reachable from AI.md and discard the
    irrelevant ones afterwards. AI.md says the opposite: "An agent MUST NOT read
    this ruleset exhaustively." Every task loads one of those overlays, so the
    gate silently defeated conditional loading and the annex split, at a cost of
    roughly 79,000 tokens per task.
    """
    for p in md_files():
        meta = _applies_to(p)
        if not meta or meta.get("load") not in LOADED_CLASSES:
            continue
        text = p.read_text(encoding="utf-8")
        if rel(p) == "AI.md":
            text = text.replace("MUST NOT read this ruleset exhaustively", "")
        m = EXHAUSTIVE_READ.search(text)
        if m:
            fail(f"{rel(p)}: mandates an exhaustive ruleset read "
                 f"({m.group(0)[:40]!r}); AI.md forbids it. Point at the "
                 f"AI.md Loading Protocol instead")


# Every doc that loads on EVERY task, and the authorization for it. `always` is a
# tax on all work, so it is granted, not assumed. A new doc defaults to
# `conditional`; promoting one to `always` means adding it here, deliberately.
ALWAYS_AUTHORIZED = {
    "CORE/NORMATIVE_LANGUAGE.md":   "an agent cannot read any keyword without it",
    "CORE/CORE.md":                 "the cross-cutting baseline every doc inherits",
    "CORE/RULE_DEPENDENCY_TREE.md": "precedence and conflict resolution for every doc",
    "CORE/VERSION_CONTROL_SYSTEM.md": "every change is committed",
    "CORE/LOGGING.md":              "log safety binds any code that emits a log line",
    "CORE/CODE_REVIEW_PLATFORM.md": "every change is reviewed",
    "COMPLIANCE/LICENSES.md":       "license compatibility binds every project",
    "DESIGN/CLEAN_CODE.md":         "applies to any code written",
    "DESIGN/COGNITIVE_COMPLEXITY.md": "applies to any code written",
    "DESIGN/EARLY_RETURN.md":       "applies to any code written",
    "DESIGN/SOLID.md":              "applies to any code written",
    "LANGUAGE/CONVENTIONS.md":      "applies to every language",
    "LANGUAGE/READABILITY.md":      "applies to every language",
    "SECURITY/SECURITY.md":         "security is not opt-in",
    "TEST/TEST.md":                 "every behaviour change is tested",
}


def check_always_is_authorized() -> None:
    """`load: always` is a tax on every task, and MUST be granted explicitly.

    A rule that governs a narrow situation belongs behind a `when` clause. Adding
    "Withheld Verification Suites" and "Guards Are Code" to TEST/TEST.md -- an
    always-loaded doc -- put 800 tokens of benchmark-isolation rules into every
    implementation task in every project. Both are now conditional docs.
    """
    for p in md_files():
        meta = _applies_to(p)
        if not meta or meta.get("load") != "always":
            continue
        r = rel(p)
        if r not in ALWAYS_AUTHORIZED:
            fail(f"{r}: load: always is unauthorized. Every task in every project "
                 f"pays for it. Use load: conditional with a `when` clause, or add "
                 f"{r} to ALWAYS_AUTHORIZED with the reason it governs all work")

    for r, reason in ALWAYS_AUTHORIZED.items():
        target = ROOT / r
        if not target.exists():
            fail(f"ALWAYS_AUTHORIZED names {r}, which does not exist")
            continue
        meta = _applies_to(target)
        if meta and meta.get("load") != "always":
            fail(f"ALWAYS_AUTHORIZED grants {r} but it is load: {meta.get('load')}; "
                 f"remove the stale grant")
        if len(reason.split()) < 4:
            fail(f"ALWAYS_AUTHORIZED[{r}] gives no reason it governs all work")


def check_no_rules_in_indexes() -> None:
    """An index navigates; it does not legislate.

    MANIFEST.md lists only `always`, `conditional` and `task` docs, and AI.md
    tells an agent not to open a category index. A keyworded bullet in an index
    is therefore a rule nothing loads. That regression stranded 18 obligations,
    including `MUST ensure licenses are compatible`, the moment the manifest
    replaced index-walking. A link line ("- [X.md](X.md) - ... MAY ...") is prose
    about a doc, not a rule, so link bullets are exempt.
    """
    for p in md_files():
        meta = _applies_to(p)
        if not meta or meta.get("load") != "index" or rel(p) == "MANIFEST.md":
            continue
        body = p.read_text(encoding="utf-8")
        body = body[body.find("\n---\n") + 5:] if body.startswith("---\n") else body
        for raw in re.findall(r"^- .*(?:\n  \S.*)*", body, re.M):
            bullet = " ".join(raw.split())
            if "](" in bullet:
                continue
            if KEYWORD.search(bullet):
                fail(f"{rel(p)}: index doc carries an obligation, which nothing "
                     f"loads: {bullet[:60]}... Move it to an always/conditional/"
                     f"task doc")


FAILSAFE = "or no compliance scope is declared"


def check_compliance_failsafe() -> None:
    """A regulation doc may be gated, but silence must never drop it.

    The five jurisdiction-specific regimes cost 2,167 tokens on every task in
    every project, including projects with no EU nexus. Gating them is right;
    gating them on a positive declaration is not, because an agent that fails to
    detect the project's jurisdiction would silently skip GDPR. Each `when`
    therefore also fires when nothing has been declared, so the pre-gating
    behaviour is what happens by default.

    `LICENSES.md` stays `always`: license compatibility binds every project.
    """
    comp = ROOT / "COMPLIANCE"
    if not comp.is_dir():
        fail("COMPLIANCE/ is missing")
        return
    for p in sorted(comp.glob("*.md")):
        if p.name.endswith(".ANNEX.md") or p.name == "COMPLIANCE.md":
            continue
        meta = _applies_to(p)
        if not meta:
            fail(f"{rel(p)}: unreadable frontmatter")
            continue
        if p.name == "LICENSES.md":
            if meta.get("load") != "always":
                fail(f"{rel(p)}: license policy binds every project; it must be load: always")
            continue
        if meta.get("load") != "conditional":
            continue  # a regime may legitimately be always-on
        when = str(meta.get("when", ""))
        if FAILSAFE not in when:
            fail(f"{rel(p)}: conditional compliance doc must also load when nothing "
                 f"is declared. Add {FAILSAFE!r} to its `when`, or an undetected "
                 f"jurisdiction silently skips this regime")


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
            w = re.match(r"([A-Z][a-z]+(?:-[a-z]+)?)", probe)
            if not w:
                continue
            tok = w.group(1)
            if "-" in tok:
                if tok not in HYPHEN_VERBS:
                    continue
            elif tok not in IMPERATIVE_VERBS:
                continue
            fail(f"{rel_path}:{n}: normative bullet has no obligation keyword "
                 f"(file is in KEYWORD_CONVERTED): {text[:60]!r}")


def main() -> int:
    check_indexes()
    check_ai_md_lists_dirs()
    check_no_orphans()
    check_frontmatter()
    check_preflight_readable()
    check_annex_contract()
    check_override_notes()
    check_no_exhaustive_read()
    check_compliance_failsafe()
    check_always_is_authorized()
    check_no_rules_in_indexes()
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
