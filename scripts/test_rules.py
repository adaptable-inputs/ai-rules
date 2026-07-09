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
# `entry` and `index` are read during ordinary work, so they may be ratchet-locked.
# `annex` is task-gated and holds no obligation; `never`/`setup` are not project rules.
NON_LOADABLE = {"never", "setup", "annex"}


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

    def test_inherits_targets_exist(self):
        for p, meta, _ in loadable_docs():
            for t in meta.get("inherits", []) or []:
                target = ROOT / t[:-3] if t.endswith("/**") else ROOT / t
                self.assertTrue(target.exists(), f"{rel(p)}: inherits missing {t}")

    def test_scope_and_semdeps_sections_are_gone(self):
        # They live in frontmatter now; a prose copy would be a second source
        # of truth and pure context cost.
        for p, _, body in loadable_docs():
            for n, ln in prose_lines(body):
                m = re.match(r"^## (Scope|Semantic Dependencies)\b", ln)
                if m and m.group(1) == "Scope" and ln.startswith("## Scope Boundary"):
                    continue
                self.assertIsNone(m, f"{rel(p)}:{n}: {ln.strip()} belongs in frontmatter")

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
        """Covers check_keyword_ratchet()."""
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
        """Covers check_preflight_readable()."""
        self._expect_fail(
            lambda r: self._sub(r, "CHANGELOG.md",
                                '  load: "setup"', '  load: "never"\n  reason: "x"'),
            "marked load: never")

    def test_broken_inherits_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "LIBRARY/JPA.md",
                                '"LANGUAGE/JAVA/JAVA.md"', '"LANGUAGE/JAVA/NOPE.md"'),
            "which does not exist")

    def test_unquoted_glob_is_caught(self):
        self._expect_fail(
            lambda r: self._sub(r, "LANGUAGE/GO/GO.md",
                                'globs: ["**/*.go"]', "globs: [**/*.go]"),
            "invalid YAML frontmatter")

    def test_orphan_file_is_caught(self):
        """Covers check_no_orphans()."""
        def edit(repo):
            (repo / "CORE" / "ORPHAN.md").write_text(
                '---\napplies_to:\n  load: "always"\n---\n# ORPHAN\n', encoding="utf-8")
        self._expect_fail(edit, "orphaned file")

    def test_category_missing_from_ai_md_is_caught(self):
        """Covers check_ai_md_lists_dirs()."""
        def edit(repo):
            d = repo / "WIDGETS"
            d.mkdir()
            (d / "WIDGETS.md").write_text(
                '---\napplies_to:\n  load: "index"\n---\n# WIDGETS\n', encoding="utf-8")
        self._expect_fail(edit, "not listed in AI.md")

    def test_bad_load_value_is_caught(self):
        """Covers check_frontmatter()."""
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
# Generated artifacts: MANIFEST.md and the category indexes
# --------------------------------------------------------------------------
def run_script(root: Path, name: str, *args):
    r = subprocess.run([sys.executable, str(root / "scripts" / name), *args],
                       capture_output=True, text=True, cwd=root)
    return r.returncode, r.stdout + r.stderr


