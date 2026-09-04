### Naming convention

Plain names, no grouping:

```
{what-it-does}
```

Lowercase, hyphen-separated, no spaces or underscores.

**Read `.skill-config.json` for the current word cap.** It is not repeated here
on purpose: the scripts read that file, so a copy in this text would be free to
drift out of step with it.

- The name should be self-explanatory: what it produces, not how.
- Avoid `helper`, `tool`, `util`, `manager` unless genuinely the best word.
- With no group to separate areas, **collision checking matters more, not less**.
  Read the installed skills before proposing, and if a name sits close to an
  existing one, say so — two skills with similar names compete for the same
  requests, and the wrong one wins silently.

Propose one candidate and confirm it.
