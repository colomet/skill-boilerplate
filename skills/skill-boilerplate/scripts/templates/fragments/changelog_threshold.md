## Changelog

History starts inside the SKILL.md, in a short table at the end. Once it
outgrows roughly 30 lines, move it out to `CHANGELOG.md` and leave a pointer
behind.

Format once extracted — [Keep a Changelog](https://keepachangelog.com):

```markdown
## [1.1.0] - 2026-03-14

### Added
- What is new

### Changed
- What behaves differently now

### Fixed
- What was wrong and now isn't
```

### The six categories, and how to tell them apart

Categories only help if two people classify the same change the same way. The
test is what the change does to someone who already had the previous version:

| Category | Use it when | Not to be confused with |
|---|---|---|
| `Added` | Something exists now that did not exist before | `Changed` — nothing was replaced |
| `Changed` | Existing behaviour or content works differently now | `Fixed` — it was not wrong before, just different |
| `Deprecated` | Still works, but is on its way out | `Removed` — it is still there today |
| `Removed` | It is gone. Anything relying on it breaks | `Deprecated` — that is the warning, this is the event |
| `Fixed` | It was wrong and now it is right | `Changed` — this implies the old one was defective |
| `Security` | A vulnerability was closed | `Fixed` — separate, so it can be found fast |

Two rules that keep this usable:

- **One category per entry.** A change that seems to be two is usually two
  changes; write it as two lines.
- **Write for whoever uses the skill, not for whoever edited the file.** "Now
  handles multi-page PDFs" is useful; "refactored the parser" is not.

- One entry per released version, newest at the top.
- Write what changed for whoever *uses* the skill, not what you did to the file.
- **History is immutable.** Past entries are never rewritten. A correction is a
  new entry.
- The reason for moving it out: history is consultation material and shouldn't
  pay a context toll on every activation.
