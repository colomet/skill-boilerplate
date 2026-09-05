# The eleven questions

What each setup question decides, and what changes in the generated
`skill-creator` depending on your answer.

Each question appears here word for word as setup asks it, followed by what the
answer changes. So this doubles as somewhere to read all twelve at leisure,
with no prompt waiting on you. A test fails if the wording here and the wording
in the skill ever drift apart.

**You shouldn't need this page to answer the questions.** They're written to
stand on their own, and setup opens by explaining what the whole thing is for.
This page is for anyone who wants the reasoning behind a choice before making
it, or who wants to read the lot through before starting.

## What the questions are actually about

None of them asks what your skills will *do*. They decide the house rules every
skill you write from then on will follow:

| Round | Decides |
|---|---|
| 1 | How skills are named, whether they carry version numbers, whether you keep a changelog |
| 2 | The specifics of whatever Round 1 turned on — which group names, how long a name can get, what number to start at |
| 3 | What a skill looks like inside: a fixed layout or not, a header table of facts or not |
| 4 | What your tool does for you: testing that the right skill loads, checking a skill before you finish it, planning for sub-folders |
| 12th | What to call the tool you end up with |

Every question has an option that turns the thing off, and turning everything
off is a legitimate outcome — you get a plain tool with no conventions, which
suits plenty of people. The cost of a convention is that you have to keep it;
the cost of no convention is that nothing is predictable. Neither is free.

**Setup runs once.** There is no reconfigure command. To change an answer:
delete the generated `skill-creator`, re-download this boilerplate, install it
fresh. See *Why one-shot* at the end.

The questions come in four rounds. They are grouped by what depends on
what, not by topic: a round is answered all at once, so a question can never
rely on another in the same round. That's why "which group names?" comes a round
after "do you want groups at all?".

---

## Round 1 — The three shapes

### Q1 · Grouping in names

```
Q1  Every skill you build will need a name. Names are lowercase with hyphens
    instead of spaces -- `report-builder`, never `Report Builder`. That part
    isn't a choice; the format requires it.

    What you're choosing is whether a name should begin with a word saying
    which area the skill belongs to. That prefix is what keeps forty skills
    findable, and stops two people building the same thing under two names.
    A) No grouping            report-builder
    B) Grouped by area        finance-report-builder
    C) Area and sub-area      finance-monthly-report-builder
    D) I'll describe my own way
```

| Answer | Looks like | Fits when |
|---|---|---|
| No grouping | `report-builder` | A small collection, or one subject area |
| By area | `finance-report-builder` | Several distinct areas, a few skills each |
| Area and sub-area | `finance-monthly-report-builder` | An area broad enough that names start colliding |
| Your own | — | None of the above describes what you already do |

There is no correct answer. What hurts is inconsistency: a collection where half
the names are grouped and half aren't gives you no pattern to check a new name
against, so collisions stop being visible.

### Q2 · Version numbers

```
Q2  Each time you change a skill, do you want it to carry a number that goes
    up? It's how you tell the copy you edited this morning from the one a
    colleague installed last month.
    A) A simple counter       4  ->  5
    B) Two levels             1.4  ->  1.5
    C) Three levels           1.4.0  ->  1.4.1   (the usual choice for software)
    D) Four levels            1.4.0.1
    E) No version numbers     (nothing in the format requires them)
```

| Answer | Looks like |
|---|---|
| Simple counter | `4` |
| Two levels | `1.4` |
| Three levels | `1.4.0` |
| Four levels | `1.4.0.1` |
| None | — |

Three levels is what most software uses: roughly, the first number changes when
something breaks, the second when something is added, the third when something
is fixed.

Nothing in the skill format requires a version at all. "None" is a real answer,
not a lesser one.

### Q3 · Changelog

```
Q3  A changelog is where you write one line every time you change a skill,
    saying what changed. It's how you answer "why is this like this?" months
    later, when the reason has been forgotten.

    You write those lines yourself -- your tool will remind you and give you
    the format, but it can't know what you did.
    A) Yes, from the very first version -- its own CHANGELOG.md file
    B) Start small: a short table at the end of the skill itself, moved out
       to its own file once it outgrows about 30 lines
    C) No changelog
```

