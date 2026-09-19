# otelyssey - a self-run marketplace of OpenTelemetry agent plugins

Date: 2026-09-19. Status: approved design, before the implementation plan.

## Purpose

A marketplace of agent plugins whose subject is OpenTelemetry, in the
[Agent Plugins](https://agent-plugins.org/) format (`plugin.json` at
schema 1.0.0), readable by Claude Code and GitHub Copilot CLI first
(both read `.claude-plugin/marketplace.json` at the repository root),
Codex later (`.agents/plugins/marketplace.json`, the same generator).

The existing marketplaces are curated by hand and age. This one is run
by the repository: a contributor submits a plugin **once**, through
an issue; deterministic workflows validate its format and install it;
an agentic workflow judges its relevance and its novelty, talks with
the contributor on the issue, and admits it; a nightly workflow keeps
every admitted plugin at its latest release and refreshes its
repository statistics; every listing artifact is generated from one
store.

## Decisions taken with the maintainer

- **Admission is the agent's.** The agentic workflow admits or rejects
  on its own once the deterministic gates are green; the maintainer
  keeps a right of withdrawal (deleting a store record through a pull
  request removes the plugin).
- **Engine: GitHub Copilot** for every agentic workflow (gh-aw's
  default engine, billed in premium requests, no engine secret to
  hold). One secret exists anyway: the private key of the GitHub App
  that chains the workflows (see the guard rails), because GitHub
  emits no workflow event for what the repository's own `GITHUB_TOKEN`
  does.
- **Scope: OpenTelemetry in the broad sense.** A plugin is admissible
  when its main subject touches OpenTelemetry: instrumentation, the
  Collector, the semantic conventions, or the exploitation of OTel
  telemetry in a backend (Grafana, Datadog, Dynatrace, ...). An
  observability plugin with no OpenTelemetry in it is rejected, with
  the reason.
- **Releases are followed automatically.** The nightly workflow reads
  each admitted plugin's latest tag, replays the format and install
  validation on that tag, and re-pins the marketplace only when it
  passes; a failure opens an issue for the contributor. The
  contributor never re-submits for a new version.
- **Two layers, one owner each.** What the format fixes is
  deterministic Python with no dependency: parsing the submission,
  validating `plugin.json`, installing the plugin on the runner,
  reading statistics, generating the artifacts. What takes a judgment
  is an agentic workflow: relevance, duplicates, the conversation, the
  admission.

## Repository layout

```text
.store/<plugin>.json                 one record per admitted plugin - the only source of truth
.claude-plugin/marketplace.json      generated: the marketplace Claude Code and Copilot CLI read
.agents/plugins/marketplace.json     generated, later: the same for Codex
marketplace/<plugin>/README.md       generated: the plugin's page
README.md                            intro, then the generated table
scripts/                             the deterministic layer, Python 3.11+, standard library only
tests/                               pytest on recorded fixtures
.github/ISSUE_TEMPLATE/submit-plugin.yml
.github/workflows/intake.yml         deterministic gates on the submission issue
.github/workflows/review.md          gh-aw: judgment, conversation, admission
.github/workflows/admit.yml          merges the admission pull request, rebuilds, closes the issue
.github/workflows/nightly.yml        statistics, releases, rebuild
.github/workflows/duplicates.md      gh-aw, weekly audit of the store
.github/workflows/ci.yml             lint and tests of the scripts, schema check of the store
```

### The store record

`.store/<name>.json`, `<name>` the plugin's `plugin.json` name:

| field | content |
| --- | --- |
| `name` | the `plugin.json` name (the Agent Plugins pattern) |
| `description` | one or two sentences, from the submission |
| `category` | one of a short closed list the issue form offers (instrumentation, collector, conventions, backend, workflow) |
| `repository` | `owner/repo`, public GitHub |
| `path` | the plugin's directory inside the repository, empty at the root |
| `ref` | the admitted tag |
| `sha` | the 40-hex commit the tag resolved to when admitted or last followed |
| `version` | `plugin.json`'s version at that sha |
| `author`, `license`, `homepage`, `keywords` | from `plugin.json` at that sha, the submission filling the gaps |
| `submitted_in` | the issue number |
| `admitted_at` | UTC date |
| `stats` | `stars`, `forks`, `watchers`, `refreshed_at` |