class TestProseFormatter(unittest.TestCase):
    """fmt_prose.py rewrites files in a pre-commit hook. It must be incapable of
    changing what a rule obliges, and it must prove that per block, not per run."""

    @staticmethod
    def _mod():
        spec = importlib.util.spec_from_file_location(
            "fmt_prose", ROOT / "scripts" / "fmt_prose.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def test_corpus_is_reflowed(self):
        rc, out = run_script(ROOT, "fmt_prose.py", "--check")
        self.assertEqual(rc, 0, out)

    def test_reflow_preserves_normalized_text(self):
        f = self._mod()
        block = ["- MUST NOT swallow exceptions silently; log with `logger.error`",
                 "  and rethrow a specific type."]
        new = f.reflow(block)
        self.assertEqual(" ".join("\n".join(block).split()),
                         " ".join("\n".join(new).split()))

    def test_guard_rejects_meaning_changes(self):
        f = self._mod()
        cases = [
            ("- MUST NOT swallow exceptions.", "- Swallow exceptions."),       # keyword
            ("- MUST not retry.", "- MUST retry."),                            # negation
            ("- MUST use `Duration`.", "- MUST use Duration."),                # identifier
            ("- SHOULD retry 3 times.", "- SHOULD retry 4 times."),            # number
            ("- MUST a; SHOULD b.", "- SHOULD b; MUST a."),                    # order
            ("- If x, MUST y.", "- MUST y."),                                  # condition
            ("- See [a](b).", "- See [a](c)."),                                # link target
        ]
        for before, after in cases:
            with self.subTest(before=before):
                self.assertFalse(f.safe(before, after),
                                 f"guard accepted a meaning change: {before!r} -> {after!r}")

    def test_guard_accepts_a_pure_reflow(self):
        f = self._mod()
        self.assertTrue(f.safe("- MUST use `Duration`\n  for timeouts.",
                               "- MUST use `Duration` for timeouts."))

    def test_code_span_is_never_split(self):
        f = self._mod()
        atoms = f.atoms("Run `git subtree add --prefix x` now and see [a b](c).")
        self.assertIn("`git subtree add --prefix x`", atoms)
        self.assertIn("[a b](c).", " ".join(atoms))

    def test_snippets_survive_byte_for_byte(self):
        """Both of these shipped as real corruption before the guard existed."""
        f = self._mod()
        # A fenced block reflowed into one line (four shell commands merged).
        self.assertFalse(f.code_intact("```\ngit add .\ngit status\n```",
                                       "``` git add . git status ```"))
        # Two significant spaces squeezed inside a code span (markdownlint MD038).
        self.assertFalse(f.code_intact("a `x  y` b", "a `x y` b"))
        # A space inserted between a code span and its punctuation.
        self.assertFalse(f.safe("use `bun.lockb`).", "use `bun.lockb` )."))
        # A space inserted inside link text (markdownlint MD039).
        self.assertFalse(f.safe("see [`X`](y.md)", "see [ `X` ](y.md)"))

    def test_a_span_wrapped_across_lines_may_rejoin(self):
        # A newline inside a code span renders as one space, so rejoining is faithful.
        f = self._mod()
        self.assertTrue(f.code_intact("`plan -> merge (if\n  permitted)`",
                                      "`plan -> merge (if permitted)`"))

    def test_inline_never_adds_or_squeezes(self):
        f = self._mod()
        for text in ("see [`X`](y.md) now", "a `x  y` b", "ends `z`."):
            self.assertEqual(f.inline(text), text, f"inline() altered {text!r}")

    def test_corpus_code_matches_last_commit(self):
        """No committed snippet was altered by any reflow in this repo's history."""
        f = self._mod()
        r = subprocess.run(["git", "show", "HEAD:CORE/VERSION_CONTROL_SYSTEM.md"],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode:
            self.skipTest("not a git checkout")
        cur = (ROOT / "CORE" / "VERSION_CONTROL_SYSTEM.md").read_text(encoding="utf-8")
        self.assertTrue(f.code_intact(r.stdout, cur))

    def test_fenced_code_is_untouched(self):
        f = self._mod()
        with Sandbox() as repo:
            p = repo / "DESIGN" / "ZZ.md"
            p.write_text('---\napplies_to:\n  load: "never"\n  reason: "t"\n---\n'
                         "# Z\n\n```bash\ngit status\ngit log\n```\n", encoding="utf-8")
            import os
            cwd = os.getcwd()
            os.chdir(repo)
            try:
                out, _ = f.process("DESIGN/ZZ.md")
            finally:
                os.chdir(cwd)
            self.assertIn("git status\ngit log", out)


class TestGeneratedArtifacts(unittest.TestCase):
    """A stale manifest is worse than no manifest: an agent trusts it and stops
    looking, so a rule doc disappears without any gate noticing."""

    def test_manifest_is_current(self):
        rc, out = run_script(ROOT, "gen_manifest.py", "--check")
        self.assertEqual(rc, 0, out)

    def test_indexes_are_accurate(self):
        rc, out = run_script(ROOT, "check_indexes_accurate.py")
        self.assertEqual(rc, 0, out)

    def test_new_doc_makes_the_manifest_stale(self):
        with Sandbox() as repo:
            (repo / "LIBRARY" / "ZZZ.md").write_text(
                '---\napplies_to:\n  load: "conditional"\n'
                '  when: "zzz is present"\n  purpose: "z"\n---\n# ZZZ\n',
                encoding="utf-8")
            rc, out = run_script(repo, "gen_manifest.py", "--check")
            self.assertEqual(rc, 1, f"manifest check missed a new doc\n{out}")
            self.assertIn("stale", out)

    def test_changed_condition_makes_the_manifest_stale(self):
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "JPA.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace('libraries: ["jpa"]',
                                   'libraries: ["jpa", "hibernate"]', 1),
                         encoding="utf-8")
            rc, out = run_script(repo, "gen_manifest.py", "--check")
            self.assertEqual(rc, 1, f"manifest check missed a changed condition\n{out}")

    def test_unlisted_doc_is_caught_by_the_index_check(self):
        with Sandbox() as repo:
            (repo / "DESIGN" / "ZZZ.md").write_text(
                '---\napplies_to:\n  load: "never"\n  reason: "t"\n---\n# Z\n',
                encoding="utf-8")
            rc, out = run_script(repo, "check_indexes_accurate.py")
            self.assertEqual(rc, 1, out)
            self.assertIn("does not list ZZZ.md", out)

    def test_dangling_index_link_is_caught(self):
        with Sandbox() as repo:
            p = repo / "DESIGN" / "DESIGN.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace("- [AOP.md](AOP.md)", "- [AOP.md](GONE.md)", 1),
                         encoding="utf-8")
            rc, out = run_script(repo, "check_indexes_accurate.py")
            self.assertEqual(rc, 1, out)
            self.assertIn("links to missing GONE.md", out)

    def test_manifest_never_lists_an_annex_as_a_row(self):
        # The header prose names `*.ANNEX.md` to explain the convention; what
        # must not appear is an annex as a selectable row.
        rows = [l for l in (ROOT / "MANIFEST.md").read_text(encoding="utf-8").splitlines()
                if l.startswith("- `")]
        self.assertTrue(rows)
        for r in rows:
            self.assertNotIn(".ANNEX.md`", r,
                             "an annex is task-gated; listing it invites a stray load")

    def test_every_selectable_row_states_a_condition(self):
        for line in (ROOT / "MANIFEST.md").read_text(encoding="utf-8").splitlines():
            if line.startswith("- `") and " - " in line:
                self.assertNotIn("Load when -.", line,
                                 f"row has no usable condition: {line}")


