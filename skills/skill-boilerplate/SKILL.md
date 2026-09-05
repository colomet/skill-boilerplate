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

## Step 1 — Say what the questions are for, then ask them

### First, this. Before any option appears.

Most people will never open the documentation, and shouldn't have to. Show
them this — in their own language, keeping the shape and every specific — and
wait for them to be ready before Q1:

> You're about to set up your own skill-building tool. Twelve questions, two
> minutes or so.
>
> **None of them asks what your skills will do.** They decide the house rules
> every skill you write from now on will follow: how they're named, whether
> they carry version numbers, what each one looks like inside, and what gets
> checked before you call one finished.
>
> At the end you get a new skill of your own. From then on you ask *that* one
> to build things, and it applies these rules every time without asking again.
>
> Two things worth knowing before you start:
>
> - **Every question has a "no" option, and "no" is a real answer.** Answering
>   no to everything gives you a plain tool with no house rules, which is the
>   right outcome for plenty of people.
> - **This runs once.** Afterwards it locks itself. Changing your mind means
>   installing this again from scratch and answering again — so it's worth
>   reading the options rather than taking the first.
>
> Ready?

If they ask why it can only run once, answer in a sentence — a tool you can
re-run halfway through produces a collection split between old rules and new
ones, and nothing to say which skill follows which — and offer
`docs/configuration.md` for the longer version. Don't volunteer the link
otherwise.

### Then the questions

Four rounds, using `ask_user_input_v0`. Ask **all eleven**, in order,
even where an answer seems inferable. This is the one moment where thorough
beats quick: every unasked question becomes a guess baked into every skill the
user ever generates.

**Write for someone who has never built a skill.** No jargon in the questions
themselves — say what a thing is, and what choosing it would change, before
asking about it. Every option shows a concrete example rather than naming a
category. If a question can't be understood without opening the docs, it is
written wrong.

**The rounds are grouped by dependency, not by topic.** Three questions in one
round are answered simultaneously, so a question can never depend on another in
the same round. Round 2 exists because its questions need Round 1's answers.

### Round 1 — The three shapes

```
Q1  Every skill you build needs a name. Names are lowercase with hyphens
    instead of spaces -- `report-builder`, never `Report Builder`. That part
    isn't a choice; the format requires it.

    What you're choosing is whether a name should begin with a word saying
    which area the skill belongs to. That prefix is what keeps forty skills
    findable, and stops two people building the same thing under two names.
    A) Grouped by area        finance-report-builder
    B) Area and sub-area      finance-monthly-report-builder
    C) I'll describe my own way
    D) No grouping            report-builder

Q2  Each time you change a skill, do you want it to carry a number that goes
    up? It's how you tell the copy you edited this morning from the one a
    colleague installed last month.
    A) A simple counter       4  ->  5
    B) Two levels             1.4  ->  1.5
    C) Three levels           1.4.0  ->  1.4.1    (the usual one for software)
    D) Four levels            1.4.0.1  ->  1.4.0.2

    E) No numbers at all -- nothing in the format requires them

Q3  When you change a skill, you can keep a running list: one line per change,
    dated, saying what you did. Months later that list is the only way to
    answer "why is this like this?", once the reason has left your memory.

    The usual name for such a list is a changelog. You write the lines
    yourself -- your tool reminds you and gives you the shape, but it can't
    know what you changed.
    A) Yes, from day one -- each skill keeps its own CHANGELOG.md file
    B) Start small -- a few lines at the end of the skill itself, moved out
       to their own file once they pass about 30 lines
    C) No list
```

### Round 2 — Filling in Round 1

Skip any question whose answer Round 1 already settled: Q4 if names aren't
grouped, Q6 if there are no version numbers.

```
Q4  You chose grouped names, so every name will start with a group word --
    the `finance` in `finance-report-builder`. Which groups do you want to
    start with? New names get checked against this list, so a typo becomes
    a caught mistake rather than a stray skill. You can add to it later.
    A) By department          finance, hr, ops, sales, legal, it
    B) By kind of work        research, writing, analysis, review
    C) I'll type my own
    D) None yet, I'll decide as I go

Q5  How long should a skill's name be allowed to get? Counting the words
    between hyphens, group word included. A cap keeps names scannable in a
    list; no cap lets them say more.
    A) At most 2              finance-report
    B) At most 3              finance-monthly-report
    C) At most 4              finance-eu-monthly-report
    D) No limit

Q6  You asked for version numbers. What should a brand-new skill's version
    be, before anyone has used it? (Shown three-level here; it will match
    whichever shape you picked.)
    A) Start at one           1.0.0     -- it counts from the moment it works
    B) Start at zero          0.1.0     -- signals "still settling"
    C) Something else
```

### Round 3 — What a skill looks like inside

```
Q7  A skill's instructions live in a single file, SKILL.md. Inside it you
    write sections with headings -- what this is for, when to use it, how to
    do it, what to watch out for.

    Should every skill you write use the same headings, in the same order?
    (This is about the sections inside that one file. Folders are Q9.)
    A) Same headings every time
    B) A suggested set, ignore it when it doesn't fit
    C) No fixed set -- write whatever sections each skill needs

Q8  At the very top of a skill, before the instructions start, you can put a
    few labelled facts about it -- the way a jar has a label, or a form has a
    box on the first page. It tells you what you are holding without reading
    the thing:

        | Area    | Finance |
        | Version | 1.4.0   |

    Do you want that label on every skill, and if so, which lines go in it?
    Pick only what stays true on its own: `Area` is settled the day you name
    the skill, while `Related skills` needs revisiting every time you write
    another one, and is the first line to go stale.  (multi-select)
    Area / What it produces / Rules it follows / Related skills /
    Version / History / None -- no label

Q9  Besides its instructions, a skill can carry extra files, in three folders
    the format already names: `references/` for documents it consults,
    `scripts/` for code it runs, `assets/` for templates and images.

    Those three are fixed -- you are not choosing them. The question is what
    happens when one of them, usually `references/`, gets too full to scan
    and you want to divide it into sub-folders. Agreeing those sub-folder
    names now means every skill divides the same way.
    A) Don't plan for it -- the three folders, nothing inside them
    B) Agree the sub-folder names now, and I'll type them
    C) Leave it open -- divide however each skill needs at the time
```

### Round 4 — What your tool does for you

```
Q10 Skills load on their own, from their description -- you never call one by
    name. Which means sometimes the wrong one loads, or none does, and it
    isn't obvious why. Should your tool include a routine for checking that:
    write a few sample requests, see which skill actually fires, reword the
    description until the right one wins?
    A) Yes -- worth it once you have enough skills to compete with each other
    B) No -- overkill for a handful

Q11 Before you call a skill finished, a script can check it for broken links,
    missing fields and placeholders you forgot to fill in. You get that
    script either way. This only decides whether your tool treats running it
    as a required last step, or leaves it to you.
    A) Required step
    B) There if I want it
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
| Q9 | `scope.folders` — `spec_only` / `custom_vocab` / `per_skill`, plus `scope.vocabulary` |
| Q10 | `scope.evaluation` — boolean |
| Q11 | `scope.packaging_gate` — boolean |
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
