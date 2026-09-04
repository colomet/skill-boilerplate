### Naming convention

```
{group}-{what-it-does}
```

Lowercase, hyphen-separated, no spaces or underscores.

**Read `.skill-config.json` for the current group list and word cap.** They are
not repeated here on purpose: the scripts read that file, so a copy in this text
would be free to drift out of step with it — and a name proposed under one rule
while the scaffolder warns under another leaves the user with a contradiction
whose cause is invisible.

- The group identifies the **area**, not the technology or the output format.
- The last part should be self-explanatory in a word or two: what it produces,
  not how.
- Avoid `helper`, `tool`, `util`, `manager` unless genuinely the best word.
- If sibling skills exist in the same group, the name must fit alongside them —
  a family shares a root.

A name outside the group list is a warning, not an error. Say so and let the
user decide; conventions have legitimate exceptions.

Propose one candidate and confirm it. Ask in the open only when the area is
genuinely new, or when two groups are equally defensible.
