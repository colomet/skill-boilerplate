Three optional folders, exactly as the spec defines them. None is required —
a skill can be a single `SKILL.md`.

| Folder | Holds | Loaded |
|---|---|---|
| `references/` | Documentation the skill consults | On demand, when needed |
| `scripts/` | Executable code | When run |
| `assets/` | Templates, images, fonts — used as-is | When used |

No other top-level folder names. If `references/` grows large enough to need
internal structure, subdivide *inside* it rather than adding a fourth folder at
the top: `references/{area}/` is predictable from the outside in a way an
invented name is not.

### Naming sub-folders inside `references/`

Folders are optional. But once one exists, it follows the shape below — a
convention nobody applies is worse than none, because the reader still has to
check both possibilities.

| Sub-folder | Holds |
|---|---|
| `references/examples/` | Worked examples of what this skill produces |
| `references/sources/` | What to consult, where it is, and what it says |

**A `sources/` folder holds citations and your own summaries — not the sources
themselves.** A standard, a manual or a regulation belongs to whoever published
it, carries its own licence, and would bloat the skill besides. What goes in:
which document, which edition, which clause, where to find it, and your own
notes on the part that matters.

Self-containment is about **file paths**, not links. Citing a public URL is
fine; pointing at `../another-folder/doc.md` is not — that path breaks silently
wherever the skill is installed, and the skill still loads without error.