The record is written by the pipeline only: the admission pull request
creates it, the nightly workflow updates `ref`, `sha`, `version` and
`stats`. A human edits it only to withdraw a plugin (delete the file).

### Generated artifacts

`scripts/build.py` reads `.store/` and writes, deterministically and
idempotently:

- `.claude-plugin/marketplace.json`: `name: otelyssey`, `owner:
  {"name": "using-system", "url": ...}`, one entry per record with
  `source: {"source": "github", "repo": <repository>, "path": <path>
  when set, "ref": <ref>, "sha": <sha>}` (the one form both hosts
  accept; Copilot CLI rejects a `git-subdir` source, verified
  2026-09-19),
  `description`, `version`, `category`, `keywords`, `license`,
  `author`, `homepage`;
- `marketplace/<name>/README.md`: the plugin's page: description,
  category, repository link, version and tag, author, license,
  keywords, statistics, the install lines for Claude Code and Copilot
  CLI, the issue it was admitted from;
- the README's table, between two markers: plugin (linked to its
  page), description, category, repository, stars, forks, watchers.

A run of `build.py` on a store that did not change produces no diff.

## The submission

`.github/ISSUE_TEMPLATE/submit-plugin.yml`, labels `submission`: plugin
name, description, GitHub repository (`owner/repo`), path inside the
repository (optional), tag to review (required: a release tag, the
immutable form; the sha is derived), version, license, author name and
URL, homepage (optional), keywords, category (dropdown). The template
says what will be checked and that no pull request against `.store/`
is accepted from a contributor.

## Admission

### intake (deterministic, on `issues: opened, edited, reopened` carrying `submission`)

1. `scripts/intake.py` parses the issue body into a candidate record
   and names every missing or malformed field.
2. `scripts/validate.py` resolves the tag to a sha, clones the
   repository at that sha (shallow, no credentials), checks that
   `<path>/plugin.json` exists and validates against the Agent Plugins
   1.0.0 schema (fetched once, cached under `tests/fixtures/`), that
   the `name` matches the submission, that the version matches, and
   that every `skills/<x>/` carries a `SKILL.md`; entries the format
   does not define (`agents/`, `commands/`, `hooks/`, a lock file, a
   `.claude-plugin/` carried next to `plugin.json`) are reported as
   notes, never as errors: real plugins ship them. A `plugin.json`
   missing at the root is an error, named as the legacy layout when
   `.claude-plugin/plugin.json` exists.
3. `scripts/smoke.py` writes a temporary marketplace holding a copy
   of the checked-out plugin (a relative source: no second clone, no
   network in the smoke) and installs the plugin with Copilot CLI (`copilot plugin
   marketplace add`, `copilot plugin install`) and with Claude Code's
   headless plugin install when one exists at that time; the install
   must exit 0 and list the plugin. No plugin code is executed beyond
   the host's install.
4. The workflow comments one result on the issue: each check with pass
   or the exact reason, and sets `format-ok` or `needs-changes`. A
   re-edit re-runs it (concurrency per issue, cancel in progress).
5. On `format-ok` the candidate record is attached to the issue as a
   hidden comment block (`<!-- otelyssey-candidate ... -->`), the input
   of the agentic step, so the agent never re-derives what the gates
   established.

### review (gh-aw, engine copilot, on `format-ok` labelled)

Inputs: the candidate record, the plugin's README and `plugin.json` at
the sha, the store, the open and closed submission issues. The agent:

- rules on **relevance** to OpenTelemetry in the broad sense, from the
  plugin's own description, skills and README, and states the
  evidence;
- rules on **duplication** against the store and the other
  submissions: same repository, same plugin under another name, or a
  plugin whose purpose an admitted one already covers; a near-duplicate
  is a question to the contributor, not a rejection;
- **converses** on the issue through safe outputs (`add-comment`,
  `add-labels` / `remove-labels`, bounded): what is missing, what
  would make the plugin admissible, an answer to the contributor's
  replies (the workflow also triggers on `issue_comment` from the
  submitter while `format-ok` holds);
