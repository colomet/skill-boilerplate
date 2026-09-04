---
name: skill-boilerplate
description: "One-time setup wizard that generates a personalized skill-creator. Use when the user has just installed this boilerplate and wants to configure it, says 'set up the skill creator', 'configure the boilerplate', 'let's set this up', 'I want to start making skills', or asks how to get started with this repo. Runs once, asks eleven questions about naming conventions, versioning, layout and scope, plus one for what to call the result, then writes a ready-to-use skill-creating skill. Do NOT use this to create an individual skill -- that is what the generated tool does afterwards."
---

# Skill Boilerplate

Runs **once**. Asks eleven plain questions about how you want your skills
named, versioned and documented, then generates a skill -- named in Q12,
`my-skill-creator` by default -- with those decisions already baked in.

The questions assume no prior knowledge of the skill format. If a question
needs a term the user may not know, the question explains the term first.

After it runs, you use the generated skill for everything. This
boilerplate has no further purpose.

## When NOT to use this

- **To create an actual skill.** That is the generated skill's job.
  If it already exists, send the user there.
- **To change a decision made during setup.** This is deliberately one-shot
  (see *Why one-shot* below). To reconfigure: delete the generated
  skill, re-download this boilerplate, install it fresh.
- **To learn the SKILL.md format.** That is `docs/spec.md`.

---

## Step 0 — Find where you are, and check the lock

The skill folder may be installed read-only. Work out its path, then check
whether setup has already run:

```bash
ls -a <this-skill-folder>/ | grep -x '.configured'
```

If `.configured` exists, **stop**. Do not re-run the questions. Tell the user:

> This boilerplate has already run. Your generated skill is configured and
> ready to use — just ask it to create a skill. To start over with different
> answers, delete the generated skill, re-download the boilerplate
> and install it fresh.

If the skill folder is read-only, the lock cannot be written there. In that
case the lock is the generated skill itself: if one already exists in
the user's collection, setup has run. Say so and stop.

### Why it carries no version of its own

This boilerplate is versioned with the repository, in the top-level
`CHANGELOG.md` — not with the conventions it is about to set up. It does not
belong to the collection it creates, so a version number here would be a second
copy of a number that already lives somewhere else, free to drift.

### Why one-shot

A setup you can re-run mid-life produces a split ecosystem: skills made
before the change follow one convention, skills made after follow another, and
nothing records which is which. Locking the decisions keeps a single answer to
"how are skills named here" for as long as the install lasts. The cost —
reinstalling to change your mind — is paid once and visibly, which is the
right trade.

---

## Step 1 — The eleven questions

Four rounds, using `ask_user_input_v0`. Ask **all eleven**, in order,
even where an answer seems inferable. This is the one moment where thorough
beats quick: every unasked question becomes a guess baked into every skill the
user ever generates.

**Write for someone who has never built a skill.** No jargon in the questions
themselves — say what a thing is before asking about it, and make every option
show a concrete example rather than name a category. Every question has a
neutral option; nothing here is mandatory.

**The rounds are grouped by dependency, not by topic.** Three questions in one
round are answered simultaneously, so a question can never depend on another in
the same round. Round 2 exists because its questions need Round 1's answers.

### Round 1 — The three shapes

```
Q1  Skill names are lowercase with hyphens instead of spaces. Beyond that,
    do you want them grouped?
    A) No grouping            report-builder
    B) Grouped by area        finance-report-builder
    C) Area and sub-area      finance-monthly-report-builder
    D) I'll describe my own way

Q2  Do you want version numbers on your skills?
    A) A simple counter       4
    B) Two levels             1.4
    C) Three levels           1.4.0        (the usual choice for software)
    D) Four levels            1.4.0.1
    E) No version numbers     (nothing in the format requires them)

Q3  A changelog is a list of what changed in each version, so you can tell
    later why something is the way it is. Do you want one?
    A) Yes, from the very first version
    B) Only once there's enough history to be worth its own file
    C) No
```

