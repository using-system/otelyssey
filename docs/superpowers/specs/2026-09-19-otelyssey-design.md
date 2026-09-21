# otelyssey - a self-run marketplace of OpenTelemetry agent plugins

Date: 2026-09-19. Status: approved design, before the implementation plan.

## Purpose

A marketplace of agent plugins whose subject is OpenTelemetry, in the
[Agent Plugins](https://agent-plugins.org/) format (`plugin.json` at
schema 1.0.0), readable by Claude Code and GitHub Copilot CLI today
(Copilot CLI looks for `marketplace.json` at the repository root first,
Claude Code and VS Code read `.claude-plugin/marketplace.json`: the
generator writes the same content at both places), Codex CLI
(`.agents/plugins/marketplace.json`, the same generator, with the
git-backed sources Codex accepts), Grok Build
(`.grok-plugin/marketplace.json`, Codex's content again: it reads that
place only, verified on 1.0.34), APM (`apm marketplace add`, the
Claude Code schema, an Agent Plugins package for its `copilot` target),
Kiro (a plugin at its repository's root, imported by url), Hermes Agent
(`hermes plugins install owner/repo[/path] --ref <sha>`; `--ref` and
the pack command are in Hermes's releases since v2026.8.13 (0.20.1),
not in the PyPI package, still 0.19.0; the `owner/repo/path` shorthand
is in both), OpenClaw (a clone at the commit, its directory installed
with `openclaw plugins install ./<dir>[/<path>] --force
--accept-capabilities`: the `git:` route wants a native OpenClaw
package, "missing package.json" on an Agent Plugins bundle, and its
marketplace route installs the root of a `url` entry, the `path`
dropped; verified 2026-09-21 on 2026.9.5) and Mistral Vibe (a
directory under `~/.vibe/plugins/`, copied from a clone at the commit)
through the install lines on each plugin's page.

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
- **Scope: OpenTelemetry, directly or through a backend that ingests
  it.** A plugin is admissible when its main subject is instrumentation,
  the Collector, the semantic conventions, or the operation of an
  observability backend that ingests OpenTelemetry telemetry, over OTLP
  or through a Collector exporter. A backend plugin need not name
  OpenTelemetry: the backend's compatibility, from the plugin's text or
  the vendor registry at opentelemetry.io, is the criterion, and the
  rule names no vendor. A plugin whose subject is neither is rejected,
  with the reason.
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
marketplace.json                     generated: the marketplace Copilot CLI reads first
.claude-plugin/marketplace.json      generated: the same content, the one Claude Code reads
.agents/plugins/marketplace.json     generated: Codex's catalog, url and git-subdir sources at the sha
.grok-plugin/marketplace.json        generated: the same content, the one Grok Build reads
hermes-pack.yaml                     generated: Hermes Agent's pack, every plugin pinned at its sha
marketplace/<plugin>/README.md       generated: the plugin's page
README.md                            intro, then the generated plugin list
scripts/                             the deterministic layer, Python 3.11+, standard library only
tests/                               pytest on recorded fixtures
.github/ISSUE_TEMPLATE/submit-plugin.yml
.github/workflows/intake.yml         deterministic gates on the submission issue
.github/workflows/review.md          gh-aw: judgment, conversation, the ruling
.github/workflows/admission.yml      writes the record, opens and merges the admission pull request, rebuilds, closes the issue
.github/workflows/nightly.yml        statistics, releases, rebuild
.github/workflows/duplicates.md      gh-aw, weekly audit of the store
.github/workflows/ci.yml             lint and tests of the scripts, schema check of the store
```

### The store record

`.store/<name>.json`, `<name>` the plugin's `plugin.json` name:

| field | content |
| --- | --- |
| `name` | the `plugin.json` name (the Agent Plugins pattern) |
| `description` | `plugin.json`'s, else the repository's description; neither is a `needs-changes` |
| `categories` | a non-empty ordered list of distinct values among instrumentation, collector, backend, observability, the principal first, ruled by the review from the plugin's content (every category a named skill justifies) |
| `repository` | `owner/repo`, public GitHub |
| `path` | the plugin's directory inside the repository, empty at the root |
| `ref` | the admitted tag |
| `sha` | the 40-hex commit the tag resolved to when admitted or last followed |
| `version` | `plugin.json`'s version at that sha |
| `author`, `license`, `homepage`, `keywords` | from `plugin.json` at that sha, the repository's metadata filling the gaps (its owner, its license, its homepage, its topics); a license from neither is a `needs-changes`, an author from neither too; keywords may be empty |
| `submitted_in` | the issue number |
| `admitted_at` | UTC date |
| `stats` | `stars`, `forks`, `watchers`, `refreshed_at` |

The record is written by the pipeline only: the admission pull request
creates it, the nightly workflow updates `ref`, `sha`, `version`, the
fields derived from the manifest, and `stats`. A human edits it only
to withdraw a plugin (delete the file).

### Generated artifacts

`scripts/build.py` reads `.store/` and writes, deterministically and
idempotently:

- `.agents/plugins/marketplace.json`, Codex's catalog: one entry per
  record with `source: {"source": "url" | "git-subdir", "url":
  https://github.com/<repository>.git, "path": ./<path> when set,
  "ref", "sha"}`, the default policy, the principal category's title, and
  `description`, `version`, `keywords`, `author`, `homepage` as the
  manifest fields Codex lists before the install;
- `.grok-plugin/marketplace.json`, the same content: Grok Build reads
  that place only, and only the `url` and `git-subdir` sources (a copy
  of the Claude Code manifest lists nothing, verified on 1.0.34);
- `hermes-pack.yaml`, Hermes Agent's plugin pack (`hermes plugins pack
  install <url>` installs every entry after a review screen): one entry
  per record with `repo: <repository>`, `subdir: "<path>"` when set
  (double-quoted: the store's path rule is loose, a JSON string is a
  YAML one),
  `ref: "<sha>"` (a tag or a branch is refused; quoted, a sha of decimal
  digits reading as an int); not written for an empty
  store, which Hermes refuses;
- `marketplace.json` and `.claude-plugin/marketplace.json`, the same
  content: `name: otelyssey`, `owner: {"name": "using-system", "url":
  ...}`, one entry per record with
  `source: {"source": "url", "url": https://github.com/<repository>.git,
  "path": <path> when set, "ref": <ref>, "sha": <sha>}` (the one form
  Claude Code, Copilot CLI and APM all accept and clone over https,
  checking out the sha; a `github` source Claude Code clones over ssh,
  which fails without a GitHub key; Copilot CLI rejects a `git-subdir`
  source, Claude Code a `git` one; verified 2026-09-21 under an
  isolated HOME without a key, on Claude Code 2.1.278, Copilot CLI
  1.0.86 and APM 0.31.0: a wrong sha fails on both CLIs, a wrong ref
  with the right sha installs on Claude Code and fails on Copilot,
  which fetches the ref too). The smoke keeps a local source and never
  clones: the url form is proven by that hand check of 2026-09-21, not
  by the pipeline,
  `description`, `version`, `category` (the principal), `keywords`, `license`,
  `author`, `homepage`;
- `marketplace/<name>/README.md`: the plugin's page: description,
  repository link, categories, version and tag, author, license,
  keywords, statistics, the install lines for Claude Code, Copilot
  CLI, Codex CLI, Grok Build, APM, VS Code, Hermes Agent, OpenClaw,
  Mistral Vibe and, for a plugin at its repository's root, Kiro;
- the README's plugin list, between two markers: one subsection per
  principal category holding plugins, one entry per plugin (the plugin
  linked to its page, the author, the description, its other
  categories) and a line of live shields.io badges below it, anchored
  at `#` (GitHub links a bare image to itself, and drops an anchor
  without href): version, created, last commit, license, stars, forks,
  watchers. The counts the store carries refresh the plugin's page, not
  the README, which changes only when a record does.

