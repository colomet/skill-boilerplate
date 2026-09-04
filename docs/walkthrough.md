# How this works, start to finish

What actually happens, from installing this repo to having your first skill.
For what each setup question decides, see [configuration.md](configuration.md);
for the file format itself, [spec.md](spec.md).

## The shape of it

There are two tools, and confusing them is the easiest mistake to make. They
look similar and do entirely different jobs.

| | `skill-configurator` | the tool it generates |
|---|---|---|
| Runs | **Once**, ever | Every time you want a new skill |
| Asks about | Conventions for your whole collection | What *this one* skill does |
| Lives | Until setup is done | For as long as you keep making skills |
| Then | Can be deleted | Stays |

The configurator does not make skills. It makes the thing that makes skills.

---

## Part one — setup, once

### 1. Install the configurator

Copy `skills/skill-configurator/` to wherever your environment keeps skills:

- **Claude.ai** — zip the folder, then Settings → Capabilities → Skills → upload
- **Claude Code** — drop it in your skills directory, or install this repo as a
  plugin

Nothing else from this repository needs to go with it. The configurator folder
is self-contained; `docs/`, `tests/` and `template/` are for people reading the
repo, not for the tool.

### 2. Start it

Ask in plain language — *"set up the skill boilerplate"*, *"let's configure
this"*, *"I want to start making skills"*. You don't invoke it by name.

### 3. It checks whether setup already ran

If it finds a lock file, it stops and says so rather than quietly starting over.
See [why one-shot](configuration.md#why-one-shot).

### 4. Eleven questions, in four rounds

| Round | Decides |
|---|---|
| 1 · The three shapes | Whether names are grouped · version numbers · changelog |
| 2 · Filling in round 1 | Which groups · how many words in a name · starting number |
| 3 · Presentation | Section layout · header table |
| 4 · What the tool does | Trigger testing · final check · sub-folders |

Round 2 exists because it depends on round 1 — a round is answered all at once,
so "which group names?" can't sit beside "do you want groups at all?". If you
answered no to grouping, round 2 skips that question entirely.

Every question offers a neutral option. Nothing here is mandatory.

### 5. One more: naming the tool itself

Defaults to `my-skill-creator`. Not `skill-creator` — Anthropic ships a skill
with that exact name, and two folders with one name is a collision. You can pick
anything, as long as it isn't reserved (`claude`, `anthropic`).

### 6. It reads your answers back

Not as labels. As consequences, in your own terms:

```
Names          finance-report-builder  (grouped by area, at most 3 words)
Groups         finance, hr, ops, sales, legal, it
Versions       1.4.0 — new skills start at 1.0.0
Changelog      starts inside SKILL.md, moves out when it grows
Layout         a suggested one, ignore it when it doesn't fit
Header table   Area, Version
Trigger tests  not included
Final check    required before finishing
Folders        the standard three only
Tool name      my-skill-creator
```

Correct anything, as many times as you want. This is the last reversible moment.

### 7. It generates, and locks

```
my-skill-creator/
├── SKILL.md
├── .skill-config.json
└── scripts/
    ├── scaffold_skill.py
    └── validate_skill.py
```

A `CHANGELOG.md` appears here too if you asked for one from the start.

Install this the same way you installed the configurator. The configurator has
no further purpose — delete it whenever you like.

---

## Part two — making skills, from now on

Ask the generated tool for a skill: *"create a skill for X"*, *"I want Claude to
handle Y"*. It runs through:

### Step 0 — Should this be a skill at all?

Two questions before anything gets built.

**Is this going to repeat?** A skill earns its place when there's a workflow
you'll run again. A one-off task doesn't need one — a good prompt does the job
without leaving anything behind to maintain. If the answer is no, it says so and
offers the prompt instead. It won't refuse; it won't build it silently either.

**What are two or three real requests this should handle?** Actual sentences,
the way someone would type them. These bound the scope, and they become the raw
material for the `description` — which is the only thing that decides whether
the skill ever loads.

### Step 0b — What you already have

At most three questions, and only what can't be inferred: do you have a name
already, a partial draft, or just an idea?

### Step 1 — Naming

Reads your installed skills and `.skill-config.json` before proposing anything —
the first to catch collisions, the second because conventions can be edited
between sessions and the scripts obey the file, not anyone's memory.

### Step 2 — Writing the body

Following the layout you chose, with the header table you specified.

### Step 3 — Folders

Only the ones actually needed. An empty folder is a promise nobody keeps.

Then versioning, changelog and the packaging gate, according to your setup.

---

## Changing your mind later

**Three things you can edit directly** in `.skill-config.json`, no reinstall
needed: the group list, the word cap, and the starting version. The scripts read
that file at runtime, and the generated `SKILL.md` points at it rather than
repeating the values, so a change takes effect with nothing else to update. The
file says which keys these are, under `_readme`.

**Everything else means starting over**: delete the generated tool, re-download
this repo, install the configurator fresh. Those answers decided what text got
written into the skill, so changing them in the JSON would make the scripts do
one thing while the instructions still describe another.

That's deliberate. A configurator you can re-run mid-life produces a split
collection — skills built under the old answers, skills built under the new
ones, and nothing recording which is which.

---

## If you'd rather skip all of this

`template/` is a plain skill skeleton: a valid `SKILL.md` and nothing else. Copy
it, fill it in, ignore the rest of this repo. The three optional folders are
documented in a comment inside it, to be created when you have something to put
in them.
