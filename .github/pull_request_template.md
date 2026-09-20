<!-- PR title = the squash commit. Conventional Commits required - CONTRIBUTING.md#contribute-code. -->

## What


## Why


## How to test


## Checklist

- [ ] References an existing issue (`Closes #N` above; open the issue first when none exists)
- [ ] One logical change
- [ ] PR title follows Conventional Commits, no `!` / breaking marker unless discussed first
- [ ] `ruff check` and `format --check` at the CI-pinned version, `pytest`, `store --check`, `build --check` pass
- [ ] `gh aw compile` run and its outputs committed when a `.github/workflows/*.md` changed
- [ ] Two reviewer sub-agents (code, security) reported nothing left to fix, or the change is prose only
- [ ] No hand edit to `.store/` (except a withdrawal) nor to the generated files
- [ ] Everything committed is in English
