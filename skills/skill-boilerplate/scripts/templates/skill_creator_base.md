---
name: skill-creator
{{METADATA}}description: "Creates and maintains Claude Skills end to end: naming, writing the SKILL.md body, and packaging, enforcing this user's own naming, versioning and documentation conventions. Use whenever a new skill is needed, even if the word 'skill' isn't used: 'I want a skill for X', 'make Claude able to do Y', 'how should I name this', 'help me define this'. Also to continue one in progress: 'write the body', 'create the SKILL.md', 'what's the next step'. Do NOT use for automated evaluation with graded agents or multi-run benchmarking -- that is Anthropic's official skill-creator, which this tool complements rather than replaces."
---

# Skill Creator

Creates a skill from idea to finished folder, following the conventions set up
when this skill was generated. Those conventions live in `.skill-config.json`
next to this file — read it if you need the raw values.

## When NOT to use this

- **To read or fix a non-skill Markdown file.** This is about skills only.
- **To change the conventions themselves.** They were locked at setup time.
  Changing them means re-installing the boilerplate from scratch.

---

## Step 0 — Should this be a skill at all?

Two questions before anything else, and they come first because building the
wrong artefact well is still building the wrong artefact.

**1. Is this going to repeat?**

A skill earns its place when there's a workflow you'll run again — the same
kind of task, more than once, where re-explaining your preferences every time
is the actual cost. A one-off task doesn't need one: a good prompt does the job
without leaving anything behind to maintain.

If the answer is no, say so plainly and offer the prompt instead. Don't refuse
— the user may have a reason — but don't build it silently either. Fifteen
skills where three would do is a collection nobody can navigate, and each one
still costs context on every single request.

**2. What are two or three real requests this should handle?**

Actual sentences, the way someone would type them. Not "handle reports" but
"turn last month's numbers into the board summary".

These do double duty: they define the scope concretely enough to know when the
skill is finished, and they become the raw material for the `description` in
Step 1 — which is the only thing that decides whether the skill ever loads. A
skill built without them tends to end up describing its subject rather than its
trigger, and then never fires.

If the user can't produce two, that's information: the need may not be shaped
clearly enough to build for yet.

## Step 0b — What you already have

Work out from context what you already know, and ask only what you genuinely
can't infer. At most three questions, one round.

- Does the user already have a name? → skip the naming step
- Do they have a partial draft? → go straight to reviewing it
- Only an idea? → start from the beginning

---

## Step 1 — Naming

**Two reads before proposing anything.** Neither is step one of a list; they are
the conditions for naming to be possible at all.

```bash
ls {the directory where skills are installed}
cat .skill-config.json
```

The directory tells you what already exists: which groups are in use, which name
patterns repeat, and whether a sibling skill already covers this ground. If one
does, say so before proposing — the fix may be to extend that skill rather than
add a new one.

`.skill-config.json` holds the current conventions: the group list, the word
cap, the starting version. **Read them from there every time, never from
memory.** They can be edited between sessions, and the scripts obey the file —
a name proposed from a remembered list while the scaffolder checks the real one
produces a contradiction the user cannot trace.

{{NAMING}}

### The description field

This is the only thing that decides whether the skill ever loads. The body is
not read until after that decision is made. Write it accordingly:

- Say **when to use it**, not how it works
- Include the informal phrasings a real user would type, not just the formal one
- Include a "do NOT use this for..." clause if a neighbouring skill overlaps
- **Hard limit: 1024 characters.** Past that it is truncated silently, and the
  truncation eats the tail — which is where the trigger phrases accumulate.
  Aim for 1000 or under, and count.

---

## Step 2 — Writing the body

{{BODY_STRUCTURE}}

{{IDENTIFICATION}}

### Rules that hold regardless

- **Write facts as facts, not as sentences about facts.** Prose costs context
  and buries the thing it carries. Anything that is a value, a setting, a limit
  or a name goes as `Label: value`.

  > This project was set up with scalability in mind, using Node.

  becomes

  > Runtime: Node.js v20

  The test is subtraction: cross out a sentence and ask whether the model would
  do anything differently. If not, it was decoration. Prefer the imperative over
  explanation, an example over a description, and one rule with the case that
  motivated it over three stated in general.

  **The exception is judgement.** Reasons stay when they let the model resolve a
  case you didn't foresee — "guard for uniqueness *because a blind replace hits
  the wrong line silently*" earns its words; "this is important" doesn't. Cut
  the padding around the reason, not the reason.
- **Keep SKILL.md lean.** Only the frontmatter is loaded on every activation;
  the body is loaded when the skill fires. Detail that isn't needed every time
  belongs in `references/`. Once the body gets long, pruning is the condition
  for adding, not a later chore.

  This is a separate rule from the one above, and neither substitutes for the
  other: moving text to `references/` divides it, writing densely reduces it. A
  body split across four files is still long when the skill fires.
- **Reference by name, never by section number.** "(see Packaging)" survives a
  reordering; "(§4.2)" does not.
- **Self-containment.** Everything the skill cites lives inside its own folder.
  A packaged skill contains only its own directory: any path pointing outside
  breaks silently at the destination, and the skill still loads without error.
  If two skills need the same material, duplicate it.
- **Battle-tested.** Don't add a rule without a real case that motivated it. A
  rule with no case behind it is noise: it costs context and prevents nothing
  demonstrable.
- **Index every document the day you create it.** A file nobody links to exists
  but cannot be found.
- **No self-describing counts in prose.** "12 checks", "4 pages" — these go
  stale without anyone noticing, because nobody remembers they're there. If the
  number matters, let a script count it.
- **Editing files: guard for uniqueness.** Use an exact-match replace, or Python
  with an explicit `assert count == 1`. Never blind `sed`, never append without
  checking. In text editing, silent failure is the normal failure mode.


---

## Step 3 — Folders

{{FOLDERS}}

### When something becomes its own file

- One file, one subject. If a file covers two, split it.
- Content the body needs *every single time* stays in SKILL.md. Content needed
  only in some runs goes to `references/`.
- Logic that is more reliable as deterministic code than as prose goes to
  `scripts/`.
- Files used as-is, never read as instructions (templates, images, fonts), go
  to `assets/`.

Use `scripts/scaffold_skill.py` to generate the folder once the shape is decided:

```bash
python3 scripts/scaffold_skill.py {skill-name} --references --scripts
```

It creates only the folders you ask for. An empty folder is a promise nobody
keeps.

---

{{VERSIONING}}

{{CHANGELOG}}

{{EVALUATION}}

{{PACKAGING}}

## Standard output

When the skill is done, report:

```
NAME:        {name}          (pattern detected: {pattern}, siblings: {list|none})
DESCRIPTION: {n} characters  (limit 1024)
STRUCTURE:   {tree}
{{OUTPUT_VERSION_LINE}}
NEXT:        {what remains, or "ready to use"}
```
