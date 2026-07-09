#!/usr/bin/env python3
"""Unwrap handwritten prose so an agent pays no tokens for line breaks.

Effort is measured as the tokens required to evaluate the text. A hard line
break inside a paragraph or a bullet is whitespace: Markdown renders it as a
single space, so it carries no meaning, yet a `\\n  ` continuation costs real
tokens. Across the loaded corpus that is 1,049 tokens of pure formatting.

By contrast, every classic "wordiness" rewrite measured against this corpus
(`in order to` -> `to`, `for example` -> `e.g.`, ...) saves 27 tokens in total,
and several change meaning. This script therefore reflows and rewrites nothing
else: it is the only prose transform with a real payoff and a proof of safety.

SAFETY. Every changed block is checked twice before it is written:

  1. Inline equality - the block's text with all runs of whitespace collapsed
     must be byte-identical before and after. Unwrapping cannot pass this check
     while dropping, adding, or reordering a single character.
  2. Obligation fingerprint - the ordered RFC 2119 keywords, negations,
     conditionals, backticked identifiers, links, and numbers must match.

Failing either check aborts the run without writing. A hook that silently
rewrites a normative sentence is worse than no hook.

Skipped: frontmatter, fenced code, tables, block quotes, headings, and any line
ending in two spaces (an intentional hard break).

    python3 scripts/fmt_prose.py           # rewrite in place
    python3 scripts/fmt_prose.py --check   # exit 1 if any file would change
"""
from __future__ import annotations

import glob
import re
import sys

KEYWORD = re.compile(r"\b(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY NOT|MAY)\b")
COND = re.compile(r"\b(if|when|unless|until|where|once|after|before|while)\b", re.I)
NEG = re.compile(r"\b(not|never|no|none|cannot|without)\b", re.I)
CODE = re.compile(r"`[^`]+`")
LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
NUM = re.compile(r"\b\d+(?:\.\d+)?\b")

BULLET = re.compile(r"^(\s*)([-*]|\d+\.)\s")
WIDTH = 120  # markdownlint MD013


SPAN = re.compile(r"`[^`\n]*`")


def inline(text: str) -> str:
    """Collapse runs of whitespace, but never inside a code span, and never
    introduce whitespace that was not there.

    A code span is verbatim: two spaces inside one are significant, and squeezing
    them rewrites the code it documents (markdownlint MD038 caught that).
    Equally, joining segments with a space turns [`X`] into [ `X` ] (MD039). So
    this copies spans byte-for-byte and only ever shortens existing whitespace.
    """
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch == "`":
            end = text.find("`", i + 1)
            if end != -1 and "\n" not in text[i:end]:
                out.append(text[i:end + 1])
                i = end + 1
                continue
        if ch.isspace():
            j = i
            while j < len(text) and text[j].isspace():
                j += 1
            out.append(" ")
            i = j
            continue
        out.append(ch)
        i += 1
    return "".join(out).strip()


def fingerprint(text: str) -> tuple:
    """Everything that decides what a rule obliges. Must survive a reflow.

    Computed on the normalized text: a fingerprint of the physical layout would
    flag a code span that merely moved across a line boundary.
    """
    text = inline(text)
    return (
        tuple(KEYWORD.findall(text)),
        tuple(m.lower() for m in COND.findall(text)),
        tuple(m.lower() for m in NEG.findall(text)),
        tuple(CODE.findall(text)),
        tuple(LINK.findall(text)),
        tuple(NUM.findall(text)),
    )


def atoms(text: str) -> list[str]:
    """Split `text` (already inlined) into units a line break must not split.

    Wrapping inside `git subtree add --prefix ...` or inside a [text](link)
    corrupts it, and a code span's interior spaces are significant. Scanning
    keeps each span verbatim; joining the atoms with single spaces reproduces
    `text` exactly.
    """
    out: list[str] = []
    i, cur = 0, ""
    while i < len(text):
        ch = text[i]
        if ch == "`":
            end = text.find("`", i + 1)
            if end != -1:
                cur += text[i:end + 1]
                i = end + 1
                continue
        if ch == " ":
            # A space inside an unclosed link keeps the link one atom.
            if cur and (cur.count("[") != cur.count("]")
                        or cur.count("(") != cur.count(")")):
                cur += ch
                i += 1
                continue
            if cur:
                out.append(cur)
                cur = ""
            i += 1
            continue
        cur += ch
        i += 1
    if cur:
        out.append(cur)
    return out


FENCE_BLOCK = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.M | re.S)


SPAN_ANY = re.compile(r"`[^`]*`", re.S)
LINE_JOIN = re.compile(r"\n[ \t]*")


def code_units(text: str) -> tuple[list[str], list[str]]:
    """Every fenced block, and every inline code span with line joins applied.

    A span wrapped across two source lines renders as one space, so rejoining it
    is faithful. Intra-line spacing is left alone: two spaces inside a span are
    significant, and squeezing them rewrites the code (markdownlint MD038).
    """
    spans = [LINE_JOIN.sub(" ", s) for s in SPAN_ANY.findall(text)]
    return FENCE_BLOCK.findall(text), spans


