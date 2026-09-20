# otelyssey

A marketplace of OpenTelemetry agent plugins in the
[Agent Plugins](https://agent-plugins.org/) format, run by the repository
itself: submit a plugin once; the repository checks it, lists it and
follows its releases.

## Install

Add the marketplace to your client:

```text
claude plugin marketplace add using-system/otelyssey
copilot plugin marketplace add using-system/otelyssey
codex plugin marketplace add using-system/otelyssey
grok plugin marketplace add using-system/otelyssey
apm marketplace add using-system/otelyssey
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
```

Then pick a plugin below: its page has the install line — and the ones for
VS Code, Kiro, OpenClaw and Mistral Vibe.

## Submit a plugin

**[Open a plugin submission](https://github.com/using-system/otelyssey/issues/new?template=submit-plugin.yml)**
— one form, the repository does the rest.

Your plugin needs:

- a public GitHub repository;
- a `plugin.json` in the [Agent Plugins](https://agent-plugins.org/) format,
  at the repository's root or in a subdirectory: the form asks for its URL,
  everything else is read from it;
- OpenTelemetry as its subject: instrumentation, semantic conventions, the
  Collector, or a backend that ingests its telemetry.

The repository answers on the issue. Once listed, it follows your releases
every night.

## Plugins

<!-- otelyssey:plugins -->
### Instrumentation

- [observability](https://github.com/BastiDood/skills) by [Basti Ortiz](https://bastidood.dev/) - Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation. · [install](marketplace/observability/README.md)  
<img src="https://img.shields.io/badge/version-0.1.7-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [stdtel](https://github.com/amiable-dev/skills-telemetry) by [amiable-dev](https://github.com/amiable-dev) - Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot. · also in Observability · [install](marketplace/stdtel/README.md)  
<img src="https://img.shields.io/badge/version-0.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

### Backends

- [dynatrace-managed-mcp](https://github.com/dynatrace-oss/dynatrace-managed-mcp) by [Dynatrace](https://www.dynatrace.com) - MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters. · [install](marketplace/dynatrace-managed-mcp/README.md)  
<img src="https://img.shields.io/badge/version-1.1.1-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [langwatch](https://github.com/langwatch/agent-plugin) by [LangWatch](https://langwatch.ai) - Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch. · [install](marketplace/langwatch/README.md)  
<img src="https://img.shields.io/badge/version-1.2.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [sentry](https://github.com/getsentry/agent-plugin) by [Sentry](https://sentry.io) - Set up Sentry, debug production issues, and configure application monitoring. · [install](marketplace/sentry/README.md)  
<img src="https://img.shields.io/badge/version-1.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

- [signoz](https://github.com/SigNoz/agent-skills) by [SigNoz](https://signoz.io) - Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts · [install](marketplace/signoz/README.md)  
<img src="https://img.shields.io/badge/version-2026.9.200-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

### Observability

- [oddyssey](https://github.com/using-system/oddyssey) by [using-system](https://github.com/using-system) - Observability-Driven Development for CLI coding agents · also in Instrumentation, Backends · [install](marketplace/oddyssey/README.md)  
<img src="https://img.shields.io/badge/version-1.13.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version">&nbsp;&nbsp;<img src="https://img.shields.io/github/created-at/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at">&nbsp;&nbsp;<img src="https://img.shields.io/github/last-commit/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit">&nbsp;&nbsp;<img src="https://img.shields.io/github/license/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license">&nbsp;&nbsp;<img src="https://img.shields.io/github/stars/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars">&nbsp;&nbsp;<img src="https://img.shields.io/github/forks/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks">&nbsp;&nbsp;<img src="https://img.shields.io/github/watchers/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers">

<!-- /otelyssey:plugins -->
