#!/usr/bin/env python3
"""Assemble a personalized skill-creator from the configurator's answers.

    python3 generate_skill_creator.py --config answers.json --destination .

Reads a JSON file of answers, picks the matching template fragments, fills in
their tokens, and writes a ready-to-use `skill-creator/` folder.

Deliberate limits:

- Does not overwrite. If `skill-creator/` already exists, it aborts. The
  configurator is meant to run once; silently replacing a configured skill
  would be the worst possible failure mode.
- Does not invent answers. A missing key is an error, not a default, because a
  wrong default here gets baked into every skill the user ever makes.
- Does not write the lock file. That is the configurator's job, after it has
  confirmed the generation succeeded.

Requires Python 3.8+. Standard library only.
"""

import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "templates")
FRAGMENTS = os.path.join(TEMPLATES, "fragments")

DEFAULT_TOOL_NAME = "my-skill-creator"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_tool_name(name):
    """Same rules the generated validator will enforce on any skill: lowercase,
    hyphens, and the two words the format reserves. Checked here too so a bad
    answer fails at generation time, not at first validation."""
    if not NAME_RE.match(name):
        sys.exit(f"Invalid tool_name {name!r}: lowercase letters, digits and "
                 f"hyphens only, no leading/trailing/double hyphens")
    for reserved in ("claude", "anthropic"):
        if reserved in name.lower():
            sys.exit(f"tool_name {name!r} contains '{reserved}', which the "
                     f"format reserves -- pick another name")


DIGIT_LABELS = {
    "1": "1 digit (e.g. `3`)",
    "2": "2 digits (e.g. `1.4`)",
    "3": "3 digits, SemVer (e.g. `1.4.2`)",
    "4": "4 digits (e.g. `1.0.0.0`)",
}

REQUIRED_KEYS = ("naming", "versioning", "changelog", "rigor", "scope")


def read_fragment(name):
    path = os.path.join(FRAGMENTS, name)
    if not os.path.isfile(path):
        sys.exit(f"Missing template fragment: {name}")
    with open(path, encoding="utf-8") as f:
        return f.read().rstrip("\n")


def fill(text, tokens):
    # A token that is alone on its line and resolves to nothing takes the line
    # with it. Without this, an empty substitution leaves a stray blank line --
    # harmless in prose, but visible inside a fenced code block.
    for key, value in tokens.items():
        if value == "":
            text = re.sub(r"^[ \t]*\{\{" + key + r"\}\}[ \t]*\n", "",
                          text, flags=re.MULTILINE)
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{([A-Z_]+)\}\}", text)
    if leftover:
        sys.exit(f"Unfilled tokens remain: {sorted(set(leftover))}")
    return text


def naming_block(cfg):
    """Assemble the naming section.

    Values the scripts read at runtime -- the group list, the word cap -- are
    deliberately not substituted in here. They live in `.skill-config.json`
    only. A copy in the prose would be free to drift out of step with the file
    the scaffolder actually obeys, and the user would see a contradiction whose
    cause is invisible. The custom convention is different: it is free prose
    describing a rule, not a value any script reads, so it is baked in.
    """
    convention = cfg["naming"]["convention"]
    fragment = {
        "prefix": "naming_prefix.md",
        "prefix_block": "naming_prefix_block.md",
        "flat": "naming_flat.md",
        "custom": "naming_custom.md",
    }.get(convention)
    if not fragment:
        sys.exit(f"Unknown naming convention: {convention!r}")

    text = read_fragment(fragment)
    if convention == "custom":
        text = fill(text, {
            "CUSTOM_CONVENTION": cfg["naming"].get("custom_convention", ""),
        })
    return text


def versioning_block(cfg):
    scheme = str(cfg["versioning"]["scheme"])
    if scheme == "none":
        return read_fragment("versioning_none.md")
    if scheme not in DIGIT_LABELS:
        sys.exit(f"Unknown versioning scheme: {scheme!r}")
    return fill(read_fragment("versioning_scheme.md"), {
        "DIGITS": DIGIT_LABELS[scheme],
        "INITIAL_VERSION": cfg["versioning"]["initial_version"],
    })


def identification_block(cfg):
    fields = cfg["rigor"].get("identification_fields") or []
    if not fields:
        return read_fragment("identification_none.md")
    rows = "\n".join(f"| {f} | |" for f in fields)
    table = f"| Field | Value |\n|---|---|\n{rows}"
    return fill(read_fragment("identification_table.md"), {"FIELDS": table})


def folders_block(cfg):
    mode = cfg["scope"]["folders"]
    if mode == "custom_vocab":
        vocab = cfg["scope"].get("vocabulary") or []
        if not vocab:
            sys.exit("folders=custom_vocab but no vocabulary given")
        listed = "\n".join(f"- `{v}/`" for v in vocab)
        return fill(read_fragment("folders_custom_vocab.md"), {"VOCAB": listed})
    fragment = {"spec_only": "folders_spec_only.md",
                "per_skill": "folders_per_skill.md"}.get(mode)
    if not fragment:
        sys.exit(f"Unknown folders mode: {mode!r}")
    return read_fragment(fragment)