- **admits** by a safe output `create-pull-request` carrying exactly
  one file, `.store/<name>.json`, with the candidate record plus
  `admitted_at`, and the label `admission`; or **rejects** with
  `rejected` and the reason, closing the issue.

Bounds: `max-ai-credits` per run, one comment and one pull request at
most per run, network limited to GitHub, the contributor's content
treated as untrusted (gh-aw's prompt-injection filtering, no shell
execution of plugin content).

### admit (deterministic, on the `admission` pull request)

`ci.yml` validates the record against the store schema and
`build.py`'s output; on green, `admit.yml` squash-merges the pull
request, runs `build.py`, commits the generated artifacts to `main`,
closes the submission issue with `admitted` and a comment linking the
plugin's page.

## Nightly

`nightly.yml`, once a day:

1. `scripts/stats.py`: for each record, stars, forks and watchers from
   the GitHub API (the workflow's token), `refreshed_at` set.
2. `scripts/releases.py`: for each record, the latest release tag of
   the repository (`git ls-remote --tags`, semver-sorted, the reading
   oddyssey-actions does); when it differs from `ref`, the format
   validation and the install on the hosts are replayed on it (the
   same scripts as intake, `releases.py --smoke`); on pass, `ref`,
   `sha` and `version` are updated; on failure, an
   issue is opened for the contributor (one per plugin and tag, never
   repeated) and the record stays.
3. `build.py`, then one commit by the workflow's bot on `main`,
   `chore(store): nightly refresh`, only when something changed.

`duplicates.md` (gh-aw, weekly): audits the store for plugins that
serve the same purpose and opens one review issue, closing the older
one, as awesome-copilot's detector does; accepted pairs recorded on
past issues are respected.

## Errors and guard rails

- Every deterministic failure names the rule and the value: the
  contributor fixes the issue and the gates re-run.
- Actions pinned by commit SHA with the version in a comment;
  permissions minimal per job; the install smoke runs under an
  isolated HOME with no credential. A GitHub App installed on this
  repository only (Contents, Issues and Pull requests read and write,
  Metadata read) is the pipeline's identity, `otelyssey-bot[bot]`:
  `intake.yml`, `admit.yml` and `nightly.yml` mint a one-hour
  installation token in their first step, the agentic workflows sign
  their safe outputs with it, and it labels the submission issue,
  merges the admission and pushes the bot commits as the `main`
  ruleset's bypass actor, the app `otelyssey-bot` (the maintainer's
  own pushes are refused): an event produced with `GITHUB_TOKEN` starts no
  workflow, so the chain intake → review → admission needs it. Its
  client id is the repository variable `OTELYSSEY_APP_CLIENT_ID`, its
  private key the one secret, `OTELYSSEY_APP_PRIVATE_KEY`, whose value
  is never written anywhere.
- gh-aw workflows are compiled to `.lock.yml` and committed with their
  `.md`; `gh aw compile` in `ci.yml` refuses a drift.
- A plugin's own code is never executed by the pipeline beyond the
  host's install; a `plugin.json` is data, never instructions.

## Tests

- `tests/`: pytest, one module per script, on recorded fixtures (issue
  bodies well-formed and malformed, `plugin.json` samples valid and
  invalid, GitHub API answers, `ls-remote` outputs); `build.py`
  end-to-end on a fixture store, asserting the three artifacts
  byte-for-byte and idempotence.
- The store ships empty. The first record, `oddyssey`
  (`using-system/oddyssey`, the Agent Plugins manifest it ships in
  `marketplace/oddyssey/`), is written by the pipeline itself on the
  first real submission, which is the end-to-end test of the whole
  chain; a fixture copy of it drives the unit tests.
- `ci.yml`: ruff at a pinned version, pytest, `build.py --check`
  (regenerate and diff), gh-aw compile check.

## Out of scope for the first version

Codex's marketplace file (the generator's second output, one flag),
plugins hosted outside GitHub, private repositories, a website, a
rating or a comment system, any signing of plugins.
