# The skill format — quick reference

Authoritative spec: <https://agentskills.io/specification>
Anthropic's reference implementation and examples:
<https://github.com/anthropics/skills>

This page summarizes what matters when building one. Where it disagrees with
the spec, the spec wins — check the link.

## The minimum

A skill is a folder containing one file, `SKILL.md`, with YAML frontmatter and
a Markdown body:

```yaml
---
name: my-skill-name
description: What this does and when to use it
---
```

Two required fields:

- **`name`** — unique, lowercase, hyphens instead of spaces.
- **`description`** — what it does *and when to use it*.

Valid at the top level of the frontmatter: `name`, `description`, `license`,
`allowed-tools`, `metadata`, `compatibility`. Anything else — a loose
`version:`, a loose `project:` — fails validation. Put those under `metadata`.

## Why the description carries all the weight

Only the frontmatter is loaded for every skill, every time, so the model can
decide which one is relevant. The body isn't read until the skill actually
fires.

Two consequences:

1. **The description is the entire trigger.** A perfect body behind a vague
   description never runs. Write when-to-use-it phrasings, including the
   informal ones a real person would type.
2. **An oversized SKILL.md costs on every activation**, including the ones where
   the skill turns out to be irrelevant. Detail that isn't needed every time
   belongs in `references/`, which loads on demand. This is what "progressive
   disclosure" means in practice.

The description has a hard limit of 1024 characters. Past it, the text is
truncated silently — and the truncation takes the tail, which is exactly where
trigger phrases tend to accumulate.

## Optional folders

| Folder | Holds |
|---|---|
| `references/` | Documentation loaded on demand |
| `scripts/` | Executable code |
| `assets/` | Templates, images, fonts — used as-is |

None is required. A skill can be a single file.

## Distribution

- As a plain folder, copied where the tool looks for skills.
- As a Claude Code plugin, installed via a marketplace manifest.
- Through the API, for custom skills.

## Trust

A skill can direct an agent to run code and call tools. Use skills only from
sources you trust, and audit unfamiliar ones — `SKILL.md`, scripts, assets, all
of it — before running them.