A run of `build.py` on a store that did not change produces no diff.

## The submission

`.github/ISSUE_TEMPLATE/submit-plugin.yml`, labels `submission`: one
field, the URL of the plugin's `plugin.json` on GitHub
(`https://github.com/<owner>/<repo>/blob/<ref>/<path>/plugin.json`, or
the `raw.githubusercontent.com` form). It gives the repository and the
path, nothing else: nothing typed into the form enters the store, the
pages or the catalogs, only the manifest and the repository's metadata,
validated. The URL's ref is ignored: the ref reviewed is
the repository's latest release (`X.Y.Z` or `vX.Y.Z`, the highest by
semver) carrying the plugin, else its default branch, resolved by the
intake, and the sha is derived from it; every other field is read from
`plugin.json` at that sha, the repository's metadata filling the gaps.
The categories are the review's. A branch whose name carries a slash
cannot be told from the path: the ref is one segment (or GitHub's
`refs/heads/<branch>` and `refs/tags/<tag>`), and a wrong split is a
`needs-changes` naming the missing directory.

## Admission

### intake (deterministic, on `issues: opened, edited, reopened` carrying `submission`)

1. `scripts/intake.py` parses the issue body's one field, the manifest
   URL, into the repository and the path, and names a malformed URL;
   on a clean one it resolves the repository's latest release tag
   (`git ls-remote --tags`, semver-sorted) carrying the plugin, else
   its default branch, and its sha into the candidate, and names an
   unreadable repository as an error.
