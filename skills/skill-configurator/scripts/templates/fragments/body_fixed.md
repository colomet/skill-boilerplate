### Body structure — required

Every SKILL.md follows this shape. It is a template, not a suggestion: a
consistent shape is what lets someone open an unfamiliar skill and find what
they need without reading it end to end.

```markdown
---
name: {name}
description: {when to use it, with real trigger phrases}
---

# {Readable title}

{One line: what this does and when it comes into play}

## When NOT to use this

## 1. {Main section — the what}

## 2. Process / flow

## 3. Standard output

## 4. Reference cases        (if useful)

## 5. Handoff                (if another skill follows)
```

Two optional sections, added **only when there is a real risk of skipping a
step** — audits, verification, technical verdicts. A skill that fills in a
template omits them entirely; filling them in for completeness produces generic
noise:

- **Rationalizations** — the excuses for cutting a corner, each with a
  counter-argument specific to this skill, not a generic one.
- **Red flags** — signals, mid-execution, that the result is going wrong.
