# otelyssey

A marketplace of OpenTelemetry agent plugins in the
[Agent Plugins](https://agent-plugins.org/) format, run by the repository
itself: a contributor submits a plugin once, through an issue, and the
repository validates it, admits it, follows its releases and lists it.

Add the marketplace; each plugin's page under `marketplace/` gives its install line:

```text
claude plugin marketplace add using-system/otelyssey
copilot plugin marketplace add using-system/otelyssey
codex plugin marketplace add using-system/otelyssey
apm marketplace add using-system/otelyssey
```

VS Code: `"chat.plugins.marketplaces": ["using-system/otelyssey"]` in `settings.json`.

## Submit a plugin

Open a [plugin submission](https://github.com/using-system/otelyssey/issues/new?template=submit-plugin.yml):
a public GitHub repository holding a `plugin.json` in the Agent Plugins
format and a subject that is OpenTelemetry. The
repository checks the format, installs the plugin, judges its relevance
to OpenTelemetry and whether it is a plugin already listed, talks to you
on the issue, and lists it. Every night it follows your releases (a
new `X.Y.Z` or `vX.Y.Z` tag or, without tags, a new `version` in
`plugin.json` on your default branch) and refreshes your repository's
statistics. Plugins that compete on the same
scope are all listed: the marketplace never arbitrates between
competitors.

## Plugins

<!-- otelyssey:plugins -->
### Instrumentation

- [langwatch](https://github.com/langwatch/agent-plugin) by [LangWatch](https://langwatch.ai) - Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch. The hook emits the record over OTLP: an \`OTEL\_EXPORTER\_OTLP\_ENDPOINT\` in the environment takes precedence over the signed-in control plane. · [install](marketplace/langwatch/README.md)  
<img src="https://img.shields.io/badge/version-1.2.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [stdtel](https://github.com/amiable-dev/skills-telemetry) by [amiable-dev](https://github.com/amiable-dev) - Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot, emitted as OpenTelemetry spans over OTLP/HTTP to any collector. Metadata only, no prompt or file content. · [install](marketplace/stdtel/README.md)  
<img src="https://img.shields.io/badge/version-0.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

### Workflows

- [oddyssey](https://github.com/using-system/oddyssey) by [using-system](https://github.com/using-system) - A CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack, or remote ones on any OpenTelemetry backend, and feed the next spec-driven improvement loop. Skills and agents to instrument a codebase with OpenTelemetry, benchmark it with k6, observe a run through its metrics, traces, logs and profiles, and verify that a fix landed. Submitted through the first end-to-end run (#5). · [install](marketplace/oddyssey/README.md)  
<img src="https://img.shields.io/badge/version-1.13.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

<!-- /otelyssey:plugins -->