2. `scripts/validate.py` resolves the ref to a sha, clones the
   repository at that sha (shallow, no credentials), checks that
   `<path>/plugin.json` exists and validates against the Agent Plugins
   1.0.0 schema (fetched once, cached under `tests/fixtures/`), and
   that it carries a `name` and a `version` (the record's, read from
   `plugin.json`). A `skills/<x>/`
   without `SKILL.md` (not a skill; a client skips it, #63) and the
   directories the format does not define (`agents/`, `commands/`,
   `hooks/`, a `.claude-plugin/` carried next to `plugin.json`) are
   reported as notes, never as errors: real plugins ship them; a plain
   file next to `plugin.json` is never noted (a plugin at its
   repository's root sits next to all of the repository's files, #31).
   A `plugin.json`
   missing at the root is an error, named as the legacy layout when
   `.claude-plugin/plugin.json` exists.
3. `scripts/derive.py` builds the record: the manifest first
   (`name`, `version`, `description`, `license`, `homepage`, `author`,
   `keywords`), the repository's GitHub metadata next (its description,
   `license.spdx_id`, homepage, owner as the author, topics as the
   keywords), through the REST API with the app's token; a description,
   a license or an author from neither is an error the contributor
   fixes in `plugin.json`, a `needs-changes`. The comment says which
   fields the repository filled. `scripts/resync.py`, run by hand
   once (2026-09-20), read the derived fields of the records admitted
   from the old form again from their manifests, the same way.
4. `scripts/smoke.py` writes a temporary marketplace holding a copy
   of the checked-out plugin (a relative source: no second clone, no
   network in the smoke) and installs the plugin with Copilot CLI (`copilot plugin
   marketplace add`, `copilot plugin install`), with Claude Code's
   headless plugin install, with Codex CLI (`codex plugin
   marketplace add`, `codex plugin add`, reading the marketplace's
   `.agents/plugins/marketplace.json` with a local source) and with
   Grok Build (`grok plugin marketplace add`, `grok plugin install
   <name> --trust`, reading `.grok-plugin/marketplace.json` with a
   local source), each under an isolated HOME (and CODEX_HOME); the
   install must exit 0 and list the plugin. No plugin code is executed
   beyond the host's install.
5. The workflow comments one result on the issue: each check with pass
   or the exact reason, and sets `format-ok` or `needs-changes`. A
   re-edit re-runs it (concurrency per issue, cancel in progress).
6. On `format-ok` the derived record is attached to the issue as a
   hidden comment block (`<!-- otelyssey-candidate ... -->`), the input
   of the admission workflow, which reads it through the REST API. The
   agent never sees it: the GitHub MCP server strips HTML comments and
   escapes quotes in every body it returns (settled by the first run,
   #5), so the comment also states in backticks what the review rules
   on - name, version, repository, path, tag, full sha - and the agent
   never re-derives what the gates established.

### review (gh-aw, engine copilot, on `format-ok` labelled)

Inputs: the intake comment's facts (name, version, repository, path,
tag, sha), the plugin at the sha (`plugin.json`, the README, every
`SKILL.md`, `mcp.json` when it exists, and a skill's annex files when
the manifest, the README, the `SKILL.md` files and `mcp.json` leave
the relevance unsettled: Markdown and JSON under the skill's directory
only, at most twenty files, two hundred lines and 64 KB each), the
store, the open and closed submission issues, and the vendor registry
read with the `web_fetch` tool (the shell's allowlist has no `curl`: on
#103 and #112 a `curl` was refused and the agent asked the contributor
instead; the page's source, `data/ecosystem/vendors.yaml` of
`open-telemetry/opentelemetry.io`, read through GitHub, is the
fallback). The agent:

- rules on **relevance** to OpenTelemetry in the broad sense, from the
  plugin's own description, skills, `mcp.json` and README, and states the
  evidence;
- rules on **resubmission** against the store, the same plugin under
  another name: the same repository, the same skills' content at any
  version or, when neither side has a skill, the same `mcp.json`
  servers; scope is not a criterion, two distinct plugins that serve
  the same need are both listed;
- **converses** on the issue through safe outputs (`add-comment`,
  `add-labels` / `remove-labels`, bounded): what is missing, what
  would make the plugin admissible, an answer to the contributor's
  replies (the workflow also triggers on `issue_comment` from the
  submitter while `format-ok` holds);
- **rules the categories**, one or several of the store's four, from
  the plugin's content, every one a named skill justifies, the
  principal first;
- **admits** by commenting the three rulings with their evidence and
  labelling `admissible`; or **rejects** with `rejected` and the
  reason, closing the issue. The agent writes no file and opens no
  pull request: the agents rule, the scripts write (settled by the
  first run, #5: the record cannot cross the MCP sanitizer exactly).
  The categories are the one value it contributes to the record, on the
  ruling's first line, an enum the admission reads and bounds.

Bounds: `max-ai-credits` per run, one comment at most per run, a
read-only shell, network limited to GitHub, the contributor's content
treated as untrusted (the agentic workflows read below gh-aw's
`approved` integrity on purpose, since a submission is external by
definition; no shell execution of plugin content).

### admission (deterministic, on `admissible` labelled)

`admission.yml` reads the intake comment through the REST API, writes
`.store/<name>.json` from its candidate block plus the ruling's
categories, `admitted_at` and zero `stats` (`scripts/admission.py`),
refuses a record the review's latest ruling does not name (the ruling's
first line carries the name, the version, the sha and the categories, so
an issue edited after the ruling is not admitted, and the label alone
admits nothing), checks the plugin still validates at its tag at the
record's sha, pushes `admission/<name>`,
opens the pull request labelled `admission` (`ci.yml` validates the
record against the store schema), waits for `ci`, squash-merges, runs
`build.py`, commits the generated artifacts to `main`, and closes the
submission issue with `admitted` and a comment linking the plugin's
page. One workflow chains the whole admission explicitly: no workflow
listens to every pull request event to find the admission one.

## Nightly

`nightly.yml`, once a day:

1. `scripts/stats.py`: for each record, stars, forks and watchers from
   the GitHub API (the workflow's token), `refreshed_at` set.
2. `scripts/releases.py`: for each record, the latest release tag of
   the repository (`git ls-remote --tags`, semver-sorted, the reading
   oddyssey-actions does); when it differs from `ref`, the format
   validation and the install on the hosts are replayed on it (the
   same scripts as intake, `releases.py --smoke`); on pass, `ref`,
   `sha` and `version` are updated and the derived fields read again
   from the new manifest, the repository's metadata filling the gaps
   as the intake does (a field neither gives keeps its value; an
   unreadable API lets the record's values stand in for the
   repository's, never holds a release back); on failure, an issue is
   opened for the contributor (one per plugin and tag, never repeated)
   and the record stays.
3. `build.py`, then one commit by the workflow's bot on `main`,
   `chore(store): nightly refresh`, only when something changed. The
   checkout persists no credential: the plugins are cloned and
   installed in the same job; the push authenticates through `gh`
   once the plugin checkouts are gone; the admission, likewise, checks
   out with the token only after its `rm -rf work`.

`duplicates.md` (gh-aw, weekly): audits the store for the same plugin
listed twice, on the review's definition (the same repository, the
same skills' content at any version or, when neither record has a
skill, the same `mcp.json` servers), and opens one review issue with
the evidence, nothing else; pairs a maintainer ruled `keep both` or
`not duplicates` on a past issue are not reported again.

## Errors and guard rails

- Every deterministic failure names the rule and the value: the
  contributor fixes the issue and the gates re-run.
- Actions pinned by commit SHA with the version in a comment;
  permissions minimal per job; the install smoke runs under an
  isolated HOME with no credential. A GitHub App installed on this
  repository only (Contents, Issues and Pull requests read and write,
  Checks read, Metadata read) is the pipeline's identity, `otelyssey-bot[bot]`:
  `intake.yml`, `admission.yml` and `nightly.yml` mint a one-hour
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