Its value shows up months later, when you're looking at something odd and want
to know whether it was deliberate.

- **From the first version** — every skill gets its own `CHANGELOG.md`
  immediately.
- **Start small** — history begins as a short table at the end of the skill
  itself, and moves out to `CHANGELOG.md` once it outgrows about 30 lines. The
  reason for moving it: history is consultation material, and shouldn't cost
  context on every activation.
- **No** — none kept.

You write the entries. The generated tool reminds you and gives you the format,
but it can't know what you changed.

If you keep one, the generated skill-creator uses
[Keep a Changelog](https://keepachangelog.com) and treats past entries as
immutable: a correction is a new entry, never an edit of an old one. Rewriting
history is how a changelog stops being evidence.

---

## Round 2 — Filling in Round 1

Questions here are skipped when Round 1 made them moot: no group names if names
aren't grouped, no starting number if there are no version numbers.

### Q4 · Which group names?

```
Q4  You chose grouped names, so every name will start with a group word --
    the `finance` in `finance-report-builder`. Which groups do you want to
    start with? New names get checked against this list, so a typo becomes
    a caught mistake rather than a stray skill. You can add to it later.
    A) By department          finance, hr, ops, sales, legal, it
    B) By kind of work        research, writing, analysis, review
    C) I'll type my own
    D) None yet, I'll decide as I go
```

Two ready-made starting points, or your own:

- **By department** — `finance`, `hr`, `ops`, `sales`, `legal`, `it`
- **By kind of work** — `research`, `writing`, `analysis`, `review`

This list becomes what new names are checked against. A name outside it produces
a warning, never a block — a convention is a convention, and there are
legitimate exceptions. You can add to the list later by editing
`.skill-config.json`.

"None yet" is fine. The scaffolder then infers the pattern from whatever you've
already built.

### Q5 · How many words in a name?

```
Q5  How long should a skill's name be allowed to get? Counting the words
    between hyphens, group word included. A cap keeps names scannable in a
    list; no cap lets them say more.
    A) At most 2              finance-report
    B) At most 3              finance-monthly-report
    C) At most 4              finance-eu-monthly-report
    D) No limit
```

The reason a cap is offered: when a name needs five words to be clear, it's
usually a sign the skill is doing several jobs and wants to be two skills. That's
a hint, not a law, which is why exceeding it warns rather than blocks.

### Q6 · Starting number

```
Q6  What number does a brand-new skill start at?
    A) Start at one           1.0.0     -- it counts from the moment it works
    B) Start at zero          0.1.0     -- signals "still settling"
    C) Something else
```

What a brand-new skill gets before anyone has used it. Starting at `1.0.0` says
it counts from the moment it works; starting at `0.1.0` signals it's still
settling and may change under you.

---

## Round 3 — Presentation

### Q7 · Same layout every time?

```
Q7  Inside each skill is one file, SKILL.md, holding the instructions. Should
    every skill you write lay that file out the same way -- same headings, same
    order? A fixed layout lets you open something you wrote months ago and find
    the part you need without reading it through. No layout means less ceremony
    on small skills.
    A) Same layout every time
    B) A suggested layout, ignore it when it doesn't fit
    C) No layout, write what each skill needs
```

A fixed layout is worth it when you'll open a skill months after writing it: you
know where to look without reading it through, and so does anyone else. No layout
is less ceremony, which matters when most of your skills are short.

The middle answer — a suggested layout you ignore when it doesn't fit — is the
safe default if you're unsure.

### Q8 · Table of facts

```
Q8  Some people open each skill with a few lines of facts about it, the way a
    form has a header -- so you can see what it is without reading the whole
    thing:

        | Area    | Finance |
        | Version | 1.4.0   |

    Do you want one at the top of every skill, and if so, which facts?
    Pick only what you'll actually keep current: a stale line reads as true
    and misleads, which is worse than no line at all.  (multi-select)
    Area / What it produces / Rules it follows / Related skills /
    Version / History / None -- no table
```

Pick fields that stay true without effort. `Area` is settled the day you name
the skill; `Related skills` needs revisiting every time you write another one,
and is the field most likely to go stale first.

---

## Round 4 — What the tool does for you

### Q9 · Testing that skills load

```
Q9  Skills load on their own, from their description -- you never call one by
    name. Which means sometimes the wrong one loads, or none does, and it isn't
    obvious why. Should your tool include a routine for checking that: write a
    few sample requests, see which skill actually fires, reword the description
    until the right one wins?
    A) Yes -- worth it once you have enough skills to compete with each other
    B) No -- overkill for a handful
```

The failure mode here isn't a crash, it's silence: the wrong skill loads, or
none does, and nothing tells you.

Answering yes adds a procedure for catching that: list the skills that overlap,
write sample requests the way a real person would type them, run them in fresh
conversations, and read which skill actually fired.

Worth having once you have enough skills to compete with each other. Overkill
for four.

### Q10 · Checking before you finish

```
Q10 Before you call a skill finished, a script can check it for broken links,
    missing fields and placeholders you forgot to fill in. You get that script
    either way. This only decides whether your tool treats running it as a
    required last step, or leaves it to you.
    A) Required step
    B) There if I want it
```

The script also catches files nothing points to. It reads and reports; it never
modifies anything.

### Q11 · Sub-folders

```
Q11 Besides its instructions, a skill can carry extra files, in three folders
    the format already names: `references/` for documents it consults,
    `scripts/` for code it runs, `assets/` for templates and images.

    Those three are fixed. The question is what happens when one of them --
    usually `references/` -- gets too full to scan, and you want to split it
    into sub-folders. Agreeing those sub-folder names now means every skill
    splits the same way.
    A) Don't plan for it -- three folders, no sub-folders
    B) Agree the sub-folder names now, and I'll type them
    C) Leave it open -- split however each skill needs at the time
```

- **Don't plan for it** — the three folders, nothing beneath them.
- **Agree the names now** — every skill splits `references/` the same way.
- **Leave it open** — split however each skill needs, when it needs it.

Whatever you choose, splitting happens *inside* `references/`, not by adding new
folders at the top. `references/<area>/` is predictable to anyone who knows the
format; an invented top-level name is not.

---

## And one more — Q12 · Naming the tool itself

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

The thing you're about to get is a skill in its own right, so it needs a name
that follows the same format rules as any other.

It defaults to `my-skill-creator` rather than `skill-creator`, because Anthropic
ships a skill with that exact name. Two folders with one name is a collision;
defaulting away from it means you don't have to know that in advance.

Names containing `claude` or `anthropic` are rejected — the format reserves
those, independently of this particular clash.

**If both end up installed**, different folder names solve only half of it. The
two would still compete for "I want to create a skill", and that failure is
quieter than a name clash: nothing errors, one just gets picked. So the
generated `description` states the boundary outright — automated evaluation with
graded agents and multi-run benchmarking belong to the official tool; naming,
versioning and documentation conventions belong to this one. Complementary, each
covering what the other doesn't.

---

## What the generated tool asks you, every time

Setup decides conventions once. The generated tool asks two things per skill,
and they are deliberately not setup questions — they're about the skill you're
building right now, not about the collection.

**Is this going to repeat?** A skill earns its place when there's a workflow
you'll run again. A one-off task doesn't need one; a good prompt does the job
without leaving anything behind to maintain. The tool says so and offers the
prompt instead — it doesn't refuse, but it doesn't build silently either.

**What are two or three real requests it should handle?** Actual sentences,
the way someone would type them. They define the scope concretely enough to
know when the skill is finished, and they become the raw material for the
`description`, which is the only thing that decides whether the skill ever
loads. A skill built without them tends to describe its subject rather than
its trigger, and then never fires.

Certainty markers — labelling claims as verified, unconfirmed or
interpretation — were a setup question in earlier versions and are not offered
any more. They are content, not container: a convention about what a skill
should say, not about how skills are built. Any skill that needs them can ask
for them when it's written.

## Why one-shot

A setup you can re-run mid-life produces a split collection: skills built
under the old answers, skills built under the new ones, and nothing recording
which is which. Six months later nobody can tell whether `finance-report`
follows the current convention or a retired one.

Locking the answers keeps one answer to "how are skills named here" for as long
as the install lasts. Changing your mind costs a reinstall — paid once, and
visibly.
