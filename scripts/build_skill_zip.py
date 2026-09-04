#!/usr/bin/env python3
"""Build the archive that claude.ai accepts as a skill upload.

    python3 scripts/build_skill_zip.py

Standard library only. Run from anywhere; paths resolve against the repository.

claude.ai wants a zip whose root is the skill folder itself -- not the
repository, and not a folder containing the repository. Cloning this repo and
zipping what you get produces the wrong shape, so this script produces the
right one:

    skill-boilerplate.zip
    └── skill-boilerplate/
        ├── SKILL.md
        └── scripts/...

The file count is printed and checked against the source folder, because a zip
that silently drops a directory produces a skill that installs cleanly and
behaves as though half its instructions were never written.
"""

import argparse
import os
import sys
import zipfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SKILL = os.path.join(REPO_ROOT, "skills", "skill-boilerplate")
DEFAULT_OUTPUT_DIR = os.path.join(REPO_ROOT, "dist")

# Never ship these, whatever the filesystem happens to be holding.
EXCLUDED_DIRS = {"__pycache__", ".git", ".pytest_cache", ".venv"}
EXCLUDED_SUFFIXES = (".pyc", ".pyo", ".zip", ".skill")
EXCLUDED_NAMES = {".DS_Store", ".configured"}


def collect_files(skill_dir):
    """Return the files to archive, as paths relative to the skill folder."""
    collected = []
    for current, dirs, files in os.walk(skill_dir):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        for name in sorted(files):
            if name in EXCLUDED_NAMES or name.endswith(EXCLUDED_SUFFIXES):
                continue
            full = os.path.join(current, name)
            collected.append(os.path.relpath(full, skill_dir))
    return collected


def build(skill_dir, output_dir):
    skill_dir = os.path.abspath(skill_dir)
    if not os.path.isdir(skill_dir):
        sys.exit("Not a directory: {}".format(skill_dir))
    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        sys.exit("No SKILL.md in {} -- that isn't a skill folder.".format(skill_dir))

    skill_name = os.path.basename(skill_dir.rstrip(os.sep))
    members = collect_files(skill_dir)
    if not members:
        sys.exit("Nothing to archive in {}".format(skill_dir))

    os.makedirs(output_dir, exist_ok=True)
    archive = os.path.join(output_dir, skill_name + ".zip")

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for relative in members:
            # Forward slashes in the archive on every platform, including Windows.
            arcname = "/".join([skill_name] + relative.split(os.sep))
            zf.write(os.path.join(skill_dir, relative), arcname)

    with zipfile.ZipFile(archive) as zf:
        written = [n for n in zf.namelist() if not n.endswith("/")]

    if len(written) != len(members):
        sys.exit(
            "Count mismatch: {} files on disk, {} in the archive.".format(
                len(members), len(written)
            )
        )

    print("{}  ({} files)".format(os.path.relpath(archive, os.getcwd()), len(written)))
    print("Upload it at claude.ai: Customize > Skills > + > Upload a skill.")
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "skill",
        nargs="?",
        default=DEFAULT_SKILL,
        help="Skill folder to package (default: skills/skill-boilerplate)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Where to write the archive (default: dist/)",
    )
    args = parser.parse_args()
    build(args.skill, args.output_dir)


if __name__ == "__main__":
    main()