# --------------------------------------------------------------------------
# Corpus + checker: gating a regulation must fail safe
# --------------------------------------------------------------------------
class TestComplianceFailsafe(unittest.TestCase):
    """Gating the five jurisdiction-specific regimes saves 2,167 tokens per task.
    Gating them on a positive declaration would mean an agent that misjudges the
    jurisdiction silently skips GDPR. Silence must load, not skip."""

    REGIMES = ["GDPR_BDSG.md", "EPRIVACY_TTDSG.md", "EU_AI_ACT.md",
               "DORA.md", "NIS2_KRITIS.md"]

    def test_corpus_passes(self):
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_each_regime_loads_when_nothing_is_declared(self):
        for name in self.REGIMES:
            with self.subTest(doc=name):
                meta = yaml.safe_load(
                    (ROOT / "COMPLIANCE" / name).read_text(encoding="utf-8")
                    .split("---")[1])["applies_to"]
                self.assertEqual(meta["load"], "conditional")
                self.assertIn("or no compliance scope is declared", meta["when"])

    def test_licenses_stays_always(self):
        meta = yaml.safe_load(
            (ROOT / "COMPLIANCE" / "LICENSES.md").read_text(encoding="utf-8")
            .split("---")[1])["applies_to"]
        self.assertEqual(meta["load"], "always",
                         "license compatibility binds every project")

    def test_positive_only_gate_is_caught(self):
        """Covers check_compliance_failsafe()."""
        with Sandbox() as repo:
            p = repo / "COMPLIANCE" / "GDPR_BDSG.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace(
                "the declared compliance scope includes `gdpr`, "
                "or no compliance scope is declared",
                "the declared compliance scope includes `gdpr`"), encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, f"a positive-only gate would skip GDPR\n{out}")
            self.assertIn("silently skips this regime", out)

    def test_demoting_licenses_is_caught(self):
        with Sandbox() as repo:
            p = repo / "COMPLIANCE" / "LICENSES.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace('load: "always"',
                                   'load: "conditional"\n  when: "x"', 1),
                         encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("load: always", out)

    def test_ai_md_documents_the_declaration(self):
        text = (ROOT / "AI.md").read_text(encoding="utf-8")
        self.assertIn("compliance_scope", text)
        for regime in ("gdpr", "eprivacy", "eu-ai-act", "dora", "nis2"):
            self.assertIn(f"`{regime}`", text, f"AI.md does not name {regime}")


