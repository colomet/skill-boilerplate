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
  skill-configurator          ← runs once, asks 11 + 1 questions
        │
        ▼
   my-skill-creator           ← generated, personalized, permanent
        │
        ▼
   your skills
```

The configurator locks itself after running. Setup happens once per install;
changing your mind means reinstalling. [Why](docs/configuration.md#why-one-shot).

Two tools, and confusing them is the easy mistake: the configurator doesn't make
skills, it makes the thing that makes skills. For the full walk-through — what
happens at each step, what you're asked, what comes out — see
**[docs/walkthrough.md](docs/walkthrough.md)**.

## Layout

```
skill-boilerplate/
├── README.md · LICENSE · CHANGELOG.md    for humans, at repository level
├── docs/
├── skills/
│   └── skill-configurator/               the installable skill: SKILL.md, scripts/
├── template/
└── tests/
```

Skills live under `skills/`, and the separation is deliberate in both
directions: repository files never go inside a skill folder, and a skill folder
holds nothing that isn't part of the skill. In particular **a skill folder
carries no README.md** — everything a reader needs belongs in `SKILL.md` or
`references/`. The README you are reading is repository-level, which is a
different thing.

## Getting started

1. Copy `skills/skill-configurator/` into wherever your Claude environment looks for
   skills — or install this repo as a Claude Code plugin.
2. Ask Claude to set it up: *"configure the skill boilerplate"*.
3. Answer the eleven questions, plus one more: what to call the tool you're
   about to get. It defaults to `my-skill-creator`, not `skill-creator` —
   Anthropic already ships one with that exact name, so a different default
   avoids the collision without even asking, and the question still lets you
   pick something else.
4. Use the generated skill from then on: *"create a skill for X"*.

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

Requires Python 3.8 or newer.

## Tests

```bash
python3 tests/test_boilerplate.py
```

Covers the generator across minimal and maximal configurations, both generated
scripts, and the guarantee that the validator doesn't touch what it inspects.

## Security

A skill can direct an agent to run code and call tools. Only use skills from
sources you trust, and audit unfamiliar ones — `SKILL.md`, scripts, assets —
before running them. That applies to this repo too.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
