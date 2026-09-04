## Packaging gate

Before shipping a skill, run the structural check:

```bash
python3 scripts/validate_skill.py {path-to-skill}
```

Zero errors is the bar. Warnings are read and judged; they don't block.

It checks the required frontmatter fields, the description length limit, broken
internal links, files unreachable from SKILL.md, unresolved placeholders, an
oversized SKILL.md and missing trailing newlines. It never modifies anything.

Known exceptions go in `.skillcheck-ignore`, each with its reason:

```
references/drafts/   # a path -- a trailing slash matches everything beneath
!version             # a whole check, disabled for this skill only
```

Both kinds are reported in the output rather than hidden. A silenced check
nobody can see is a check nobody will ever reconsider — which is also why they
are never silenced inside the script, where they would be invisible.

**Count the files before packaging, and after.** A zip that quietly loses a
folder produces a skill that loads without error and behaves as if half its
instructions were never written. The count is the only thing that catches it.

```bash
find {skill}/ -type f | wc -l     # before
unzip -l {skill}.zip | tail -1    # after — same number
```
