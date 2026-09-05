# Updating, extending, making it yours

Everything after the first install.

## The short version

Three separate things can be updated, and they don't move together:

| Thing | Updated how | Loses your setup? |
| :--- | :--- | :--- |
| The boilerplate | reinstall or `/plugin update` | It's already spent — nothing to lose |
| Your generated tool | edit it, or regenerate from scratch | Regenerating does, editing doesn't |
| The skills you made | they're yours; nothing here touches them | No |

The important one is the third. **Updating anything here never touches skills
you've already written.** They're plain folders with no link back.

## Updating the boilerplate

A new version fixes bugs in the generator or the scripts it emits. It does not
reach into a tool you already generated.

**Installed as a Claude Code plugin:**

```
/plugin update skill-boilerplate@colomet-skills
```

**Installed from the zip on claude.ai:** download the newer
`skill-boilerplate.zip` from
[releases](https://github.com/colomet/skill-boilerplate/releases) and upload it
again. Replace the skill rather than adding a second copy — two skills with the
same name is a coin toss over which one loads.

**Installed by hand:**

```bash
git pull
cp -r skills/skill-boilerplate ~/.claude/skills/
```

Worth knowing: if you already ran setup, the newer copy is locked too — the lock
lives with the generated tool, not with the download. Updating gives you a
better boilerplate you have no reason to run. That's only worth doing if you
intend to generate a fresh tool.

## Getting fixes into a tool you already generated

Your generated tool carries a copy of `scaffold_skill.py` and
`validate_skill.py` as they were on the day you generated it. A later fix to
those scripts does not travel to you.

Two ways to pick one up.

**Copy the file across** — for a fix that doesn't depend on your answers, which
is most of them:

```bash
cp skills/skill-boilerplate/scripts/generated/validate_skill.py \
   my-skill-creator/scripts/
```

Both scripts read `.skill-config.json` at runtime rather than having your
choices compiled in, so a newer copy still obeys your conventions. Check the
[changelog](../CHANGELOG.md) first — if an entry mentions a config key you don't
have, add it to your JSON before copying.

**Regenerate** — when the fix is in the generator itself, or in the text it
writes into `SKILL.md`. Reinstall the boilerplate, run setup again, and answer
as before. You'll get a fresh tool. Skills you already made are unaffected;
they don't consult the tool that made them.

## What you can change without regenerating

Three values live in `.skill-config.json` and are read at runtime. Edit the
file and the change takes effect immediately:

- the list of group or prefix names
- the cap on words in a name
- the starting version number

The file lists these under `_readme`, so it says so on its own without you
remembering this page.

**Everything else means starting over.** The other answers decided what
sentences got written into the generated `SKILL.md`. Editing the JSON would
leave the scripts doing one thing while the instructions still described
another — and the instructions are what Claude reads. A tool that contradicts
itself is worse than one you have to rebuild.

## Extending

### Adding your own skills to a copy of this repository

The layout supports more than one skill. `skills/` is a folder of folders:

```
skills/
├── skill-boilerplate/
└── your-other-skill/
```

Two things to update when you add one:

1. **`.claude-plugin/marketplace.json`** — add an entry if you want it
   installable separately. With a single `skills/` folder shared at the
   marketplace root, list the subdirectory explicitly rather than relying on
   the default scan.
2. **The packaging script** takes any skill folder, so nothing there changes:

```bash
python3 scripts/build_skill_zip.py skills/your-other-skill
```

### Forking this as your own collection

If you want the machinery but under your own name:

- **`LICENSE`** — Apache 2.0 requires you keep the original copyright line.
  Add yours; don't replace it.
- **`.claude-plugin/marketplace.json`** — change `name` and `owner`. The
  marketplace name is what people type after the `@`, so
  `skill-boilerplate@your-marketplace`.
- **`.claude-plugin/plugin.json`** — change `repository` and `homepage`.
- **`.github/ISSUE_TEMPLATE/config.yml`** — the contact links point at this
  repository by URL.
- **`README.md`** — the install commands name `colomet/skill-boilerplate`.

The test suite checks that the two manifests agree with each other, so a rename
that only half lands fails rather than shipping.

### Changing what the wizard asks

The twelve questions live in `SKILL.md`; the text they produce lives in
`scripts/templates/fragments/`, one file per answer. Adding an option means a
new fragment and a new branch in `generate_skill_creator.py`.

Before adding one, the question worth asking is whether it's a real choice.
Some things aren't preferences — the description limit, keeping `SKILL.md`
lean, a skill citing nothing outside its own folder. Those hold regardless of
taste, and the README lists them. A question that only has one sensible answer
costs the user a decision and buys nothing.

## Working on the repository itself

```bash
python3 tests/test_boilerplate.py     # standard library only
```

No dependencies. Python 3.8 or newer. CI runs the same command on Linux, macOS
and Windows on every push and pull request.

The suite covers more than the generator: it checks the shape of the uploadable
archive, that the manifests agree, that the licence has a real copyright
holder, and that community files sit where GitHub looks for them. Several of
those exist because the thing they check was wrong once in a way nothing failed
on.

See [CONTRIBUTING.md](../.github/CONTRIBUTING.md) for the workflow.

## Publishing a version

For whoever maintains a fork. Pushing a tag does the rest.

1. Update `CHANGELOG.md` — move `[Unreleased]` entries under a dated version.
2. Update `version` in `.claude-plugin/plugin.json` to match. Don't add a
   `version` to the marketplace entry as well; when both carry one, the stale
   manifest wins silently.
3. Commit, and wait for CI to pass on `main`.
4. Tag and push:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

`.github/workflows/release.yml` takes it from there: it checks the tag against
the manifest and stops if they disagree, runs the suite once more, builds
`skill-boilerplate.zip`, creates the release, and attaches the archive with
notes cut from the changelog section matching the tag.

If a release already exists for that tag, the workflow updates its notes and
replaces the asset rather than failing. You can also re-run it by hand from the
Actions tab against any existing tag.

### What a release page holds

Three downloads, and only one is uploadable.

| Download | What it is |
| :--- | :--- |
| `skill-boilerplate.zip` | **The one to upload.** Rooted at the skill folder |
| Source code (zip) | The repository, minus development scaffolding |
| Source code (tar.gz) | The same, other format |

GitHub adds the two source downloads to every release and there is no setting
to remove them. Neither is in the shape claude.ai accepts: `git archive` always
roots at `<repo>-<tag>/`, leaving the skill under `skills/`, while an upload
has to be rooted at the skill folder itself. `export-ignore` trims what goes
in, not where the root sits — which is why the usable archive is built
separately and attached, and why the notes open by naming it.

What `export-ignore` does do is keep `tests/`, `scripts/` and `.github/` out of
those two, on the reasoning that a release is for installing and a clone is for
changing. That applies to the green **Code > Download ZIP** button as well, so
anyone meaning to work on the code should clone rather than download —
`CONTRIBUTING.md` says so.

A version number that has been published is never reused, even for a fix that
arrives minutes later. Someone may already have the old one.
