# The eleven questions

What each setup question decides, and what changes in the generated
`skill-creator` depending on your answer. Read this beforehand if you want to
know what you're committing to — or skip it and answer the questions, which are
written to stand on their own.

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

A changelog is a list of what changed in each version. Its value shows up months
later, when you're looking at something odd and want to know whether it was
deliberate.

- **From the first version** — every skill gets one immediately.
- **Once it's worth its own file** — history starts inside the skill and moves
  out when it grows.
- **No** — none kept.

If you keep one, the generated skill-creator uses
[Keep a Changelog](https://keepachangelog.com) and treats past entries as
immutable: a correction is a new entry, never an edit of an old one. Rewriting
history is how a changelog stops being evidence.

---

## Round 2 — Filling in Round 1

Questions here are skipped when Round 1 made them moot: no group names if names
aren't grouped, no starting number if there are no version numbers.

### Q4 · Which group names?

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

A cap on hyphen-separated words. "No limit" is a valid answer.

The reason a cap is offered: when a name needs five words to be clear, it's
usually a sign the skill is doing several jobs and wants to be two skills. That's
a hint, not a law, which is why exceeding it warns rather than blocks.

### Q6 · Starting number

What a brand-new skill gets before anyone has used it. Starting at `1.0.0` says
it counts from the moment it works; starting at `0.1.0` signals it's still
settling and may change under you.

---

## Round 3 — Presentation

### Q7 · Same layout every time?

Whether every skill you write uses the same headings in the same order.

A fixed layout is worth it when you'll open a skill months after writing it: you
know where to look without reading it through, and so does anyone else. No layout
is less ceremony, which matters when most of your skills are short.

The middle answer — a suggested layout you ignore when it doesn't fit — is the
safe default if you're unsure.

### Q8 · Table of facts

A small header table at the top of each skill: area, version, what it produces,
which rules it follows.

Pick only fields you'll actually keep up to date. A stale field reads as current
and misleads, which is worse than having no field at all.

---

## Round 4 — What the tool does for you

### Q9 · Testing that skills load

Skills load on their own, chosen from their descriptions — you don't call them
by name. So the failure mode isn't a crash, it's silence: the wrong skill loads,
or none does, and nothing tells you.

Answering yes adds a procedure for catching that: list the skills that overlap,
write sample requests the way a real person would type them, run them in fresh
conversations, and read which skill actually fired.

Worth having once you have enough skills to compete with each other. Overkill
for four.

### Q10 · Checking before you finish

A script that checks a skill for broken links, missing fields, unfilled
placeholders, and files nothing points to. It reads and reports; it never
modifies anything.

You get the script either way. This decides whether running it is written in as
a required last step, or left to you.

### Q11 · Sub-folders

A skill can carry extra files in three folders: `references/` for documents it
consults, `scripts/` for code it runs, `assets/` for templates and images.

- **Just those three** — nothing else at the top level.
- **Plus your own names** — for splitting up `references/` once it fills.
- **Case by case** — decide each time.

Whatever you choose, splitting happens *inside* `references/`, not by adding new
folders at the top. `references/<area>/` is predictable to anyone who knows the
format; an invented top-level name is not.

---

## And one more — Q12 · Naming the tool itself

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

A configurator you can re-run mid-life produces a split collection: skills built
under the old answers, skills built under the new ones, and nothing recording
which is which. Six months later nobody can tell whether `finance-report`
follows the current convention or a retired one.

Locking the answers keeps one answer to "how are skills named here" for as long
as the install lasts. Changing your mind costs a reinstall — paid once, and
visibly.
