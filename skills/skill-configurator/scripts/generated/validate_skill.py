#!/usr/bin/env python3
"""Validate a skill's structure. Reads and reports; never modifies anything.

    python3 validate_skill.py path/to/my-skill
    python3 validate_skill.py path/to/skills-dir --all
    python3 validate_skill.py path/to/my-skill --errors-only

Checks the required frontmatter, the description length limit, broken internal
references, files unreachable from SKILL.md, unresolved placeholders, an
oversized SKILL.md, and missing trailing newlines. Convention checks (naming,
versioning) come from `.skill-config.json` when it is present, and are skipped
when it isn't.

Findings are ERROR (must fix), WARN (judge it yourself) or INFO. Exit status is
1 if there is any ERROR, 0 otherwise -- so it can gate a build.

Paths that legitimately don't resolve belong in `.skillcheck-ignore`, one per
line with a `#` reason. They are never silenced inside this script, where they
would be invisible to whoever reads the output.

Requires Python 3.8+. Standard library only. The frontmatter parser is
hand-rolled on purpose: requiring PyYAML would make this fail to run in exactly
the minimal environments where it is most needed.
"""

import argparse
import json
import os
import re
import sys

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
DESCRIPTION_LIMIT = 1024
BODY_LINE_LIMIT = 500
WORD_LIMIT = 5000
SPEC_FOLDERS = ("references", "scripts", "assets")

RE_PATH = re.compile(
    r"(?<![\w/-])(references|scripts|assets)/[A-Za-z0-9_./-]+"
    r"\.(?:md|py|js|json|csv|html|txt|ya?ml)(?![A-Za-z0-9])")
RE_PLACEHOLDER = re.compile(
    r"\[FILL IN[^\]]*\]|\bTODO\b|\bFIXME\b|\bTBD\b|<PLACEHOLDER>")