# --------------------------------------------------------------------------
# The guards obey the rules they impose
# --------------------------------------------------------------------------
class TestGuardsConform(unittest.TestCase):
    """TEST/TEST.md: "A guard MUST be covered by a test that fails when the guard
    is removed or weakened." Guards are trusted more than the code they inspect
    and reviewed less, so nothing may ship uncovered."""

    def _checker_source(self) -> str:
        return (ROOT / "scripts" / "check_structure.py").read_text(encoding="utf-8")

    def test_every_checker_is_registered_in_main(self):
        src = self._checker_source()
        defined = set(re.findall(r"^def (check_\w+)\(", src, re.M))
        main = src[src.index("def main()"):]
        for fn in sorted(defined):
            self.assertIn(f"{fn}()", main,
                          f"{fn} is defined but never runs: a guard that is not "
                          f"called cannot fail")

    def test_every_checker_has_a_test_that_names_it(self):
        defined = set(re.findall(r"^def (check_\w+)\(", self._checker_source(), re.M))
        tests = (ROOT / "scripts" / "test_rules.py").read_text(encoding="utf-8")
        missing = [fn for fn in sorted(defined) if fn not in tests]
        self.assertEqual(missing, [],
                         "these guards have no test naming them; an uncovered "
                         "guard is an assertion that it works")

    def test_every_script_is_exercised(self):
        scripts = {p.stem for p in (ROOT / "scripts").glob("*.py")
                   if p.stem not in {"test_rules"}}
        tests = (ROOT / "scripts" / "test_rules.py").read_text(encoding="utf-8")
        missing = [s for s in sorted(scripts) if f"{s}.py" not in tests]
        self.assertEqual(missing, [],
                         "these scripts run in CI or a hook but no test proves "
                         "they can fail")


# --------------------------------------------------------------------------
# Corpus + checker: no doc orders an exhaustive read
# --------------------------------------------------------------------------
class TestNoExhaustiveRead(unittest.TestCase):
    """PROGRAMMING, PLAN and CODE_REVIEW each shipped a `Ruleset Read Gate
    (Mandatory)` ordering the agent to read every file reachable from AI.md.
    AI.md forbids exactly that. Every task loads one of those three docs."""

    def test_corpus_has_no_read_gate(self):
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_ai_md_prohibition_is_not_flagged(self):
        # AI.md is the one doc allowed to say the words, as a prohibition.
        text = (ROOT / "AI.md").read_text(encoding="utf-8")
        self.assertIn("MUST NOT read this ruleset exhaustively", text)
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_reintroduced_read_gate_is_caught(self):
        """Covers check_no_exhaustive_read()."""
        with Sandbox() as repo:
            p = repo / "PROGRAMMING" / "PROGRAMMING.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## Ruleset Read Gate (Mandatory)\n"
                         "- SHOULD start every programming task by reading the "
                         "complete ai-rules ruleset.\n", encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("exhaustive ruleset read", out)

    def test_transitive_read_mandate_in_a_leaf_doc_is_caught(self):
        with Sandbox() as repo:
            p = repo / "TEST" / "TEST.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n- MUST NOT skip reachable Markdown files.\n",
                         encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("exhaustive ruleset read", out)


