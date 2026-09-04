#!/usr/bin/env python3
"""Tests for the boilerplate's own scripts.

    python3 tests/test_boilerplate.py

Standard library only, no pytest required. Run from the repo root.

The rule these exist to honour: a rule nobody can re-run tomorrow isn't
enforced, it's remembered. Every convention the generator claims to apply is
checked here against generated output, not against intent.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATOR = os.path.join(ROOT, "skills", "skill-boilerplate", "scripts",
                         "generate_skill_creator.py")

MAXIMAL = {
    "naming": {"convention": "prefix_block", "prefixes": ["ops", "fin"],
               "max_segments": 4},
    "versioning": {"scheme": "4", "initial_version": "1.0.0.0"},
    "changelog": "always",
    "rigor": {"body_structure": "fixed",
              "identification_fields": ["Domain", "Version"]},
    "scope": {"evaluation": True, "packaging_gate": True,
              "folders": "custom_vocab", "vocabulary": ["phases"]},
}

MINIMAL = {
    "naming": {"convention": "flat", "prefixes": [], "max_segments": None},
    "versioning": {"scheme": "none", "initial_version": ""},
    "changelog": "never",
    "rigor": {"body_structure": "free",
              "identification_fields": []},
    "scope": {"evaluation": False, "packaging_gate": False,
              "folders": "spec_only", "vocabulary": []},
}


def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True,
                          text=True)


class GeneratorTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def generate(self, config):
        path = os.path.join(self.tmp, "config.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f)
        result = run([GENERATOR, "--config", path, "--destination", self.tmp])
        name = config.get("tool_name") or "my-skill-creator"
        return result, os.path.join(self.tmp, name)

    def read_skill(self, root):
        with open(os.path.join(root, "SKILL.md"), encoding="utf-8") as f:
            return f.read()

    def test_maximal_generates(self):
        result, root = self.generate(MAXIMAL)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.isfile(os.path.join(root, "SKILL.md")))
        self.assertTrue(os.path.isfile(os.path.join(root, "CHANGELOG.md")))
        self.assertTrue(os.path.isfile(os.path.join(root, ".skill-config.json")))

    def test_minimal_generates_without_changelog(self):
        result, root = self.generate(MINIMAL)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(os.path.exists(os.path.join(root, "CHANGELOG.md")))

    def test_no_unsubstituted_tokens(self):
        for config in (MAXIMAL, MINIMAL):
            with self.subTest(config=config["naming"]["convention"]):
                self.tearDown()
                self.tmp = tempfile.mkdtemp()
                _, root = self.generate(config)
                self.assertNotIn("{{", self.read_skill(root))

    def test_version_present_only_when_scheme_set(self):
        _, root = self.generate(MAXIMAL)
        self.assertIn("version: 1.0.0.0", self.read_skill(root))
        self.tearDown()
        self.tmp = tempfile.mkdtemp()
        _, root = self.generate(MINIMAL)
        self.assertNotIn("metadata:", self.read_skill(root))

    def test_optional_sections_absent_when_disabled(self):
        _, root = self.generate(MINIMAL)
        text = self.read_skill(root)
        self.assertNotIn("Trigger evaluation", text)
        self.assertNotIn("Packaging gate", text)
        self.assertNotIn("Identification table", text)

    def test_optional_sections_present_when_enabled(self):
        _, root = self.generate(MAXIMAL)
        text = self.read_skill(root)
        self.assertIn("Trigger evaluation", text)
        self.assertIn("Packaging gate", text)
        self.assertIn("Identification table", text)

    def test_values_live_in_config_not_in_prose(self):
        """The group list and word cap must not be copied into SKILL.md.

        The scripts read them from .skill-config.json. A second copy in prose
        would be free to drift, and the user would see the scaffolder warn
        under one rule while the skill proposed names under another.
        """
        _, root = self.generate(MAXIMAL)
        text = self.read_skill(root)
        for value in ("`ops`", "`fin`", "4 segments", "at most 4"):
            self.assertNotIn(value, text, f"{value!r} leaked into the prose")
        self.assertIn(".skill-config.json", text)
        with open(os.path.join(root, ".skill-config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        self.assertEqual(cfg["naming"]["prefixes"], ["ops", "fin"])
        self.assertEqual(cfg["naming"]["max_segments"], 4)

    def test_config_marks_editable_and_locked_keys(self):
        _, root = self.generate(MAXIMAL)
        with open(os.path.join(root, ".skill-config.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        readme = cfg["_readme"]
        self.assertIn("naming.prefixes", readme["edit_freely"])
        self.assertIn("naming.max_segments", readme["edit_freely"])
        self.assertIn("naming.convention", readme["requires_regenerating"])
        self.assertIn("versioning.scheme", readme["requires_regenerating"])

    def test_custom_convention_still_baked_in(self):
        """Free prose describing a rule is not a value -- it stays in the text."""
        cfg = json.loads(json.dumps(MAXIMAL))
        cfg["naming"]["convention"] = "custom"
        cfg["naming"]["custom_convention"] = "Verb first, then the object."
        _, root = self.generate(cfg)
        self.assertIn("Verb first, then the object.", self.read_skill(root))

    def test_default_tool_name_is_my_skill_creator(self):
        """Not `skill-creator`: Anthropic already ships one with that exact
        name, and colliding with it by default would defeat the point of
        asking at all."""
        _, root = self.generate(MAXIMAL)
        self.assertTrue(root.endswith("my-skill-creator"))
        text = self.read_skill(root)
        self.assertIn("name: my-skill-creator", text)
        self.assertNotIn("name: skill-creator\n", text)

    def test_step_zero_asks_whether_it_should_be_a_skill(self):
        """Building the wrong artefact well is still building the wrong one.
        The generated tool must push back before it starts."""
        _, root = self.generate(MAXIMAL)
        text = self.read_skill(root)
        self.assertIn("Should this be a skill at all?", text)
        self.assertIn("Is this going to repeat?", text)
        self.assertIn("two or three real requests", text)

    def test_certainty_markers_are_gone_entirely(self):
        """Certainty markers are content, not container. They were a setup
        question; now they are not offered at all, in any configuration."""
        for cfg in (MAXIMAL, MINIMAL):
            self.tearDown()
            self.tmp = tempfile.mkdtemp()
            _, root = self.generate(cfg)
            text = self.read_skill(root)
            for term in ("[Verified]", "[Unconfirmed]", "[Interpretation]",
                         "regulated"):
                self.assertNotIn(term, text, f"{term!r} survived")

    def test_description_declares_boundary_with_official(self):
        """A generated skill installed alongside Anthropic's official
        skill-creator must not compete for the same request without telling
        the model why it, and not the other one, should fire."""
        _, root = self.generate(MAXIMAL)
        text = self.read_skill(root)
        self.assertIn("Do NOT use for automated evaluation", text)
        self.assertIn("skill-creator", text.split("Do NOT use", 1)[1])

    def test_custom_tool_name_is_used_throughout(self):
        cfg = json.loads(json.dumps(MAXIMAL))
        cfg["tool_name"] = "acme-skill-maker"
        _, root = self.generate(cfg)
        self.assertTrue(root.endswith("acme-skill-maker"))
        self.assertIn("name: acme-skill-maker", self.read_skill(root))

    def test_reserved_tool_name_is_rejected(self):
        for bad in ("claude-helper", "my-anthropic-tool"):
            cfg = json.loads(json.dumps(MAXIMAL))
            cfg["tool_name"] = bad
            result, _ = self.generate(cfg)
            self.assertNotEqual(result.returncode, 0, bad)
            self.assertIn("reserves", result.stdout + result.stderr)

    def test_malformed_tool_name_is_rejected(self):
        for bad in ("Skill_Creator", "-leading-hyphen", "double--hyphen"):
            cfg = json.loads(json.dumps(MAXIMAL))
            cfg["tool_name"] = bad
            result, _ = self.generate(cfg)
            self.assertNotEqual(result.returncode, 0, bad)

    def test_refuses_to_overwrite(self):
        self.generate(MAXIMAL)
        result, _ = self.generate(MAXIMAL)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stdout + result.stderr)

    def test_rejects_incomplete_config(self):
        broken = {"naming": MAXIMAL["naming"]}
        path = os.path.join(self.tmp, "broken.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(broken, f)
        result = run([GENERATOR, "--config", path, "--destination", self.tmp])
        self.assertNotEqual(result.returncode, 0)

    def test_rejects_unknown_values(self):
        bad = json.loads(json.dumps(MAXIMAL))
        bad["changelog"] = "sometimes-maybe"
        path = os.path.join(self.tmp, "bad.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bad, f)
        result = run([GENERATOR, "--config", path, "--destination", self.tmp])
        self.assertNotEqual(result.returncode, 0)


class GeneratedScriptTests(unittest.TestCase):
    """The generated scripts must work in the collection they land in."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        path = os.path.join(self.tmp, "config.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(MAXIMAL, f)
        run([GENERATOR, "--config", path, "--destination", self.tmp])
        self.root = os.path.join(self.tmp, "my-skill-creator")
        self.scaffold = os.path.join(self.root, "scripts", "scaffold_skill.py")
        self.validate = os.path.join(self.root, "scripts", "validate_skill.py")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_skill_creator_validates_itself_clean(self):
        result = run([self.validate, self.root])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("0 errors", result.stdout)

    def test_scaffold_creates_only_requested_folders(self):
        run([self.scaffold, "ops-eu-report", "--destination", self.tmp,
             "--references"])
        skill = os.path.join(self.tmp, "ops-eu-report")
        self.assertTrue(os.path.isdir(os.path.join(skill, "references")))
        self.assertFalse(os.path.exists(os.path.join(skill, "scripts")))

    def test_scaffold_covers_every_folder_combination(self):
        """Each flag combination must produce exactly those folders.

        The template ships with no folders at all, so this is the guarantee
        that the ones you need actually appear when you ask for them -- and
        that the ones you didn't ask for stay absent.
        """
        import itertools
        flags = {"references": "--references",
                 "scripts": "--scripts",
                 "assets": "--assets"}
        for size in range(len(flags) + 1):
            for combo in itertools.combinations(sorted(flags), size):
                name = "combo-" + ("none" if not combo else "-".join(combo))
                args = [self.scaffold, name, "--destination", self.tmp]
                args += [flags[c] for c in combo]
                result = run(args)
                self.assertEqual(result.returncode, 0, result.stderr)
                skill = os.path.join(self.tmp, name)
                for folder in flags:
                    exists = os.path.isdir(os.path.join(skill, folder))
                    self.assertEqual(exists, folder in combo,
                                     f"{name}: {folder} present={exists}")

    def test_scaffolded_skill_with_folders_validates_once_filled(self):
        """A skill scaffolded with folders passes validation once the folders
        have real content and the description is written."""
        run([self.scaffold, "ops-eu-full", "--destination", self.tmp,
             "--references", "--scripts"])
        skill = os.path.join(self.tmp, "ops-eu-full")
        path = os.path.join(skill, "SKILL.md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        text = text.replace(
            '"[FILL IN: what this skill does and exactly when to use it -- '
            'the phrases a user would actually type, not just the topic]"',
            '"Builds the monthly EU operations report. Use when someone asks '
            'for the EU ops report or says the monthly numbers are due."')
        text = text.replace("[FILL IN: what this skill does, in a sentence or "
                            "two.]", "Builds the monthly EU ops report.")
        text = text.replace("[FILL IN: the steps, rules or knowledge to "
                            "follow.]",
                            "See references/method.md for the procedure.")
        text = text.replace("- [A situation this should not fire for -- "
                            "especially if a neighbouring skill\n  covers it]",
                            "- Ad-hoc queries that are not the monthly report.")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        with open(os.path.join(skill, "references", "method.md"), "w",
                  encoding="utf-8") as f:
            f.write("# Method\n\nPull figures, compare to target, write up.\n")
        with open(os.path.join(skill, "scripts", "pull.py"), "w",
                  encoding="utf-8") as f:
            f.write("print('figures')\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("0 errors", result.stdout)

    def test_validator_sees_through_gitkeep(self):
        """A folder holding only .gitkeep is empty in every sense that matters."""
        run([self.scaffold, "ops-eu-hollow", "--destination", self.tmp,
             "--references"])
        skill = os.path.join(self.tmp, "ops-eu-hollow")
        with open(os.path.join(skill, "references", ".gitkeep"), "w",
                  encoding="utf-8") as f:
            f.write("placeholder\n")
        result = run([self.validate, skill])
        self.assertIn("git placeholder", result.stdout)

    def test_scaffold_rejects_invalid_format(self):
        result = run([self.scaffold, "Bad_Name", "--destination", self.tmp])
        self.assertNotEqual(result.returncode, 0)

    def test_scaffold_warns_but_allows_convention_mismatch(self):
        result = run([self.scaffold, "nope", "--destination", self.tmp])
        self.assertEqual(result.returncode, 0)
        self.assertIn("warning", result.stdout)

    def test_validator_flags_placeholder_description(self):
        run([self.scaffold, "ops-eu-report", "--destination", self.tmp])
        result = run([self.validate, os.path.join(self.tmp, "ops-eu-report")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder", result.stdout)

    def test_validator_flags_top_level_version(self):
        skill = os.path.join(self.tmp, "manual")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write('---\nname: manual\nversion: 1.0\n'
                    'description: "A real description that says when to use it."\n'
                    '---\n\n# Manual\n\nBody.\n')
        result = run([self.validate, skill])
        self.assertIn("not valid at the top level", result.stdout)

    def test_validator_flags_broken_link(self):
        skill = os.path.join(self.tmp, "linky")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write('---\nname: linky\nmetadata:\n  version: 1.0.0.0\n'
                    'description: "A real description that says when to use it."\n'
                    '---\n\n# Linky\n\nSee references/gone.md for more.\n')
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist", result.stdout)

    def test_validator_honours_ignore_file(self):
        skill = os.path.join(self.tmp, "linky2")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write('---\nname: linky2\nmetadata:\n  version: 1.0.0.0\n'
                    'description: "A real description that says when to use it."\n'
                    '---\n\n# Linky2\n\nSee references/gone.md for more.\n')
        with open(os.path.join(skill, ".skillcheck-ignore"), "w",
                  encoding="utf-8") as f:
            f.write("references/gone.md  # written next week\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_ignore_file_matches_directory_prefix(self):
        skill = os.path.join(self.tmp, "prefixy")
        os.makedirs(os.path.join(skill, "references", "templates"))
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write('---\nname: prefixy\nmetadata:\n  version: 1.0.0.0\n'
                    'description: "A real description that says when to use it."\n'
                    '---\n\n# Prefixy\n\nBody.\n')
        stub = os.path.join(skill, "references", "templates", "frag.md")
        with open(stub, "w", encoding="utf-8") as f:
            f.write("Holds a {{TOKEN}} and points at references/nowhere.md\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 1, "expected findings without ignore")
        with open(os.path.join(skill, ".skillcheck-ignore"), "w",
                  encoding="utf-8") as f:
            f.write("references/templates/  # fragments, irregular by design\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_ignore_file_can_disable_a_whole_check(self):
        skill = os.path.join(self.tmp, "outsider")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write('---\nname: outsider\n'
                    'description: "A real description that says when to use it."\n'
                    '---\n\n# Outsider\n\nBody.\n')
        result = run([self.validate, skill])
        self.assertIn("this collection uses versioning", result.stdout)
        with open(os.path.join(skill, ".skillcheck-ignore"), "w",
                  encoding="utf-8") as f:
            f.write("!version  # tooling, not part of the collection\n")
        result = run([self.validate, skill])
        self.assertNotIn("this collection uses versioning", result.stdout)
        self.assertIn("disabled", result.stdout)

    def test_editing_config_changes_behaviour_without_regenerating(self):
        """The whole point of referencing instead of copying: add a group to
        the JSON and the scaffolder accepts it immediately."""
        config_path = os.path.join(self.root, ".skill-config.json")
        with open(config_path, encoding="utf-8") as f:
            cfg = json.load(f)
        result = run([self.scaffold, "legal-eu-review",
                      "--destination", self.tmp])
        self.assertIn("warning", result.stdout)
        self.assertIn("not one of", result.stdout)

        cfg["naming"]["prefixes"].append("legal")
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        result = run([self.scaffold, "legal-eu-audit",
                      "--destination", self.tmp])
        self.assertNotIn("not one of", result.stdout)

    def _write_skill(self, name, extra_frontmatter="", body="Body.\n"):
        skill = os.path.join(self.tmp, name)
        os.makedirs(skill, exist_ok=True)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(f"---\nname: {name}\nmetadata:\n  version: 1.0.0.0\n"
                    f"{extra_frontmatter}"
                    f'description: "A real description saying when to use it."\n'
                    f"---\n\n# {name}\n\n{body}")
        return skill

    def test_rejects_reserved_names(self):
        for name in ("claude-helper", "my-anthropic-tool"):
            skill = self._write_skill(name)
            result = run([self.validate, skill])
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("reserved", result.stdout)

    def test_rejects_angle_brackets_in_frontmatter(self):
        skill = self._write_skill("bracketed",
                                  extra_frontmatter="compatibility: needs <python>\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("angle brackets", result.stdout)

    def test_yaml_folded_scalar_is_not_an_angle_bracket(self):
        """`description: >` is YAML, not markup. A lone `>` cannot open a tag,
        and flagging it would fail every skill that wraps a long description."""
        skill = os.path.join(self.tmp, "folded")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("---\nname: folded\nmetadata:\n  version: 1.0.0.0\n"
                    "description: >\n  A real description that says when to "
                    "use it, wrapped\n  across two lines.\n---\n\n# Folded\n\n"
                    "Body.\n")
        result = run([self.validate, skill])
        self.assertNotIn("angle brackets", result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_angle_brackets_allowed_in_body(self):
        skill = self._write_skill("bodybrackets", body="Run it on <a file>.\n")
        result = run([self.validate, skill])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_warns_about_readme_inside_skill(self):
        skill = self._write_skill("with-readme")
        with open(os.path.join(skill, "README.md"), "w", encoding="utf-8") as f:
            f.write("# Readme\n")
        result = run([self.validate, skill])
        self.assertIn("no README.md", result.stdout)

    def test_non_spec_folder_is_a_warning_not_info(self):
        skill = self._write_skill("odd-folders")
        os.makedirs(os.path.join(skill, "phases"))
        with open(os.path.join(skill, "phases", "one.md"), "w",
                  encoding="utf-8") as f:
            f.write("# One\n")
        result = run([self.validate, skill])
        self.assertIn("WARN", result.stdout)
        self.assertIn("phases/", result.stdout)

    def test_generated_templates_carry_no_angle_brackets(self):
        """A user copying a generated frontmatter example must not inherit
        brackets that are forbidden there."""
        import glob
        base = os.path.join(ROOT, "skills", "skill-boilerplate", "scripts",
                            "templates")
        for path in [os.path.join(base, "skill_creator_base.md")] + \
                glob.glob(os.path.join(base, "fragments", "*.md")):
            with open(path, encoding="utf-8") as f:
                text = f.read()
            offenders = [l for l in text.split("\n")
                         if "<" in l and not l.lstrip().startswith(">")]
            self.assertEqual(offenders, [], f"{os.path.basename(path)}: {offenders}")

    def test_validator_never_modifies(self):
        before = {}
        for base, _, files in os.walk(self.root):
            for name in files:
                path = os.path.join(base, name)
                before[path] = os.path.getmtime(path)
        run([self.validate, self.root])
        for path, mtime in before.items():
            self.assertEqual(os.path.getmtime(path), mtime, path)


class RepositoryTests(unittest.TestCase):
    """Checks on the repository itself, not on generated output.

    Every one of these exists because the thing it checks was wrong once, in a
    way nothing failed on: a misspelt directory, a placeholder left in a legal
    notice, a documented path that had never existed. A convention nobody
    re-checks is a convention that drifts.
    """

    def test_github_directory_is_spelled_correctly(self):
        # A misspelt .github is invisible to GitHub: no templates, no CI, no error.
        self.assertTrue(os.path.isdir(os.path.join(ROOT, ".github")))
        for name in os.listdir(ROOT):
            if name.startswith(".git") and name not in (".git", ".github", ".gitignore"):
                self.fail("Unexpected dot-git directory at the repository root: " + name)

    def test_community_files_are_where_github_looks(self):
        for relative in (
            ".github/CONTRIBUTING.md",
            ".github/CODE_OF_CONDUCT.md",
            ".github/PULL_REQUEST_TEMPLATE.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/feature_request.md",
        ):
            self.assertTrue(os.path.isfile(os.path.join(ROOT, relative)), relative)

        # A pull request template inside ISSUE_TEMPLATE/ is never picked up.
        issue_dir = os.path.join(ROOT, ".github", "ISSUE_TEMPLATE")
        for name in os.listdir(issue_dir):
            self.assertNotIn("PULL_REQUEST", name.upper())
            self.assertNotIn("CONTRIBUTING", name.upper())
            self.assertNotIn("CODE_OF_CONDUCT", name.upper())

    def test_license_has_a_copyright_holder(self):
        with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("[COPYRIGHT HOLDER", text)
        self.assertNotIn("FILL IN", text.upper())

    def test_manifests_are_valid_json_and_agree(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"),
                  encoding="utf-8") as f:
            plugin = json.load(f)
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"),
                  encoding="utf-8") as f:
            market = json.load(f)

        self.assertIn("name", plugin)
        self.assertIn("name", market)
        self.assertIn("owner", market)
        self.assertIn("name", market["owner"])

        entries = market["plugins"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["name"], plugin["name"])
        self.assertTrue(entry["source"] == "./" or entry["source"].startswith("./"))
        # The docs warn that a version in both places lets a stale manifest win.
        self.assertNotIn("version", entry)

    def test_documented_paths_exist(self):
        """Every repo-relative path named in the community files is real."""
        cited = {
            "tests/test_boilerplate.py",
            "skills/skill-boilerplate/scripts",
            "scripts/build_skill_zip.py",
            "template",
            "docs",
            "CHANGELOG.md",
            "README.md",
            "LICENSE",
        }
        for relative in sorted(cited):
            self.assertTrue(os.path.exists(os.path.join(ROOT, relative)), relative)

    def test_no_readme_inside_a_skill_folder(self):
        skill_dir = os.path.join(ROOT, "skills")
        for base, _, files in os.walk(skill_dir):
            for name in files:
                self.assertNotEqual(name.lower(), "readme.md",
                                    os.path.join(base, name))


class SkillZipTests(unittest.TestCase):
    """The archive shape claude.ai accepts, checked rather than assumed."""

    script = os.path.join(ROOT, "scripts", "build_skill_zip.py")
    source = os.path.join(ROOT, "skills", "skill-boilerplate")

    @classmethod
    def setUpClass(cls):
        # Import the builder rather than restating its exclusion rules here.
        # A second copy of that list would drift, and the test would then be
        # checking a rule the script no longer applies.
        spec = importlib.util.spec_from_file_location("build_skill_zip", cls.script)
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)

    def build(self):
        out = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, out, True)
        result = run([self.script, self.source, "--output-dir", out])
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = os.path.join(out, "skill-boilerplate.zip")
        self.assertTrue(os.path.isfile(archive), "no archive written")
        return archive

    def test_archive_root_is_the_skill_folder(self):
        with zipfile.ZipFile(self.build()) as zf:
            names = [n for n in zf.namelist() if not n.endswith("/")]
        self.assertTrue(names)
        for name in names:
            self.assertTrue(name.startswith("skill-boilerplate/"), name)
        self.assertIn("skill-boilerplate/SKILL.md", names)

    def test_no_file_is_silently_dropped(self):
        """A zip missing a folder installs cleanly and behaves half-written."""
        expected = len(self.builder.collect_files(self.source))
        self.assertGreater(expected, 1)
        with zipfile.ZipFile(self.build()) as zf:
            self.assertEqual(
                len([n for n in zf.namelist() if not n.endswith("/")]), expected)

    def test_paths_use_forward_slashes(self):
        # Backslashes in an archive path are not a separator to every reader,
        # so a zip built on Windows must look like one built anywhere else.
        with zipfile.ZipFile(self.build()) as zf:
            for name in zf.namelist():
                self.assertNotIn("\\", name, name)

    def test_refuses_a_folder_that_is_not_a_skill(self):
        empty = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, empty, True)
        result = run([self.script, empty])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SKILL.md", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
