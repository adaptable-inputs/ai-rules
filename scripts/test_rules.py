#!/usr/bin/env python3
"""Test suite for the ai-rules corpus and the checkers that guard it.

Two kinds of test live here.

*Corpus tests* assert properties of the Markdown: every loadable document
carries valid frontmatter, every normative statement carries an obligation
keyword, no statement contradicts itself.

*Checker tests* assert that `check_structure.py` actually fails when it should.
A guard that cannot fail is worse than no guard, because it is trusted. Every
regression found while building this ruleset has a test here, named after the
mistake, so it cannot return silently.

Run:  python3 scripts/test_rules.py
      python3 -m unittest discover -s scripts -p 'test_*.py'
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STRUCTURE = ROOT / "scripts" / "check_structure.py"
EXAMPLES = ROOT / "scripts" / "check_examples.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("cs", STRUCTURE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cs = _load_checker()

LOADABLE = {"always", "conditional", "task"}
NON_LOADABLE = {"never", "setup", "entry", "index"}


def md_files():
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def frontmatter(p: Path):
    src = p.read_text(encoding="utf-8")
    if not src.startswith("---\n"):
        return None, src
    end = src.find("\n---\n", 3)
    return yaml.safe_load(src[4:end])["applies_to"], src[end + 5:]


def loadable_docs():
    for p in md_files():
        if rel(p) in cs.FRONTMATTER_EXEMPT:
            continue
        meta, body = frontmatter(p)
        if meta and meta["load"] in LOADABLE:
            yield p, meta, body


def outside_code(line: str) -> str:
    """Blank out inline code spans so they are not searched."""
    return re.sub(r"`[^`]*`", "``", line)


def prose_lines(body: str):
    fence = False
    for i, ln in enumerate(body.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        yield i, ln


def run_structure(root: Path):
    r = subprocess.run([sys.executable, "scripts/check_structure.py"],
                       cwd=root, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


class Sandbox:
    """A throwaway copy of the repo, so a test can corrupt a file safely."""

    def __enter__(self):
        self.dir = Path(tempfile.mkdtemp(prefix="ai-rules-test-"))
        self.repo = self.dir / "repo"
        shutil.copytree(ROOT, self.repo,
                        ignore=shutil.ignore_patterns(".git", "node_modules"))
        # Symlink rather than copy: the example checker needs the TypeScript
        # parser, and copying node_modules per test is slow.
        nm = ROOT / "node_modules"
        if nm.exists():
            (self.repo / "node_modules").symlink_to(nm, target_is_directory=True)
        return self.repo

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)
        return False


# --------------------------------------------------------------------------
# Corpus: frontmatter
# --------------------------------------------------------------------------
class TestFrontmatter(unittest.TestCase):

    def test_every_doc_has_parseable_frontmatter(self):
        for p in md_files():
            if rel(p) in cs.FRONTMATTER_EXEMPT:
                continue
            meta, _ = frontmatter(p)
            self.assertIsNotNone(meta, f"{rel(p)}: missing frontmatter")
            self.assertIn("load", meta, f"{rel(p)}: applies_to has no load")

    def test_load_value_is_known(self):
        for p in md_files():
            if rel(p) in cs.FRONTMATTER_EXEMPT:
                continue
            meta, _ = frontmatter(p)
            self.assertIn(meta["load"], cs.VALID_LOAD, f"{rel(p)}")

    def test_globs_are_strings_not_yaml_aliases(self):
        # An unquoted **/*.java parses as a YAML alias, not a string. This
        # silently produced 19 unparseable blocks on the first frontmatter pass.
        for p in md_files():
            if rel(p) in cs.FRONTMATTER_EXEMPT:
                continue
            meta, _ = frontmatter(p)
            for g in meta.get("globs", []) or []:
                self.assertIsInstance(g, str, f"{rel(p)}: glob {g!r} is not a string")

    def test_conditional_docs_declare_a_selector(self):
        for p, meta, _ in loadable_docs():
            if meta["load"] != "conditional":
                continue
            self.assertTrue(cs.CONDITIONAL_KEYS & set(meta),
                            f"{rel(p)}: load: conditional with no selector or when clause")

    def test_never_has_reason_and_setup_has_when(self):
        for p in md_files():
            if rel(p) in cs.FRONTMATTER_EXEMPT:
                continue
            meta, _ = frontmatter(p)
            if meta["load"] == "never":
                self.assertTrue(meta.get("reason"), f"{rel(p)}: never without reason")
            if meta["load"] == "setup":
                self.assertTrue(meta.get("when"), f"{rel(p)}: setup without when")


# --------------------------------------------------------------------------
# Corpus: the loading contract
# --------------------------------------------------------------------------
class TestLoadingContract(unittest.TestCase):

    def test_every_loadable_doc_is_locked(self):
        unlocked = [rel(p) for p, _, _ in loadable_docs()
                    if rel(p) not in cs.KEYWORD_CONVERTED]
        self.assertEqual(unlocked, [], "loadable but not in KEYWORD_CONVERTED")

    def test_locked_list_names_only_real_files(self):
        for f in cs.KEYWORD_CONVERTED:
            self.assertTrue((ROOT / f).exists(), f"KEYWORD_CONVERTED names missing file {f}")

    def test_preflight_docs_are_not_never_load(self):
        # A file the setup preflight must read cannot be forbidden to read.
        tpl = (ROOT / "AGENTS_TEMPLATE.md").read_text(encoding="utf-8")
        m = re.search(r"Read target-version docs:\n((?:\s*-\s*`[^`]+`\n)+)", tpl)
        self.assertIsNotNone(m, "AGENTS_TEMPLATE.md preflight list not found")
        named = re.findall(r"`([^`]+)`", m.group(1))
        self.assertTrue(named)
        for f in named:
            meta, _ = frontmatter(ROOT / f)
            self.assertNotEqual(meta["load"], "never",
                                f"{f} is required by the preflight but marked never")


# --------------------------------------------------------------------------
# Corpus: obligation vocabulary
# --------------------------------------------------------------------------
class TestNormativeLanguage(unittest.TestCase):

    def test_no_bare_normative_imperative(self):
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_no_lowercase_modal_in_loadable_prose(self):
        modal = re.compile(r"\b(must not|must|should not|should|may)\b")
        offenders = []
        for p, _, body in loadable_docs():
            for n, ln in prose_lines(body):
                if modal.search(outside_code(ln)):
                    offenders.append(f"{rel(p)}:{n}: {ln.strip()[:60]}")
        self.assertEqual(offenders, [], "lowercase modals hide the obligation level")

    def test_no_self_contradicting_keyword(self):
        # "MUST prefer X" asserts an absolute requirement and a ranked choice at
        # once. R1 produced two of these mechanically from "Always prefer".
        bad = re.compile(r"\bMUST( NOT)? (prefer|avoid)\b")
        offenders = [f"{rel(p)}: {ln.strip()[:60]}"
                     for p, _, body in loadable_docs()
                     for _, ln in prose_lines(body) if bad.search(ln)]
        self.assertEqual(offenders, [])

    def test_no_doubled_keyword(self):
        dbl = re.compile(r"\b(MUST|SHOULD|MAY)( NOT)? (MUST|SHOULD|MAY)\b")
        offenders = [f"{rel(p)}: {ln.strip()[:60]}"
                     for p, _, body in loadable_docs()
                     for _, ln in prose_lines(body) if dbl.search(ln)]
        self.assertEqual(offenders, [])

    def test_banned_hedges_absent(self):
        # NORMATIVE_LANGUAGE.md forbids these as substitutes for a keyword.
        banned = re.compile(r"^\s*[-*] (Prefer|Avoid|Never|Always|Consider) ")
        offenders = [f"{rel(p)}: {ln.strip()[:60]}"
                     for p, _, body in loadable_docs()
                     for _, ln in prose_lines(body) if banned.match(ln)]
        self.assertEqual(offenders, [])

    def test_vocabulary_doc_defines_every_keyword_in_use(self):
        vocab = (ROOT / "CORE" / "NORMATIVE_LANGUAGE.md").read_text(encoding="utf-8")
        for kw in ("MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY"):
            self.assertIn(f"`{kw}`", vocab, f"{kw} used but not defined")

    def test_security_rules_are_mandatory(self):
        # A spot-check that the classifier did not weaken load-bearing controls.
        expect_must = [
            ("LANGUAGE/SQL/SQL.md", "parameterize all external values"),
            ("SECURITY/SECURITY.md", "use parameterized queries"),
            ("SECURITY/SECURITY.md", "redact secrets"),
            ("CORE/CODE_REVIEW_PLATFORM.md", "not push directly to protected branches"),
            ("CI-CD/GITHUB_ACTIONS.md", "pin third-party actions"),
            ("INFRASTRUCTURE/TERRAFORM.md", "block apply when plan includes"),
        ]
        for f, needle in expect_must:
            body = (ROOT / f).read_text(encoding="utf-8").lower()
            i = body.find(needle)
            self.assertGreater(i, -1, f"{f}: statement vanished: {needle!r}")
            head = body[max(0, i - 24):i]
            self.assertIn("must", head, f"{f}: {needle!r} is no longer a MUST")


# --------------------------------------------------------------------------
# Checker behaviour: it must actually fail
# --------------------------------------------------------------------------
class TestRatchetFails(unittest.TestCase):
    """Every one of these reproduces a bug that shipped at least once."""

    def _expect_fail(self, edit, needle):
        with Sandbox() as repo:
            edit(repo)
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, f"checker passed but should have failed\n{out}")
            self.assertIn(needle, out, out)

    def _sub(self, repo, path, old, new):
        p = repo / path
        s = p.read_text(encoding="utf-8")
        self.assertIn(old, s, f"fixture text not found in {path}: {old!r}")
        p.write_text(s.replace(old, new, 1), encoding="utf-8")

    def test_baseline_passes(self):
        with Sandbox() as repo:
            rc, out = run_structure(repo)
            self.assertEqual(rc, 0, out)

    def test_stripped_keyword_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "SECURITY/SECURITY.md",
                                "- MUST rotate secrets", "- Rotate secrets"),
            "no obligation keyword")

    def test_wrapped_bullet_with_no_keyword_anywhere_is_caught(self):
        # The checker once read only a bullet's first line. A rule whose text
        # wraps must still be inspected in full.
        def edit(repo):
            p = repo / "SECURITY" / "SECURITY.md"
            s = p.read_text(encoding="utf-8")
            s = s.replace("- MUST rotate secrets on exposure, incident, or owner change.",
                          "- Rotate secrets on exposure, on incident, or whenever the owning\n"
                          "  team changes hands for any reason at all.", 1)
            p.write_text(s, encoding="utf-8")
        self._expect_fail(edit, "no obligation keyword")

    def test_rule_with_unlisted_verb_is_caught(self):
        # "Depend on abstractions" passed for two batches because "Depend" was
        # missing from the verb allowlist.
        self._expect_fail(
            lambda r: self._sub(r, "DESIGN/SOLID.md",
                                "- SHOULD depend on abstractions", "- Depend on abstractions"),
            "no obligation keyword")

    def test_conditional_rule_is_caught(self):
        # "If X, do Y" opens with "If", so a first-word verb test never reached
        # the verb. Every conditional rule in the corpus was unguarded.
        self._expect_fail(
            lambda r: self._sub(r, "TEST/TEST.md",
                                "- If coverage targets are not met, MUST document",
                                "- If coverage targets are not met, document"),
            "no obligation keyword")

    def test_hyphenated_verb_rule_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "ARCHITECTURE/REST.md",
                                "- MUST rate-limit and monitor", "- Rate-limit and monitor"),
            "no obligation keyword")

    def test_never_load_preflight_doc_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "CHANGELOG.md",
                                '  load: "setup"', '  load: "never"\n  reason: "x"'),
            "marked load: never")

    def test_unquoted_glob_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "LANGUAGE/GO/GO.md",
                                'globs: ["**/*.go"]', "globs: [**/*.go]"),
            "invalid YAML frontmatter")

    def test_orphan_file_is_caught(self):
        def edit(repo):
            (repo / "CORE" / "ORPHAN.md").write_text(
                '---\napplies_to:\n  load: "always"\n---\n# ORPHAN\n', encoding="utf-8")
        self._expect_fail(edit, "orphaned file")

    def test_category_missing_from_ai_md_is_caught(self):
        def edit(repo):
            d = repo / "WIDGETS"
            d.mkdir()
            (d / "WIDGETS.md").write_text(
                '---\napplies_to:\n  load: "index"\n---\n# WIDGETS\n', encoding="utf-8")
        self._expect_fail(edit, "not listed in AI.md")

    def test_bad_load_value_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "CORE/LOGGING.md",
                                '  load: "always"', '  load: "sometimes"'),
            "invalid load=")


class TestRatchetDoesNotCryWolf(unittest.TestCase):
    """False positives make a checker get ignored. These must never fail."""

    def test_label_bullets_are_not_flagged(self):
        rc, out = run_structure(ROOT)
        for noise in ("Xcode:", "Example format:", "Legacy method:", "Apache-2.0"):
            self.assertNotIn(noise, out, f"{noise} flagged as an unkeyworded rule")

    def test_checklist_questions_are_not_flagged(self):
        rc, out = run_structure(ROOT)
        self.assertNotIn("Are semantic parents", out)

    def test_keyword_on_a_continuation_line_is_not_flagged(self):
        # Joining continuation lines before searching prevents a false positive
        # on a rule whose keyword lands on the second line.
        with Sandbox() as repo:
            p = repo / "SECURITY" / "SECURITY.md"
            s = p.read_text(encoding="utf-8")
            s = s.replace("- MUST redact secrets in logs, telemetry, and error messages.",
                          "- Keep logs, telemetry, and error messages free of secrets, and\n"
                          "  MUST NOT emit a credential in any of them.", 1)
            p.write_text(s, encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 0, f"false positive on a wrapped keyword\n{out}")

    def test_required_section_names_are_not_flagged(self):
        rc, out = run_structure(ROOT)
        for noise in ("Scope and applicability", "Override notes where"):
            self.assertNotIn(noise, out, f"{noise} flagged as an unkeyworded rule")


# --------------------------------------------------------------------------
# Corpus: the annex contract
# --------------------------------------------------------------------------
class TestAnnex(unittest.TestCase):

    def annexes(self):
        return [p for p in md_files() if p.name.endswith(".ANNEX.md")]

    def test_every_annex_has_a_parent_that_declares_it(self):
        for p in self.annexes():
            meta, _ = frontmatter(p)
            self.assertEqual(meta["load"], "annex", rel(p))
            parent = p.parent / meta["annex_of"]
            self.assertTrue(parent.exists(), f"{rel(p)}: parent missing")
            pmeta, _ = frontmatter(parent)
            self.assertEqual(pmeta.get("annex"), p.name,
                             f"{rel(parent)} does not declare its annex")

    def test_annex_holds_no_obligation(self):
        # The whole saving rests on this: nothing an agent must obey lives here.
        # Checklist questions may mention a keyword; a bullet that *states* a
        # rule may not.
        for p in self.annexes():
            _, body = frontmatter(p)
            for n, ln in prose_lines(body):
                m = re.match(r"^- (MUST|SHOULD|MAY)( NOT)? ", ln)
                self.assertIsNone(m, f"{rel(p)}:{n}: obligation in an annex: {ln.strip()[:50]}")

    def test_annex_sections_are_illustrative_only(self):
        for p in self.annexes():
            _, body = frontmatter(p)
            for n, ln in prose_lines(body):
                m = re.match(r"^## (.*)$", ln)
                if not m:
                    continue
                sec = re.sub(r"\s+(for|in)\s+.*$", "", m.group(1)).strip()
                self.assertTrue(sec.startswith(cs.ANNEX_SECTIONS),
                                f"{rel(p)}:{n}: {sec!r} does not belong in an annex")

    def test_parent_no_longer_carries_annex_sections(self):
        for p, _, body in loadable_docs():
            for n, ln in prose_lines(body):
                m = re.match(r"^## (.*)$", ln)
                if not m:
                    continue
                sec = re.sub(r"\s+(for|in)\s+.*$", "", m.group(1)).strip()
                self.assertFalse(sec.startswith(cs.ANNEX_SECTIONS),
                                 f"{rel(p)}:{n}: {sec!r} should have moved to the annex")


class TestAnnexChecks(unittest.TestCase):

    def test_rule_smuggled_into_an_annex_is_caught(self):
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "JPA.ANNEX.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## Defaults\n- MUST do a thing.\n", encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("does not belong in an annex", out)

    def test_parent_not_declaring_its_annex_is_caught(self):
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "JPA.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace('  annex: "JPA.ANNEX.md"\n', "", 1), encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("does not declare annex", out)

    def test_malformed_yaml_does_not_crash_the_checker(self):
        # check_annex_contract once raised a traceback instead of reporting.
        with Sandbox() as repo:
            p = repo / "LANGUAGE" / "GO" / "GO.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace('globs: ["**/*.go"]', "globs: [**/*.go]", 1), encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("invalid YAML frontmatter", out)
            self.assertNotIn("Traceback", out)


# --------------------------------------------------------------------------
# Examples checker
# --------------------------------------------------------------------------
class TestExamples(unittest.TestCase):

    def _run(self, root: Path):
        r = subprocess.run([sys.executable, "scripts/check_examples.py"],
                           cwd=root, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_baseline_passes(self):
        rc, out = self._run(ROOT)
        if "parser did not complete" in out:
            self.skipTest("typescript not installed; run: npm install typescript")
        self.assertEqual(rc, 0, out)

    def test_broken_python_block_is_caught(self):
        with Sandbox() as repo:
            p = repo / "LANGUAGE" / "PYTHON" / "PYTHON.md"
            p.write_text(p.read_text(encoding="utf-8") + "\n```python\ndef (:\n```\n",
                         encoding="utf-8")
            rc, out = self._run(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("does not parse", out)

    def test_unknown_fence_tag_is_caught(self):
        with Sandbox() as repo:
            p = repo / "TEST" / "TEST.md"
            p.write_text(p.read_text(encoding="utf-8") + "\n```pyhton\nx = 1\n```\n",
                         encoding="utf-8")
            rc, out = self._run(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("unknown fence tag", out)

    def test_json_block_with_comments_is_caught(self):
        with Sandbox() as repo:
            p = repo / "ARCHITECTURE" / "REST.md"
            p.write_text(p.read_text(encoding="utf-8") + '\n```json\n// c\n{"a":1}\n```\n',
                         encoding="utf-8")
            rc, out = self._run(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("tag it ```jsonc", out)

    def test_paired_snippet_redeclaration_is_caught(self):
        with Sandbox() as repo:
            p = repo / "FRAMEWORK" / "REACT.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n```ts\n// Don't\nfunction f() {}\n// Do:\nfunction f() {}\n```\n",
                         encoding="utf-8")
            rc, out = self._run(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("redeclares", out)

    def test_missing_parser_is_not_silent_success(self):
        # NODE_PATH does not apply to ESM imports, so the parser once crashed and
        # its exit code 1 was read as "ran fine, found no errors".
        with Sandbox() as repo:
            nm = repo / "node_modules"
            if not nm.exists():
                self.skipTest("no node_modules to hide; run: npm install typescript")
            nm.unlink()  # it is a symlink into the real repo
            rc, out = self._run(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("parser did not complete", out)


# --------------------------------------------------------------------------
# The checker and the converter must agree
# --------------------------------------------------------------------------
class TestCheckerInternals(unittest.TestCase):

    def test_verb_allowlist_has_no_section_names(self):
        # "Scope and applicability" and "Override notes ..." are section names.
        for w in ("Scope", "Override"):
            self.assertNotIn(w, cs.IMPERATIVE_VERBS,
                             f"{w!r} in the verb allowlist produces false positives")

    def test_hyphen_verbs_are_lowercase_after_the_hyphen(self):
        for v in cs.HYPHEN_VERBS:
            self.assertRegex(v, r"^[A-Z][a-z]+-[a-z]+$", f"bad hyphen verb {v!r}")

    def test_descriptive_prefixes_cover_the_standard_sections(self):
        for s in ("Scope", "Semantic Dependencies", "Code Review Checklist",
                  "Testing Guidance", "High-Risk", "Override Notes"):
            self.assertTrue(s.startswith(cs.DESCRIPTIVE_PREFIXES),
                            f"{s!r} is not registered as descriptive")

    def test_every_locked_file_is_loadable_or_index(self):
        for f in cs.KEYWORD_CONVERTED:
            meta, _ = frontmatter(ROOT / f)
            self.assertNotIn(meta["load"], NON_LOADABLE,
                             f"{f} is locked but never loaded")


if __name__ == "__main__":
    unittest.main(verbosity=2)
