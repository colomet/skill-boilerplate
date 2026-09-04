# Contributing

Thanks for your interest in this project.

## Before you start

Open an issue first for anything larger than a typo. This boilerplate takes a
deliberate position — it asks questions rather than baking in conventions — and
a change that quietly adds a convention is a change to that position, not a
feature. Worth agreeing on before the work is done.

## Workflow

1. **Fork** the repository.
2. **Create a branch** for your change:
   `git checkout -b fix/short-description`
3. **Make the change.**
4. **Run the tests** from the repository root:
   `python3 tests/test_boilerplate.py`
   Standard library only, no dependencies to install. Python 3.8 or newer.
5. **Add a test** for anything you changed in `skills/skill-boilerplate/scripts/`.
   A convention the generator claims to apply but nothing re-checks is a
   convention that will drift.
6. **Update `CHANGELOG.md`** under `[Unreleased]`.
7. **Open a pull request** using the template.

## What goes where

| Path                                   | Holds                                            |
| :------------------------------------- | :----------------------------------------------- |
| `skills/skill-boilerplate/`            | The installable skill. Nothing repository-level. |
| `skills/skill-boilerplate/scripts/`    | The generator and the scripts it emits.          |
| `template/`                             | The bare skill skeleton, for people who skip the wizard. |
| `docs/`                                 | Prose for humans reading the repository.         |
| `tests/`                                | The whole test suite, in one file.               |
| `scripts/`                              | Repository tooling. Not part of any skill.       |

Two rules the layout depends on:

- Repository files never go inside a skill folder.
- A skill folder holds nothing that isn't part of the skill — in particular,
  **no `README.md`**. Everything a reader needs belongs in `SKILL.md` or
  `references/`.

## Style

Commit messages: imperative mood, one line, no trailing period
(`fix relative path in scaffold script`).

Documentation is in English throughout, including issue and pull request
templates.

## Reporting a security problem

Don't open a public issue. Use GitHub's private vulnerability reporting on this
repository instead.
