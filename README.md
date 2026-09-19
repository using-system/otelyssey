# otelyssey

A marketplace of OpenTelemetry agent plugins in the
[Agent Plugins](https://agent-plugins.org/) format, run by the repository
itself: a contributor submits a plugin once, through an issue, and the
repository validates it, admits it, follows its releases and lists it.

Add the marketplace; each plugin's page under `marketplace/` gives its install line:

```text
claude plugin marketplace add using-system/otelyssey
copilot plugin marketplace add using-system/otelyssey
```

Claude Code clones a plugin's repository over SSH: it needs a GitHub SSH
key, or `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` in the environment, or
`git config --global url.https://github.com/.insteadOf git@github.com:`,
to clone over HTTPS instead. Copilot CLI needs none of these.

## Plugins

<!-- otelyssey:table -->
| Plugin | Description | Category | Repository | Stars | Forks | Watchers |
| --- | --- | --- | --- | ---: | ---: | ---: |
| [oddyssey](marketplace/oddyssey/README.md) | A CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack, or remote ones on any OpenTelemetry backend, and feed the next spec-driven improvement loop. Skills and agents to instrument a codebase with OpenTelemetry, benchmark it with k6, observe a run through its metrics, traces, logs and profiles, and verify that a fix landed. Submitted through the first end-to-end run (#5). | workflow | [using-system/oddyssey](https://github.com/using-system/oddyssey) | 9 | 2 | 0 |
<!-- /otelyssey:table -->

## Submit a plugin

Open a [plugin submission](https://github.com/using-system/otelyssey/issues/new?template=submit-plugin.yml):
a public GitHub repository holding a `plugin.json` in the Agent Plugins
format, a release tag, and a subject that is OpenTelemetry. The
repository checks the format, installs the plugin, judges its relevance
and its novelty, talks to you on the issue, and lists it. Every night it
follows your releases and refreshes your repository's statistics.

The design is in
[docs/superpowers/specs/2026-09-19-otelyssey-design.md](docs/superpowers/specs/2026-09-19-otelyssey-design.md).
