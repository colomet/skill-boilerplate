# Skill Boilerplate

A starting point for building [Claude Skills](https://agentskills.io/specification)
that doesn't come with someone else's conventions baked in.

Most skill templates make choices for you — how names are formed, whether
there's a version number, what a skill body has to contain. Those choices are
usually reasonable for whoever wrote them and arbitrary for everyone else. This
one asks instead.

You run a setup wizard once. It asks eleven questions about naming, versioning
and documentation, plus one more for what to call the result. Then it generates
a skill with your answers
built in, and steps out of the way.

## How it works

```
install the boilerplate
        │
        ▼
  skill-boilerplate           ← runs once, asks 11 + 1 questions
        │
        ▼
   my-skill-creator           ← generated, personalized, permanent
        │
        ▼
   your skills
```

The boilerplate locks itself after running. Setup happens once per install;
changing your mind means reinstalling. [Why](docs/configuration.md#why-one-shot).

Two tools, and confusing them is the easy mistake: the boilerplate doesn't make
skills, it makes the thing that makes skills. For the full walk-through — what
happens at each step, what you're asked, what comes out — see
**[docs/walkthrough.md](docs/walkthrough.md)**.

## Layout

```
skill-boilerplate/
├── README.md · LICENSE · CHANGELOG.md    for humans, at repository level
├── .claude-plugin/                       plugin and marketplace manifests
├── .github/                              issue and pull request templates, CI
├── docs/
├── scripts/                              repository tooling, not part of a skill
├── skills/
│   └── skill-boilerplate/                the installable skill: SKILL.md, scripts/
├── template/
└── tests/
```

Skills live under `skills/`, and the separation is deliberate in both
directions: repository files never go inside a skill folder, and a skill folder
holds nothing that isn't part of the skill. In particular **a skill folder
carries no README.md** — everything a reader needs belongs in `SKILL.md` or
`references/`. The README you are reading is repository-level, which is a
different thing.

The repository, the plugin and the skill inside it all carry the same name.
That's one name to keep straight instead of three, at the cost of one stutter:
invoked explicitly as a plugin, the skill is
`/skill-boilerplate:skill-boilerplate`. Typed once, if ever — skills normally
load from their description rather than by name.

## Getting started

### Install

Pick whichever matches where you use Claude. All three install the same skill.

**claude.ai (web or desktop)** — upload a zip whose root is the skill folder.
Grab `skill-boilerplate.zip` from the
[latest release](https://github.com/colomet/skill-boilerplate/releases),
then go to **Customize > Skills > + > Upload a skill**.

Building it yourself from a clone works too — zipping the repository does not,
because the archive root has to be the skill folder:

```bash
python3 scripts/build_skill_zip.py     # writes dist/skill-boilerplate.zip
```

**Claude Code, as a plugin** — installs the whole repository and keeps it
updatable:

```
/plugin marketplace add colomet/skill-boilerplate
/plugin install skill-boilerplate@colomet-skills
```

**Claude Code, by hand** — copy the folder into your skills directory:

```bash
cp -r skills/skill-boilerplate ~/.claude/skills/
```

### Then

1. Ask Claude to set it up: *"configure the skill boilerplate"*.
2. Answer the eleven questions, plus one more: what to call the tool you're
   about to get. It defaults to `my-skill-creator`, not `skill-creator` —
   Anthropic already ships one with that exact name, so a different default
   avoids the collision without even asking, and the question still lets you
   pick something else.
3. Use the generated skill from then on: *"create a skill for X"*.

If the official skill-creator ends up installed too, the two are meant to
complement each other, not compete: the generated `description` says so
explicitly, naming what it does and does not cover (automated evaluation and
benchmarking stay with the official one; naming, versioning and documentation
conventions are this tool's job).

You can read [what each question decides](docs/configuration.md) beforehand.

## If you'd rather not answer the questions

`template/` is a plain skill skeleton: a valid `SKILL.md` and nothing else.
Copy it, fill it in, ignore everything else here.

It ships with no folders on purpose. The three optional ones are listed in a
comment inside the template, to be created when you have something to put in
them — a folder made before it has content is a promise nobody keeps, and an
empty one still has to be opened and checked by every reader who wonders what
is in it.

## What the generated tool always does

Some things aren't preferences. These hold whatever you answer, because they're
properties of the format or of not shipping broken work:

- Reads the installed skills before proposing a name, so collisions surface
  before they're a problem
- Keeps the `description` under the 1024-character limit, past which it's
  truncated silently
- Keeps `SKILL.md` lean — it's loaded on every activation, including the ones
  where the skill turns out to be irrelevant
- Treats a skill as self-contained: nothing it cites lives outside its folder,
  because a path pointing outside breaks silently at the destination
- Counts files before and after packaging, because a zip that quietly drops a
  folder produces a skill that loads fine and behaves as though half its
  instructions were never written

## Scripts

Both are pure Python, standard library only, and run outside Claude:

```bash
python3 my-skill-creator/scripts/scaffold_skill.py my-skill --references
python3 my-skill-creator/scripts/validate_skill.py my-skill
python3 my-skill-creator/scripts/validate_skill.py path/to/skills --all
```

`validate_skill.py` reads and reports; it never modifies anything. It exits 1
on errors, so it can gate a build.

Repository tooling lives in `scripts/`, outside any skill:

```bash
python3 scripts/build_skill_zip.py                 # dist/skill-boilerplate.zip
python3 scripts/build_skill_zip.py path/to/skill   # any other skill folder
```

Requires Python 3.8 or newer.

## Tests

```bash
python3 tests/test_boilerplate.py
```

Covers the generator across minimal and maximal configurations, both generated
scripts, the guarantee that the validator doesn't touch what it inspects, the
shape of the uploadable archive, and the repository's own structure — the
manifests, the community files and the licence.

No dependencies to install. CI runs the same command on Linux, macOS and
Windows, and on the oldest Python the README claims to support.

## Security

A skill can direct an agent to run code and call tools. Only use skills from
sources you trust, and audit unfamiliar ones — `SKILL.md`, scripts, assets —
before running them. That applies to this repo too.

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) and the
[Code of Conduct](.github/CODE_OF_CONDUCT.md).

## Author

Antonio D. — [GitHub](https://github.com/colomet) ·
[LinkedIn](https://www.linkedin.com/in/antonio-d/)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
