#!/usr/bin/env python3
"""Verify every category index lists exactly the docs in its directory.

The one-line descriptions are hand-written and carry information the frontmatter
`purpose` does not, so this does not generate them. It verifies the three things
that silently rot: a new doc nobody linked, a link to a deleted file, and a
duplicate entry.

Annexes are deliberately absent from indexes: the parent names them in `annex:`,
and an index link would invite loading one outside its task.

    python3 scripts/check_indexes_accurate.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NON_CATEGORY_DIRS = {"scripts", "node_modules"}
LINK = re.compile(r"^- \[[^\]]+\]\(([^)]+)\)", re.M)

errors: list[str] = []


def category_dirs() -> list[Path]:
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
        and d.name not in NON_CATEGORY_DIRS and any(d.rglob("*.md"))
    )


def main() -> int:
    for d in category_dirs():
        index = d / f"{d.name}.md"
        if not index.exists():
            errors.append(f"{d.name}/: missing index {index.name}")
            continue

        # Every doc in the tree below, except the index itself and annexes.
        actual = {
            p.relative_to(d).as_posix() for p in d.rglob("*.md")
            if p != index and not p.name.endswith(".ANNEX.md")
        }
        if not actual:
            continue  # a single-doc category (TEST, PLAN) indexes nothing

        # A category may nest sub-indexes (AI-RULES/LESSONS_LEARNED). A doc counts
        # as listed when any index in the category links it. An index is a file
        # named after its own directory.
        indexes = [p for p in d.rglob("*.md") if p.stem == p.parent.name]
        seen: set[str] = set()
        for idx in indexes:
            text = idx.read_text(encoding="utf-8")
            # Duplicates only matter within one section: a doc may legitimately
            # appear in a prose exception list and again under `## Files`.
            for section in re.split(r"^## ", text, flags=re.M)[1:]:
                per_section: set[str] = set()
                for target in LINK.findall(section):
                    if target in per_section:
                        errors.append(f"{idx.relative_to(ROOT)}: duplicate entry {target}")
                    per_section.add(target)
            for target in LINK.findall(text):
                resolved = (idx.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"{idx.relative_to(ROOT)}: links to missing {target}")
                    continue
                if target.endswith(".ANNEX.md"):
                    errors.append(f"{idx.relative_to(ROOT)}: links to annex {target}; "
                                  f"an annex is reached through its parent's `annex:` field")
                seen.add(resolved.relative_to(d).as_posix())

        for m in sorted(actual - seen):
            errors.append(f"{index.relative_to(ROOT)}: does not list {m}")

    if errors:
        print(f"index accuracy check FAILED with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"index accuracy check passed: {len(category_dirs())} categories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
