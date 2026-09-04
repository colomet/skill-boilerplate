# What this is, and what it isn't

If you only read one page before installing, read this one.

## Two different things share a name

The repository and the skill are not the same object, and most of the confusion
around this project comes from treating them as one.

**The skill** is the product. One folder, `skills/skill-boilerplate/`, holding a
`SKILL.md` and the scripts it runs. That folder is what gets installed, and it
works on its own with nothing else from here.

**The repository** is the workshop the skill is built in. Tests that prove it
still works, a packaging script, plugin manifests, documentation, a bare
template for people who want none of it. None of that is needed to *run* the
skill. All of it is needed to *maintain* it.

| Folder | Who it's for | Needed to run the skill? |
| :--- | :--- | :--- |
| `skills/skill-boilerplate/` | anyone using it | **Yes — this is the skill** |
| `template/` | someone skipping the wizard | No |
| `tests/` | someone changing the code | No |
| `scripts/` | someone building the archive | No |
| `.claude-plugin/` | Claude Code, at install time | No |
| `.github/` | GitHub — issues, reviews, CI | No |
| `docs/` | someone deciding whether to install | No |

Delete everything but the skill folder and it still runs. What you lose is the
ability to check that it still works, to hand it to anyone else, and to change
it without guessing.

## Installing doesn't always bring the same files

Three ways in, and they don't copy the same thing. Worth knowing before you
wonder why your disk has test files on it.

| Method | What lands on your machine |
| :--- | :--- |
| Upload the zip to claude.ai | The skill folder only |
| `cp -r skills/skill-boilerplate ~/.claude/skills/` | The skill folder only |
| Install as a Claude Code plugin | **The whole repository** |

The plugin route clones everything because that's how it stays updatable with
one command. The extra folders sit there unread — Claude only looks inside
`skills/`. It costs a few hundred kilobytes and buys you `/plugin update`.

## Two tools, one after the other

```
skill-boilerplate      you install this, and run it once
        ↓
my-skill-creator       it writes this, shaped by your answers
        ↓
your skills            this is what you actually make, from then on
```

The boilerplate does not make skills. It makes the thing that makes skills, then
locks itself and gets out of the way. If you find yourself asking the
boilerplate to build a skill for you, you're one step too far back.

The middle tool is yours. It has your naming rules, your version scheme, your
document layout written into it. Nobody else's copy looks like it.

## What it's for

**You're about to write more than one skill.** The point of answering twelve
questions is that you stop answering them. The second skill and the twentieth
come out shaped the same way without you re-deciding anything.

**You want your own conventions, not someone else's.** Most templates ship with
a naming scheme and a version format already chosen. Reasonable for whoever
wrote them, arbitrary for you. This one asks.

**More than one person will write skills for the same collection.** The
generated tool is a file you can commit and share. Everyone using it produces
skills that match, which is a cheaper way to enforce a convention than review.

**You want the rules checked, not just written down.** The generated
`validate_skill.py` re-reads your conventions and reports where a skill breaks
them. A convention nobody can re-run tomorrow is a convention that drifts.

Concretely, the kind of thing people set this up for:

- A team collection where every skill needs the same header table and version
  format, because they end up in an audit trail
- A personal collection grouped by area, where names carry a prefix and you'd
  rather not remember which prefixes exist
- A repository of skills published for others, where a packaging check before
  release matters more than convenience

## What it isn't for

**It won't write a skill for you.** Neither tool invents content. They ask what
the skill should do and shape what you tell them. If you don't know what the
skill is for, no generator fixes that.

**It isn't a skill marketplace or a registry.** Nothing here discovers, ranks or
distributes other people's skills.

**It isn't a runtime.** Nothing here loads, executes or hosts a skill. That's
Claude's job. These are files that produce files.

**It isn't a replacement for the format spec.** The rules the format itself
imposes — the frontmatter fields, the description limit, the three optional
folders — come from the [specification](https://agentskills.io/specification),
not from here. A summary is in [spec.md](spec.md).

**It isn't worth it for a single skill.** If you're writing one skill and won't
write another, copy `template/`, fill it in, and skip all of this. That path is
supported on purpose.

**It isn't reconfigurable.** Setup runs once per install. Changing your mind
means starting over, deliberately —
[why](configuration.md#why-one-shot).

## Who ends up not wanting it

Worth saying plainly, since a tool that admits its limits is easier to trust.

- You already have a skill-creating setup you're happy with. There's nothing
  here that upgrades it.
- You want Anthropic's defaults rather than your own. Their `skill-creator` is
  bundled already and needs no setup.
- You need something that adapts as you go. This freezes your answers on
  purpose; that's a feature only if you want it.

## Where to go next

- [walkthrough.md](walkthrough.md) — the whole path, install to finished skill
- [configuration.md](configuration.md) — what each of the twelve questions
  decides
- [maintaining.md](maintaining.md) — updating, extending, and making it yours
-   [spec.md](spec.md) — the skill format itself, in one page
