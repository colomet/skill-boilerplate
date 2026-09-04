## Versioning

Scheme: **{{DIGITS}}**, starting at `{{INITIAL_VERSION}}`.

The version lives in the frontmatter under `metadata`:

```yaml
metadata:
  version: {{INITIAL_VERSION}}
```

Only `name`, `description`, `license`, `allowed-tools`, `metadata` and
`compatibility` are valid at the top level of the frontmatter. A loose
`version:` key fails validation — it must be nested under `metadata`.

**Hold the initial version through the whole build.** A skill under
construction doesn't get a new number for every intermediate edit; it advances
when it's finished and goes into use.

**Once delivered, a number is spent.** If the content changes, the version
changes too — the same number never describes two different files. That rule is
what makes a version worth reading at all.
