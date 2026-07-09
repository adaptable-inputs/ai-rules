#!/usr/bin/env python3
"""Verify fenced code examples in ai-rules markdown.

Scope is deliberately parse-level, not type-level. Paired Do/Don't snippets
intentionally contain wrong code and reference types they never declare, so
type-checking them would be meaningless. What is checkable:

  * the fence tag is one we recognise (catches typos that disable highlighting)
  * python / yaml / json / jsonc blocks parse
  * ts / tsx / js / jsx blocks parse (delegated to scripts/check_js.mjs)
  * paired Do/Don't snippets declare unique names, per
    AI-RULES/LESSONS_LEARNED/2026-02-08-react-example-robustness.md

Opt a block out with an HTML comment on the line before its opening fence:

    <!-- no-verify: reason -->

Exit 0 on success, 1 on any violation.
"""
from __future__ import annotations
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# text/md/bash/html/css/sql are prose or not worth a parser here.
KNOWN_TAGS = {
    "text", "md", "bash", "html", "css", "sql",
    "java", "ts", "tsx", "js", "jsx", "python", "yaml", "json", "jsonc",
}
PARSE_JS = {"ts", "tsx", "js", "jsx"}
NO_VERIFY = re.compile(r"<!--\s*no-verify")
# top-level `function name(` / `const name = (` / `class Name`
DECL = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:function|class)\s+([A-Za-z_$][\w$]*)", re.M)

errors: list[str] = []


def fail(f: str, line: int, msg: str) -> None:
    errors.append(f"{f}:{line}: {msg}")


def _parse_json_seq(rel: str, line: int, tag: str, body: str) -> None:
    """Parse one or more concatenated JSON values (a Do/Don't pair is two)."""
    dec = json.JSONDecoder()
    text, idx, n = body.strip(), 0, 0
    while idx < len(text):
        try:
            _, end = dec.raw_decode(text, idx)
        except json.JSONDecodeError as e:
            fail(rel, line, f"{tag} block does not parse: {e.msg} (value {n + 1}, line {e.lineno})")
            return
        n += 1
        idx = end
        while idx < len(text) and text[idx] in " \t\r\n,":
            idx += 1
    if n == 0:
        fail(rel, line, f"{tag} block contains no JSON value")


def blocks(path: Path):
    """Yield (tag, body, start_line, skip) for each fenced block."""
    lines = path.read_text(encoding="utf-8").split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^```([A-Za-z0-9+-]*)\s*$", lines[i])
        if not m:
            i += 1
            continue
        tag = m.group(1)
        skip = i > 0 and bool(NO_VERIFY.search(lines[i - 1]))
        j = i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            j += 1
        yield tag, "\n".join(lines[i + 1:j]), i + 1, skip
        i = j + 1


def check_js(jobs: list[tuple[str, int, str, str]]) -> None:
    """Batch ts/tsx/js/jsx blocks through the node parser."""
    if not jobs:
        return
    script = ROOT / "scripts" / "check_js.mjs"
    payload = json.dumps([{"file": f, "line": ln, "tag": t, "code": c} for f, ln, t, c in jobs])
    try:
        r = subprocess.run(["node", str(script)], input=payload, text=True,
                           capture_output=True, timeout=180, cwd=ROOT)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        fail("scripts/check_js.mjs", 0, f"could not run node parser: {e}")
        return
    # The parser prints "OK <n>" on its last stdout line when it ran to completion.
    # Anything else - a crash, a missing typescript, a bad import - must not be
    # mistaken for "no findings". Exit 1 is a legitimate "found errors" signal
    # only when that sentinel is present.
    out = r.stdout.splitlines()
    if not out or not out[-1].startswith("OK "):
        fail("scripts/check_js.mjs", 0,
             f"parser did not complete (exit {r.returncode}): "
             f"{(r.stderr.strip() or 'no stderr')[:300]}")
        return
    for line in out[:-1]:
        if line.strip():
            errors.append(line.strip())


def main() -> int:
    js_jobs: list[tuple[str, int, str, str]] = []
    total = skipped = 0

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        for tag, body, line, skip in blocks(path):
            total += 1
            if skip:
                skipped += 1
                continue
            if not tag:
                continue  # untagged fence: MD040 is disabled, so allowed
            if tag not in KNOWN_TAGS:
                fail(rel, line, f"unknown fence tag ```{tag}")
                continue
            if tag == "python":
                try:
                    ast.parse(body)
                except SyntaxError as e:
                    fail(rel, line, f"python block does not parse: {e.msg} (line {e.lineno})")
            elif tag == "yaml":
                # A block may show frontmatter, which is a multi-document stream.
                try:
                    list(yaml.safe_load_all(body))
                except yaml.YAMLError as e:
                    fail(rel, line, f"yaml block does not parse: {str(e)[:120]}")
            elif tag == "json":
                if re.search(r"^\s*//", body, re.M):
                    fail(rel, line, "json block contains // comments; tag it ```jsonc")
                    continue
                _parse_json_seq(rel, line, "json", body)
            elif tag == "jsonc":
                stripped = re.sub(r"//.*$", "", body, flags=re.M)
                _parse_json_seq(rel, line, "jsonc", stripped)
            elif tag in PARSE_JS:
                js_jobs.append((rel, line, tag, body))
                names = DECL.findall(body)
                dupes = {n for n in names if names.count(n) > 1}
                if dupes and ("Don't" in body or "Do:" in body):
                    fail(rel, line,
                         f"paired snippet redeclares {sorted(dupes)}; use *Bad/*Good names so "
                         f"each snippet is independently compilable "
                         f"(LESSONS_LEARNED/2026-02-08-react-example-robustness.md)")

    check_js(js_jobs)

    if errors:
        print(f"example check FAILED with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"example check passed: {total} blocks ({skipped} opted out, {len(js_jobs)} parsed as JS/TS)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