def assemble(cfg, tool_name):
    with open(os.path.join(TEMPLATES, "skill_creator_base.md"), encoding="utf-8") as f:
        base = f.read()
    # The template is written for the default name; every other name is a
    # substitution on top; this needs no token because it's the one place the
    # name appears literally, right after the frontmatter delimiter.
    base = base.replace("name: skill-creator", f"name: {tool_name}", 1)

    scheme = str(cfg["versioning"]["scheme"])

    # The generated skill-creator follows the collection's own rules. A tool
    # that exempts itself from the convention it enforces teaches the user to
    # ignore its warnings.
    initial = cfg["versioning"].get("initial_version", "")
    metadata = (f"metadata:\n  version: {initial}\n"
                if scheme != "none" and initial else "")

    tokens = {
        "METADATA": metadata,
        "NAMING": naming_block(cfg),
        "VERSIONING": versioning_block(cfg),
        "CHANGELOG": read_fragment(f"changelog_{cfg['changelog']}.md"),
        "IDENTIFICATION": identification_block(cfg),
        "FOLDERS": folders_block(cfg),
        "BODY_STRUCTURE": read_fragment(
            f"body_{cfg['rigor']['body_structure']}.md"),
        "EVALUATION": (read_fragment("evaluation.md")
                       if cfg["scope"]["evaluation"] else ""),
        "PACKAGING": (read_fragment("packaging.md")
                      if cfg["scope"]["packaging_gate"] else ""),
        "OUTPUT_VERSION_LINE": (
            "" if scheme == "none"
            else f"VERSION:     {cfg['versioning']['initial_version']}"),
    }

    text = fill(base, tokens)
    # Collapse the gaps left where an empty fragment was substituted.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip("\n") + "\n"


def validate_config(cfg):
    missing = [k for k in REQUIRED_KEYS if k not in cfg]
    if missing:
        sys.exit(f"Config is missing required keys: {missing}")
    if str(cfg["versioning"]["scheme"]) != "none" \
            and not cfg["versioning"].get("initial_version"):
        sys.exit("A versioning scheme was chosen but no initial_version given")
    if cfg["changelog"] not in ("always", "threshold", "never"):
        sys.exit(f"Unknown changelog mode: {cfg['changelog']!r}")
    if cfg["rigor"]["body_structure"] not in ("fixed", "suggested", "free"):
        sys.exit(f"Unknown body_structure: {cfg['rigor']['body_structure']!r}")


def generate(config_path, destination):
    with open(config_path, encoding="utf-8") as f:
        cfg = json.load(f)
    validate_config(cfg)

    tool_name = cfg.get("tool_name") or DEFAULT_TOOL_NAME
    validate_tool_name(tool_name)

    root = os.path.join(destination, tool_name)
    if os.path.exists(root):
        sys.exit(f"'{root}' already exists -- aborting, nothing overwritten.\n"
                 "The configurator is meant to run once. To start over, delete "
                 f"the existing {tool_name} first.")

    os.makedirs(os.path.join(root, "scripts"))

    with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(assemble(cfg, tool_name))

    with open(os.path.join(root, ".skill-config.json"), "w", encoding="utf-8") as f:
        # Two classes of key, and the difference matters. Value keys are read by
        # the scripts at runtime and referenced -- not copied -- by SKILL.md, so
        # editing them takes effect immediately. Shape keys decided which text
        # was written into SKILL.md when it was generated; editing one of those
        # changes what the scripts do while the prose keeps saying the old
        # thing. JSON has no comments, so the warning goes in the file itself.
        annotated = {
            "_readme": {
                "edit_freely": [
                    "naming.prefixes", "naming.max_segments",
                    "versioning.initial_version",
                ],
                "edit_freely_note": (
                    "Read by the scripts at runtime. SKILL.md points at this "
                    "file rather than repeating them, so a change here takes "
                    "effect with nothing else to update."),
                "requires_regenerating": [
                    "naming.convention", "versioning.scheme", "changelog",
                    "rigor.*", "scope.*",
                ],
                "requires_regenerating_note": (
                    "These decided which text was written into SKILL.md. "
                    "Changing one here changes what the scripts do while the "
                    "prose still describes the old setup. To change them, "
                    "reinstall the boilerplate and run setup again."),
            },
        }
        annotated.update(cfg)
        json.dump(annotated, f, indent=2, ensure_ascii=False)
        f.write("\n")

    for script in ("scaffold_skill.py", "validate_skill.py"):
        src = os.path.join(HERE, "generated", script)
        shutil.copy2(src, os.path.join(root, "scripts", script))

    if cfg["changelog"] == "always":
        version = (cfg["versioning"]["initial_version"]
                   if str(cfg["versioning"]["scheme"]) != "none" else "0.1.0")
        with open(os.path.join(root, "CHANGELOG.md"), "w", encoding="utf-8") as f:
            f.write("# Changelog\n\n"
                    "Format: [Keep a Changelog](https://keepachangelog.com).\n\n"
                    f"## [{version}]\n\n### Added\n- Generated by "
                    "skill-configurator.\n")

    written = sum(len(files) for _, _, files in os.walk(root))
    print(f"Generated '{root}' -- {written} files")
    for base_dir, _, files in os.walk(root):
        for name in sorted(files):
            rel = os.path.relpath(os.path.join(base_dir, name), root)
            print(f"  {rel}")
    print(f"\nNext: write the lock file, then {tool_name} is ready to use.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--config", required=True, help="path to the answers JSON")
    ap.add_argument("--destination", default=".",
                    help="where to create the tool_name folder (default: current dir)")
    a = ap.parse_args()
    generate(a.config, a.destination)


if __name__ == "__main__":
    main()