# --------------------------------------------------------------------------
# Corpus + checker: Override Notes hold overrides, not restatements
# --------------------------------------------------------------------------
class TestOverrideNotes(unittest.TestCase):
    """89 docs once carried "X MAY be stricter, but these constraints remain
    mandatory". The second clause asserts a force the named rules' own keywords
    withhold: 42 of them named `SHOULD` rules. The keyword is authoritative."""

    HOST = "LIBRARY/JPA.md"

    def _inject(self, repo, bullet):
        p = repo / self.HOST
        s = p.read_text(encoding="utf-8")
        self.assertIn("## Override Notes\n", s)
        p.write_text(s.replace("## Override Notes\n",
                               f"## Override Notes\n{bullet}\n", 1), encoding="utf-8")

    def _expect_fail(self, bullet, needle):
        with Sandbox() as repo:
            self._inject(repo, bullet)
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, f"checker passed but should have failed\n{out}")
            self.assertIn(needle, out, out)

    def _expect_pass(self, bullet):
        with Sandbox() as repo:
            self._inject(repo, bullet)
            rc, out = run_structure(repo)
            self.assertEqual(rc, 0, f"false positive on a real override\n{out}")

    def test_corpus_is_clean(self):
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_permission_restatement_is_caught(self):
        """Covers check_override_notes()."""
        self._expect_fail("- Framework docs MAY narrow these rules for specific stacks.",
                          "restates the global permission rule")

    def test_concession_is_caught(self):
        # The exact shape that shipped in 89 docs.
        self._expect_fail("- Project policy MAY be stricter, but the transaction "
                          "constraints here remain mandatory.",
                          "restates the global permission rule")

    def test_bare_concession_without_a_permission_clause_is_caught(self):
        self._expect_fail("- The boundary constraints in this file remain mandatory.",
                          "restates the global concession rule")

    def test_purpose_restatement_is_caught(self):
        self._expect_fail("- This file is the JPA baseline.",
                          "restates the global purpose rule")

    def test_no_index_doc_carries_an_obligation(self):
        # Introduced by the manifest change: MANIFEST.md lists only always/
        # conditional/task, so 18 obligations in indexes became unreachable,
        # including `MUST ensure licenses are compatible`.
        rc, out = run_structure(ROOT)
        self.assertEqual(rc, 0, out)

    def test_obligation_added_to_an_index_is_caught(self):
        """Covers check_no_rules_in_indexes()."""
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "LIBRARY.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## Selection\n- MUST prefer maintained libraries.\n",
                         encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, f"an unreachable rule slipped into an index\n{out}")
            self.assertIn("index doc carries an obligation", out)

    def test_link_lines_in_an_index_are_not_flagged(self):
        # "- [X.md](X.md) - rules an agent MAY apply" is prose about a doc.
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "LIBRARY.md"
            s = p.read_text(encoding="utf-8")
            p.write_text(s.replace(
                "- [JPA.md](JPA.md)",
                "- [JPA.md](JPA.md) - rules a project MAY apply;", 1),
                encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 0, f"false positive on an index link line\n{out}")

    def test_index_restatement_sections_are_caught(self):
        # 11 indexes carried these; every task that opened one paid for them.
        for heading in ("Role in the Ruleset", "Scope Boundary", "Authoring Notes"):
            with self.subTest(heading=heading), Sandbox() as repo:
                p = repo / "DESIGN" / "DESIGN.md"
                p.write_text(p.read_text(encoding="utf-8") +
                             f"\n## {heading}\n- Something.\n", encoding="utf-8")
                rc, out = run_structure(repo)
                self.assertEqual(rc, 1, out)
                self.assertIn(heading, out)

    def test_indexes_are_under_the_keyword_ratchet(self):
        import importlib.util as _il
        spec = _il.spec_from_file_location("cs", ROOT / "scripts" / "check_structure.py")
        cs = _il.module_from_spec(spec)
        spec.loader.exec_module(cs)
        for idx in ("DESIGN/DESIGN.md", "FRAMEWORK/FRAMEWORK.md", "AI.md"):
            self.assertIn(idx, cs.KEYWORD_CONVERTED,
                          f"{idx} can regain a keyword-less rule unnoticed")

    def test_specialization_contract_heading_is_caught(self):
        with Sandbox() as repo:
            p = repo / "LIBRARY" / "LIBRARY.md"
            p.write_text(p.read_text(encoding="utf-8") +
                         "\n## Specialization Contract\n- Library docs may narrow parents.\n",
                         encoding="utf-8")
            rc, out = run_structure(repo)
            self.assertEqual(rc, 1, out)
            self.assertIn("Specialization Contract", out)

    def test_a_declared_override_is_not_flagged(self):
        self._expect_pass("- The baseline mandates remain in force except for the "
                          "flush-mode override declared above.")

    def test_a_conditional_fallback_is_not_flagged(self):
        self._expect_pass("- If a query cannot use the criteria API, MAY drop to "
                          "native SQL and keep it behind the repository boundary.")

    def test_a_named_specialization_is_not_flagged(self):
        self._expect_pass("- Explicit specialization in this doc: MAY prescribe "
                          "fetch joins where the parent doc only requires no N+1.")


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