def code_intact(before: str, after: str) -> bool:
    """No snippet may be reflowed, reindented, or respaced.

    Reflowing once joined four shell commands into one line, and once squeezed
    two significant spaces inside a code span. Both were caught downstream, by a
    linter, not by this script. Now they cannot be written at all.
    """
    fb, sb = code_units(before)
    fa, sa = code_units(after)
    return fb == fa and sb == sa


def safe(before: str, after: str) -> bool:
    return (inline(before) == inline(after)
            and fingerprint(before) == fingerprint(after)
            and code_intact(before, after))


def reflow(lines: list[str]) -> list[str]:
    """Join a wrapped block onto as few lines as MD013 allows."""
    m = BULLET.match(lines[0])
    if m:
        indent, marker = m.group(1), m.group(2)
        head = f"{indent}{marker} "
        cont = indent + " " * (len(marker) + 1)
        text = inline(lines[0][m.end():] + " " + " ".join(l.strip() for l in lines[1:]))
    else:
        head = cont = ""
        text = inline(" ".join(lines))

    assert " ".join(atoms(text)) == text, f"atoms() lost information in: {text!r}"

    out, cur = [], ""
    for word in atoms(text):
        cand = f"{cur} {word}" if cur else head + word
        if cur and len(cand) > WIDTH:
            out.append(cur)
            cur = cont + word
        else:
            cur = cand
    out.append(cur)
    return out


def blocks(body: str):
    """Yield (start, end) spans of reflowable blocks in `body.split('\\n')`."""
    lines = body.split("\n")
    i, fence = 0, False

    def is_fence(s: str) -> bool:
        # A fence inside a list item is indented; matching only column 0 once
        # tried to reflow four shell commands into one line.
        return s.lstrip().startswith(("```", "~~~"))

    def is_break(s: str) -> bool:
        return (not s.strip() or is_fence(s) or s.lstrip().startswith(("#", ">", "|"))
                or s.endswith("  ") or s.startswith("    "))

    while i < len(lines):
        ln = lines[i]
        if is_fence(ln):
            fence = not fence
            i += 1
            continue
        if fence or is_break(ln):
            i += 1
            continue

        start = i
        is_bullet = bool(BULLET.match(ln))
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if is_break(nxt) or BULLET.match(nxt):
                break                      # a new list item starts its own block
            if is_bullet and not nxt.startswith(" "):
                break                      # unindented line is not a continuation
            if not is_bullet and nxt.startswith(" "):
                break                      # indented line under a paragraph
            i += 1
        yield start, i


def process(path: str) -> tuple[str, int]:
    src = open(path, encoding="utf-8").read()
    if src.startswith("---\n"):
        end = src.find("\n---\n", 3) + 5
        front, body = src[:end], src[end:]
    else:
        front, body = "", src

    lines = body.split("\n")
    spans = list(blocks(body))
    saved = 0
    for start, stop in reversed(spans):
        block = lines[start:stop]
        if len(block) == 1 and len(block[0]) <= WIDTH:
            continue
        new = reflow(block)
        b, a = "\n".join(block), "\n".join(new)
        if b == a:
            continue
        if not safe(b, a):
            raise SystemExit(
                f"{path}:{start + 1}: refusing to reflow, the block would change "
                f"meaning\n--- before\n{b}\n--- after\n{a}")
        saved += len(block) - len(new)
        lines[start:stop] = new

    out = front + "\n".join(lines)
    # Whole-file backstop. A per-block check cannot see a fence the block
    # scanner failed to recognise, and that is exactly the bug that shipped.
    if not code_intact(src, out):
        raise SystemExit(f"{path}: refusing to write, a code block or span changed")
    if inline(src[len(front):]) != inline(out[len(front):]):
        raise SystemExit(f"{path}: refusing to write, the text changed")
    return out, saved


def main() -> int:
    check = "--check" in sys.argv
    changed, lines_saved = [], 0
    for path in sorted(glob.glob("**/*.md", recursive=True)):
        if path.startswith(("node_modules", ".git")) or path == "MANIFEST.md":
            continue
        out, saved = process(path)
        if out != open(path, encoding="utf-8").read():
            changed.append(path)
            lines_saved += saved
            if not check:
                open(path, "w", encoding="utf-8").write(out)

    if check and changed:
        print(f"prose is not reflowed ({len(changed)} file(s)); "
              f"run: python3 scripts/fmt_prose.py")
        for c in changed[:10]:
            print(f"  - {c}")
        return 1
    verb = "would reflow" if check else "reflowed"
    print(f"prose check passed" if check and not changed
          else f"{verb} {len(changed)} file(s), {lines_saved} line break(s) removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