### Round 2 — Filling in Round 1

Skip any question whose answer Round 1 already settled: Q4 if names aren't
grouped, Q6 if there are no version numbers.

```
Q4  Which group names do you want to start with? This becomes the list new
    names are checked against, so it's worth a moment's thought -- though you
    can always add to it later.
    A) By department          finance, hr, ops, sales, legal, it
    B) By kind of work        research, writing, analysis, review
    C) I'll type my own
    D) None yet, I'll decide as I go

Q5  How many words can a name have, separated by hyphens?
    A) At most 2              finance-report
    B) At most 3              finance-monthly-report
    C) At most 4              finance-eu-monthly-report
    D) No limit

Q6  What number does a brand-new skill start at?
    A) Start at one           1.0.0     -- it counts from the moment it works
    B) Start at zero          0.1.0     -- signals "still settling"
    C) Something else
```

### Round 3 — Presentation

```
Q7  Should every skill you write use the same section layout -- the same
    headings in the same order? A fixed layout lets you open a skill you
    wrote months ago and find things without reading it through. No layout
    means less ceremony on small skills.
    A) Same layout every time
    B) A suggested layout, ignore it when it doesn't fit
    C) No layout, write what each skill needs

Q8  Some people put a small table of facts at the top of each skill, the
    way a form has a header:

        | Area    | Finance |
        | Version | 1.4.0   |

    Which facts do you want in yours? (multi-select)
    Area / What it produces / Rules it follows / Related skills /
    Version / History / None -- no table
```

### Round 4 — What the tool does for you

```
Q9  Skills load on their own, from their description -- you don't call them
    by name. Sometimes the wrong one loads, or none does. Do you want a
    procedure for testing that: write sample requests, check which skill
    actually fires, fix the description?
    A) Yes -- worth it once you have enough skills to compete with each other
    B) No -- overkill for a handful

Q10 Before finishing a skill, a script can check it for broken links,
    missing fields and unfilled placeholders. You get the script either
    way; this decides whether running it is a required last step or up to
    you each time.
    A) Required step
    B) There if I want it

Q11 A skill can carry extra files in up to three folders: `references/` for
    documents it consults, `scripts/` for code it runs, `assets/` for
    templates and images. When one fills up you may want to split it into
    sub-folders.
    A) Just those three, nothing else
    B) Those three, plus sub-folder names I'll type
    C) Decide case by case
```

### One more, after the eleven: naming this tool itself

```
Q12 The tool you're about to get is a skill in its own right, so it needs a
    name that follows the format's own rules -- and there's already a
    skill called `skill-creator` bundled with Claude.ai and Claude Code.
    Using that exact name would collide with it if both end up installed.

    What should this one be called?
    A) my-skill-creator
    B) skill-creator          -- fine only if the official one won't be here
    C) I'll type my own name
```

If the answer contains "claude" or "anthropic", say so and ask again — those
are reserved by the format itself, not a house style choice.

### If both are ever installed together

Different names solve the folder collision. They don't by themselves stop the
two skills from competing for the same request -- "I want to create a skill"
matches both descriptions equally well, and that ambiguity is a worse failure
than a folder clash, because it doesn't error, it just picks one silently.

The generated `description` says so explicitly: what this tool is for, and
what it explicitly is not for, naming the official skill-creator by name. See
the generated skill's own `SKILL.md` frontmatter for the exact wording.

The boundary is real, not cosmetic: the official skill-creator runs automated
evaluation with graded agents and benchmarks across multiple runs, which this
tool does not attempt. This tool enforces the naming, versioning and
documentation conventions set up here, which the official one has no way to
know about. Complementary, not competing -- each covers what the other
doesn't.

### Mapping answers to the config file

The generator expects the keys below. The question numbers above are for the
user's benefit; these are what the script reads.

