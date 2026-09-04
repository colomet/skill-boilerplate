#!/usr/bin/env python3
"""Scaffold a new skill, following this collection's conventions.

    python3 scaffold_skill.py my-new-skill
    python3 scaffold_skill.py my-new-skill --references --scripts
    python3 scaffold_skill.py my-new-skill --destination ../skills

Conventions (naming, versioning, changelog) are read from
`.skill-config.json` in the parent skill folder. If that file is missing, the
script falls back to the format's own minimum: lowercase, hyphens, no version.

What it deliberately does not do:

- Does not pick the name. It checks the format and warns about convention
  mismatches, but never silently "fixes" a name.
- Does not create folders you didn't ask for. An empty folder is a promise
  nobody keeps.
- Does not overwrite. If the destination exists, it aborts.
- Does not write the description. It leaves a marked placeholder, which
  validate_skill.py will flag until filled. The description decides whether the
  skill ever triggers; a generated one would be worse than a visible gap.

Requires Python 3.8+. Standard library only.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(os.path.dirname(HERE), ".skill-config.json")

SKILL_MD = """---
name: {name}
{metadata}description: "[FILL IN: what this skill does and exactly when to use it -- the phrases a user would actually type, not just the topic]"
---

# {title}

[FILL IN: what this skill does, in a sentence or two.]

## When NOT to use this

- [A situation this should not fire for -- especially if a neighbouring skill
  covers it]

## Instructions

[FILL IN: the steps, rules or knowledge to follow.]
"""

CHANGELOG = """# Changelog

Format: [Keep a Changelog](https://keepachangelog.com).

## [{version}]

### Added
- Initial version.
"""


def load_config():
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def check_format(name):
    """Format rules from the skill spec itself, not from anyone's preference."""
    if not name or name != name.lower():
        return "must be lowercase"
    if not all(c.isalnum() or c == "-" for c in name):
        return "only letters, digits and hyphens"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return "no leading, trailing or doubled hyphens"
    return None


def check_convention(name, cfg):
    """Warnings only -- the user's convention is a convention, not a law."""
    if not cfg:
        return []
    out = []
    naming = cfg.get("naming", {})
    segments = name.split("-")

    max_seg = naming.get("max_segments")
    if max_seg and len(segments) > max_seg:
        out.append(f"{len(segments)} segments, convention says at most {max_seg}")

    prefixes = naming.get("prefixes") or []
    convention = naming.get("convention")
    if prefixes and convention in ("prefix", "prefix_block"):
        if segments[0] not in prefixes:
            out.append(f"prefix '{segments[0]}' is not one of: "
                       + ", ".join(prefixes))
    if convention == "prefix_block" and len(segments) < 3:
        out.append("convention is prefix-block-type, this has fewer segments")
    if convention == "flat" and len(segments) > 1 and prefixes:
        out.append("convention is flat names without a prefix")
    return out


def scaffold(name, destination, folders, cfg):
    problem = check_format(name)
    if problem:
        sys.exit(f"Invalid name '{name}': {problem}")

    for warning in check_convention(name, cfg):
        print(f"  warning: {warning}")

    root = os.path.join(destination, name)
    if os.path.exists(root):
        sys.exit(f"'{root}' already exists -- aborting, nothing overwritten")

    scheme = str((cfg or {}).get("versioning", {}).get("scheme", "none"))
    version = (cfg or {}).get("versioning", {}).get("initial_version", "")
    metadata = (f"metadata:\n  version: {version}\n"
                if scheme != "none" and version else "")

    os.makedirs(root)
    title = " ".join(w.capitalize() for w in name.split("-"))
    with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(SKILL_MD.format(name=name, title=title, metadata=metadata))

    created = ["SKILL.md"]
    if (cfg or {}).get("changelog") == "always":
        with open(os.path.join(root, "CHANGELOG.md"), "w", encoding="utf-8") as f:
            f.write(CHANGELOG.format(version=version or "0.1.0"))
        created.append("CHANGELOG.md")

    for folder in folders:
        os.makedirs(os.path.join(root, folder))
        created.append(folder + "/")

    print(f"Scaffolded '{root}'")
    for item in created:
        print(f"  {item}")
    print("\nNext: fill in the description, then run validate_skill.py")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("name", help="skill name: lowercase, hyphens")
    ap.add_argument("--destination", default=".",
                    help="where to create it (default: current dir)")
    ap.add_argument("--references", action="store_true")
    ap.add_argument("--scripts", action="store_true")
    ap.add_argument("--assets", action="store_true")
    a = ap.parse_args()

    folders = [f for f, on in (("references", a.references),
                               ("scripts", a.scripts),
                               ("assets", a.assets)) if on]
    cfg = load_config()
    if cfg is None:
        print("  note: no .skill-config.json found, using format defaults only")
    scaffold(a.name, a.destination, folders, cfg)


if __name__ == "__main__":
    main()
