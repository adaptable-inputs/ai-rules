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


def category_dirs() -> list[Path]:
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name != "scripts"
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
        for g in a.get("globs", []) or []:
            if not isinstance(g, str):
                fail(f"glob parsed as {type(g).__name__}, quote it: {r}")


def main() -> int:
    check_indexes()
    check_ai_md_lists_dirs()
    check_no_orphans()
    check_frontmatter()
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