RE_TOKEN = re.compile(r"\{\{[A-Z_]+\}\}")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_frontmatter(text):
    """Return (fields, body). Minimal parser: top-level scalars and one level
    of nesting, which is all the skill frontmatter schema allows."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4:]

    data, key, buf, nested = {}, None, [], None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        indented = line[0] in " \t"
        m = re.match(r"^\s*([\w-]+):\s*(.*)$", line)
        if m and not indented:
            if key:
                data[key] = " ".join(buf).strip().strip('"').strip("'")
            key, val = m.group(1), m.group(2).strip()
            nested = key if val == "" else None
            buf = [] if val in (">", "|", "") else [val]
        elif m and indented and nested:
            data.setdefault(nested + "." + m.group(1), m.group(2).strip())
        elif key:
            buf.append(line.strip())
    if key:
        data[key] = " ".join(buf).strip().strip('"').strip("'")
    return data, body


def walk_files(root, exts):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs
                   if d not in (".git", "__pycache__", ".pytest_cache")]
        for name in files:
            if name.endswith(exts):
                yield os.path.relpath(os.path.join(base, name), root)


def load_ignore(root):
    """Read `.skillcheck-ignore`: what is expected to be irregular, and why.

    Two kinds of entry:

        references/templates/     # a path -- trailing / matches everything under it
        !version                  # a whole check, for this skill only

    A path entry silences every check for that path, not only the link check. A
    file of template fragments, for instance, legitimately holds unsubstituted
    tokens and points at paths that exist only in its own output; flagging it
    forever would train the reader to skim past real findings.

    A `!check` entry is the escape hatch for a skill that genuinely sits outside
    the convention -- tooling that builds the collection rather than belonging
    to it. Both kinds require a reason, so the next reader can judge whether it
    still holds.
    """
    path = os.path.join(root, ".skillcheck-ignore")
    paths, checks = {}, {}
    if os.path.isfile(path):
        for line in read(path).split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            target, _, reason = line.partition("#")
            target, reason = target.strip(), reason.strip() or "no reason given"
            if target.startswith("!"):
                checks[target[1:]] = reason
            else:
                paths[target] = reason
    return paths, checks


def is_ignored(rel, ignore):
    if rel in ignore:
        return True
    return any(prefix.endswith("/") and rel.startswith(prefix)
               for prefix in ignore)


def load_config(root):
    """Find the collection's conventions.

    Order matters. A skill carrying its own config wins; otherwise fall back to
    the one beside this script, which is the skill-creator's -- that is the case
    whenever a sibling skill is being validated, and it is the common case.
    """
    script_config = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".skill-config.json")
    for candidate in (os.path.join(root, ".skill-config.json"),
                      script_config,
                      os.path.join(os.path.dirname(os.path.abspath(root)),
                                   ".skill-config.json")):
        try:
            with open(candidate, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
    return None


# --- checks -----------------------------------------------------------------

def check_frontmatter(root, ctx):
    out, fm = [], ctx["fm"]
    folder = os.path.basename(os.path.abspath(root))

    if not fm.get("name"):
        out.append((ERROR, "frontmatter", "missing required field `name`"))
    elif fm["name"] != folder:
        out.append((WARN, "frontmatter",
                    f"`name: {fm['name']}` does not match folder `{folder}`"))

    desc = fm.get("description", "")
    if not desc:
        out.append((ERROR, "frontmatter", "missing required field `description`"))
    elif len(desc) > DESCRIPTION_LIMIT:
        out.append((ERROR, "frontmatter",
                    f"description is {len(desc)} chars, over the "
                    f"{DESCRIPTION_LIMIT} limit -- it will be truncated "
                    f"silently, and the tail is where triggers live"))
    elif len(desc) > DESCRIPTION_LIMIT - 24:
        out.append((WARN, "frontmatter",
                    f"description is {len(desc)} chars, close to the "
                    f"{DESCRIPTION_LIMIT} limit"))

    for field in fm:
        if field in ("version", "project"):
            out.append((ERROR, "frontmatter",
                        f"`{field}` is not valid at the top level -- it must be "
                        f"nested under `metadata:`"))
    return out


def check_version(root, ctx):
    cfg = ctx["cfg"]
    if not cfg:
        return []
    scheme = str(cfg.get("versioning", {}).get("scheme", "none"))
    version = ctx["fm"].get("metadata.version")
    if scheme == "none":
        return []
    if not version:
        return [(WARN, "version",
                 "no `metadata.version`, but this collection uses versioning")]
    parts = version.split(".")
    if len(parts) != int(scheme):
        return [(WARN, "version",
                 f"version `{version}` has {len(parts)} parts, convention is "
                 f"{scheme}")]
    return []


def check_links(root, ctx):
    ignore, _ = load_ignore(root)
    broken = {}
    files = list(walk_files(root, (".md",))) + list(walk_files(root, (".py", ".js")))
    for rel in files:
        if is_ignored(rel, ignore):
            continue
        for match in RE_PATH.finditer(read(os.path.join(root, rel))):
            target = match.group(0)
            if is_ignored(target, ignore):
                continue
            if not os.path.exists(os.path.join(root, target)):
                broken.setdefault(target, set()).add(rel)
    out = [(ERROR, "links", f"`{t}` referenced in {sorted(v)} does not exist")
           for t, v in sorted(broken.items())]
    out += [(INFO, "links", f"declared exception: `{t}` -- {why}")
            for t, why in sorted(ignore.items())]
    return out


def check_reachable(root, ctx):
    by_name = {os.path.basename(rel): rel for rel in walk_files(root, (".md",))}
    if "SKILL.md" not in by_name:
        return []
    reached, frontier = {"SKILL.md"}, ["SKILL.md"]
    while frontier:
        text = read(os.path.join(root, frontier.pop()))
        for match in RE_PATH.finditer(text):
            target = by_name.get(os.path.basename(match.group(0)))
            if target and target not in reached:
                reached.add(target)
                frontier.append(target)
    ignore, _ = load_ignore(root)
    orphans = sorted(rel for rel in set(by_name.values()) - reached
                     if rel != "CHANGELOG.md"
                     and not is_ignored(rel, ignore))
    return [(WARN, "reachable",
             f"`{rel}` is not linked from SKILL.md, directly or indirectly -- "
             f"a file nobody links to exists but cannot be found")
            for rel in orphans]


def check_size(root, ctx):
    lines = len(ctx["text"].split("\n"))
    words = len(ctx["text"].split())
    out = []
    if lines > BODY_LINE_LIMIT:
        out.append((WARN, "size",
                    f"SKILL.md is {lines} lines, over the {BODY_LINE_LIMIT} "
                    f"guideline -- move detail into references/, which is "
                    f"loaded only when needed"))
    if words > WORD_LIMIT:
        out.append((WARN, "size",
                    f"SKILL.md is about {words} words, over the {WORD_LIMIT} "
                    f"the format's own guidance suggests"))
    return out


def check_placeholders(root, ctx):
    out = []
    desc = ctx["fm"].get("description", "")
    if RE_PLACEHOLDER.search(desc):
        out.append((ERROR, "placeholders",
                    "the description still contains a placeholder -- the skill "
                    "will never trigger like this"))
    ignore, _ = load_ignore(root)
    for rel in walk_files(root, (".md",)):
        if is_ignored(rel, ignore):
            continue
        text = read(os.path.join(root, rel))
        count = len(RE_PLACEHOLDER.findall(text))
        if count and not (rel == "SKILL.md" and RE_PLACEHOLDER.search(desc)):
            out.append((WARN, "placeholders",
                        f"{rel}: {count} unresolved placeholder(s)"))
        if RE_TOKEN.search(text):
            out.append((ERROR, "placeholders",
                        f"{rel}: unsubstituted template token(s)"))
    return out


def check_newline(root, ctx):
    out = []
    ignore, _ = load_ignore(root)
    for rel in list(walk_files(root, (".md",))) + list(walk_files(root, (".py",))):
        if is_ignored(rel, ignore):
            continue
        path = os.path.join(root, rel)
        try:
            if os.path.getsize(path) == 0:
                out.append((WARN, "newline", f"{rel}: file is empty"))
                continue
            with open(path, "rb") as f:
                f.seek(-1, os.SEEK_END)
                if f.read(1) not in (b"\n", b"\r"):
                    out.append((WARN, "newline", f"{rel}: no trailing newline"))
        except OSError:
            pass
    return out


def check_reserved_and_syntax(root, ctx):
    """Rules from the skill format itself, not from anyone's preference.

    Names containing "claude" or "anthropic" are reserved. Angle brackets are
    forbidden in frontmatter because the frontmatter is placed in the model's
    system prompt, where `<...>` can be read as markup and turned into an
    injection vector.
    """
    out, fm = [], ctx["fm"]
    name = fm.get("name", "")
    for reserved in ("claude", "anthropic"):
        if reserved in name.lower():
            out.append((ERROR, "reserved",
                        f"`{reserved}` is reserved and cannot appear in a "
                        f"skill name"))

    raw = ctx["text"]
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        frontmatter = raw[3:end] if end != -1 else ""
        # Only `<` is flagged. A lone `>` cannot open a tag, and YAML uses it as
        # the folded-scalar indicator (`description: >`), which is legitimate
        # syntax -- flagging it would fail every skill that wraps a long
        # description across lines.
        if "<" in frontmatter:
            out.append((ERROR, "syntax",
                        "angle brackets in the frontmatter -- forbidden, since "
                        "the frontmatter goes into the system prompt"))
    return out


def check_no_readme(root, ctx):
    """A skill folder carries no README.

    Everything a reader needs is in SKILL.md or references/. A README inside a
    skill is documentation the model may never read and the user may never
    find, kept in step with nothing. Repository-level READMEs are a different
    thing and belong outside the skill folder.
    """
    for name in os.listdir(root):
        if name.lower() == "readme.md":
            return [(WARN, "readme",
                     "a skill folder should carry no README.md -- put that "
                     "content in SKILL.md or references/, and keep repository "
                     "READMEs outside the skill folder")]
    return []


def check_structure(root, ctx):
    present = [d for d in SPEC_FOLDERS if os.path.isdir(os.path.join(root, d))]
    others = sorted(d for d in os.listdir(root)
                    if os.path.isdir(os.path.join(root, d))
                    and d not in SPEC_FOLDERS and not d.startswith(".")
                    and d != "__pycache__")
    out = [(INFO, "structure",
            "spec folders present: " + ", ".join(f"`{d}/`" for d in present))
           if present else (INFO, "structure", "single-file skill")]
    out += [(WARN, "structure",
             f"`{d}/` is not one of the three folders the format defines. "
             f"Subdivide inside `references/{d}/` instead -- that path is "
             f"predictable from outside the skill, an invented top-level name "
             f"is not")
            for d in others]
    for d in present:
        contents = os.listdir(os.path.join(root, d))
        # A folder holding only a git placeholder is empty in every sense that
        # matters: the reader still has to open it to find that out. Counting
        # .gitkeep as content would blind this check to the exact case it
        # exists for.
        real = [f for f in contents if f not in (".gitkeep", ".keep")]
        if not real:
            what = "empty" if not contents else "only a git placeholder"
            out.append((WARN, "structure",
                        f"`{d}/` holds {what} -- a folder created before it "
                        f"has content is a promise nobody keeps"))
    return out


CHECKS = (check_frontmatter, check_reserved_and_syntax, check_version,
          check_links, check_reachable, check_size, check_placeholders,
          check_newline, check_no_readme, check_structure)


def validate(root):
    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [(ERROR, "structure", "no SKILL.md -- this is not a skill")]
    text = read(skill_md)
    fm, body = parse_frontmatter(text)
    ctx = {"fm": fm, "text": text, "body": body, "cfg": load_config(root)}
    _, skipped = load_ignore(root)

    out = []
    for check in CHECKS:
        name = check.__name__.replace("check_", "")
        if name in skipped:
            # Reported, not hidden. A silenced check the reader can't see is a
            # check nobody will ever reconsider.
            out.append((INFO, "skipped",
                        f"check `{name}` disabled -- {skipped[name]}"))
            continue
        try:
            out += check(root, ctx)
        except Exception as exc:                      # noqa: BLE001
            out.append((ERROR, check.__name__, f"check crashed: {exc}"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("--all", action="store_true",
                    help="path holds several skill folders")
    ap.add_argument("--errors-only", action="store_true")
    a = ap.parse_args()

    if not os.path.isdir(a.path):
        sys.exit(f"'{a.path}' is not a directory")

    targets = ([os.path.join(a.path, d) for d in sorted(os.listdir(a.path))
                if os.path.isdir(os.path.join(a.path, d)) and not d.startswith(".")]
               if a.all else [a.path])

    totals = {ERROR: 0, WARN: 0, INFO: 0}
    for target in targets:
        results = validate(target)
        if a.errors_only:
            results = [r for r in results if r[0] == ERROR]
        for level, _, _ in results:
            totals[level] += 1
        failed = any(r[0] == ERROR for r in results)
        print(f"\n{'!!' if failed else 'OK'} "
              f"{os.path.basename(target.rstrip(os.sep)) or target}")
        if not results:
            print("   no findings")
        for level, rule, message in results:
            print(f"   [{level:<5}] {rule:<13} {message}")

    print(f"\n{'-' * 72}\n{totals[ERROR]} errors, {totals[WARN]} warnings, "
          f"{totals[INFO]} info across {len(targets)} skill(s)")
    return 1 if totals[ERROR] else 0


if __name__ == "__main__":
    sys.exit(main())