| Question | Config key |
|---|---|
| Q1 | `naming.convention` — `flat` / `prefix` / `prefix_block` / `custom` |
| Q2 | `versioning.scheme` — `1` / `2` / `3` / `4` / `none` |
| Q3 | `changelog` — `always` / `threshold` / `never` |
| Q4 | `naming.prefixes` — list of strings |
| Q5 | `naming.max_segments` — integer or `null` |
| Q6 | `versioning.initial_version` — string |
| Q7 | `rigor.body_structure` — `fixed` / `suggested` / `free` |
| Q8 | `rigor.identification_fields` — list of strings |
| Q9 | `scope.evaluation` — boolean |
| Q10 | `scope.packaging_gate` — boolean |
| Q11 | `scope.folders` — `spec_only` / `custom_vocab` / `per_skill`, plus `scope.vocabulary` |
| Q12 | `tool_name` — the name for the generated skill itself, default `my-skill-creator` |

## Step 2 — Confirm, in plain terms

Show the eleven answers back as **consequences, not labels**. Someone who
didn't fully follow a question won't recognise `body_structure: fixed`, but
will recognise "every skill will use the same headings in the same order" — and
recognising a wrong answer is the entire point of this step.

One line per decision, in the user's own terms:

```
Names          finance-report-builder  (grouped by area, at most 3 words)
Groups         finance, hr, ops, sales, legal, it
Versions       1.4.0 — new skills start at 1.0.0
Changelog      every skill gets one from the start
Layout         same headings, same order, every time
Header table   Area, Version
Load testing   included
Final check    required before finishing
Folders        the standard three only
```

Then one line offering more:

> Tell me any of these and I'll explain what it means and what else you could
> have picked. Change anything you like — after this I write the files, and
> setup doesn't run twice.

Correct and show the table again, as many times as the user wants. There is no
limit here: unlike a normal skill flow, a wrong answer is permanent.

Wait for an explicit go-ahead. Silence is not consent.

---

## Step 3 — Generate

Write the answers to a JSON file, then run the generator. All paths are
relative to this skill's own folder — never assume a repository layout, because
once installed there isn't one.

```bash
python3 <this-skill-folder>/scripts/generate_skill_creator.py \
  --config <answers.json> \
  --destination <where the user's skills live>
```

**If the destination is read-only** — which it usually is for an installed
skill — generate into a writable working directory instead, then hand the
result to the user as a downloadable archive for them to install. Say plainly
that this is what you did; a user who thinks a skill was installed when it
wasn't will wonder why nothing works.

The script writes, under the name chosen in Q12:

```
my-skill-creator/
├── SKILL.md              assembled from the answers
├── .skill-config.json    the answers, machine-readable
├── scripts/
│   ├── scaffold_skill.py
│   └── validate_skill.py
└── CHANGELOG.md          only if Q3 = A
```

Then write the lock, if the folder is writable:

```bash
touch <this-skill-folder>/.configured
```

Report what was generated, then stop. Do not offer to create a skill in the
same breath — the user should start that as a fresh request, so the
generated skill gets a clean trigger.

Say one thing more before stopping, because it's the only thing here that is
still adjustable:

> Three of these can be changed later by editing `.skill-config.json` in the
> new skill — the group list, the word cap and the starting version. The rest
> are written into the skill's own instructions, so changing those means
> installing the boilerplate again.

The file itself repeats this under a `_readme` key, for whoever opens it in six
months without this conversation in front of them.

---

## What the generated skill-creator always includes

These hold regardless of the answers, because they are properties of the
format or of basic engineering discipline, not preferences:

- Read the existing skills directory before proposing a name (collision check)
- `description` under the 1024-character hard limit
- Progressive disclosure: keep SKILL.md lean, push detail into `references/`
- Index every new document the day it is created
- No self-describing counts in prose ("12 suites") — they rot silently
- Self-containment: a packaged skill cites nothing outside its own folder
- Unique-match guard when editing files; never blind `sed`
- Battle-tested rule: no rule without a real case that motivated it
- Verify indirect triggering (an informal phrase that doesn't name the skill)
- Count files before packaging, and after
