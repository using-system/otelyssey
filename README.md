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

Hermes Agent, OpenClaw and Mistral Vibe take no marketplace url: their lines are on
each plugin's page. Hermes Agent also installs every listed plugin at once, pinned,
from the pack, after its review screen (Hermes from its main branch: the pack command
is newer than the 0.19.0 release):

```text
hermes plugins pack show https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
```

## Submit a plugin

Open a [plugin submission](https://github.com/using-system/otelyssey/issues/new?template=submit-plugin.yml):
a public GitHub repository holding a `plugin.json` in the Agent Plugins
format and a subject that is OpenTelemetry: its instrumentation, the
Collector, or a backend that ingests its telemetry. The
repository checks the format, installs the plugin, judges its relevance
to OpenTelemetry and whether it is a plugin already listed, talks to you
on the issue, and lists it. Every night it follows your releases: your
latest `X.Y.Z` or `vX.Y.Z` tag when it carries the plugin, otherwise a
new `version` in `plugin.json` on your default branch. It also refreshes
your repository's statistics. Plugins that compete on the same
scope are all listed: the marketplace never arbitrates between
competitors.

## Plugins

<!-- otelyssey:plugins -->
### Instrumentation

- [langwatch](https://github.com/langwatch/agent-plugin) by [LangWatch](https://langwatch.ai) - Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch. The hook emits the record over OTLP: an \`OTEL\_EXPORTER\_OTLP\_ENDPOINT\` in the environment takes precedence over the signed-in control plane. · [install](marketplace/langwatch/README.md)  
<img src="https://img.shields.io/badge/version-1.2.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [observability](https://github.com/BastiDood/skills) by [Basti Ortiz](https://bastidood.dev/) - Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation: one language-agnostic skill on spans as operation records, named log events, attributes under the OpenTelemetry semantic conventions, and exception recording, for adding or reviewing instrumentation in any OpenTelemetry SDK. · [install](marketplace/observability/README.md)  
<img src="https://img.shields.io/badge/version-0.1.7-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [stdtel](https://github.com/amiable-dev/skills-telemetry) by [amiable-dev](https://github.com/amiable-dev) - Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot, emitted as OpenTelemetry spans over OTLP/HTTP to any collector. Metadata only, no prompt or file content. · [install](marketplace/stdtel/README.md)  
<img src="https://img.shields.io/badge/version-0.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

### Backends

- [dynatrace-managed-mcp](https://github.com/dynatrace-oss/dynatrace-managed-mcp) by [Dynatrace](https://www.dynatrace.com) - MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters, the telemetry Dynatrace ingests from OneAgent and over OTLP. · [install](marketplace/dynatrace-managed-mcp/README.md)  
<img src="https://img.shields.io/badge/version-1.1.1-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [signoz](https://github.com/SigNoz/agent-skills) by [SigNoz](https://signoz.io) - Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts. Thirteen skills for an OpenTelemetry-native backend: setting up observability and the OpenTelemetry Collector, generating and explaining queries, creating and investigating alerts and dashboards, reducing telemetry cost, and writing ClickHouse queries against OpenTelemetry data. · [install](marketplace/signoz/README.md)  
<img src="https://img.shields.io/badge/version-2026.9.200-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

### Workflows

- [oddyssey](https://github.com/using-system/oddyssey) by [using-system](https://github.com/using-system) - A CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack, or remote ones on any OpenTelemetry backend, and feed the next spec-driven improvement loop. Skills and agents to instrument a codebase with OpenTelemetry, benchmark it with k6, observe a run through its metrics, traces, logs and profiles, and verify that a fix landed. Submitted through the first end-to-end run (#5). · [install](marketplace/oddyssey/README.md)  
<img src="https://img.shields.io/badge/version-1.13.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

<!-- /otelyssey:plugins -->
