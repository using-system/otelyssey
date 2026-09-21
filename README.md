# otelyssey

A marketplace of OpenTelemetry agent plugins in the
[Agent Plugins](https://agent-plugins.org/) format, run by the repository
itself: submit a plugin once; the repository checks it, lists it and
follows its releases.

<p align="center">
  <img src="assets/images/otelyssey-banner.jpg" alt="otelyssey: a Greek warship crossing a sea of telemetry toward lighthouses" width="800">
</p>

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
every night. Bugs, ideas, code: see [CONTRIBUTING](CONTRIBUTING.md).

## Plugins

<!-- otelyssey:plugins -->
### Instrumentation

- [observability](marketplace/observability/README.md) by [Basti Ortiz](https://bastidood.dev/) - Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation.  
<a href="#"><img src="https://img.shields.io/badge/version-0.1.7-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [opentelemetry-agent-skills](marketplace/opentelemetry-agent-skills/README.md) by [OllyGarden](https://github.com/ollygarden) - Vendor-neutral OpenTelemetry skills for AI coding agents, grounded in upstream sources: SDK setup per language, the Collector and OCB, OTTL, declarative configuration, semantic conventions, upgrades and migrations. · also in Collector  
<a href="#"><img src="https://img.shields.io/badge/version-1.0.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [stdtel](marketplace/stdtel/README.md) by [amiable-dev](https://github.com/amiable-dev) - Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot. · also in Backends  
<a href="#"><img src="https://img.shields.io/badge/version-0.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

### Backends

- [arize-phoenix](marketplace/arize-phoenix/README.md) by [Arize AI](https://arize.com) - Connect to your Phoenix instance to debug, evaluate, and improve LLM applications.  
<a href="#"><img src="https://img.shields.io/badge/version-0.1.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [dynatrace-managed-mcp](marketplace/dynatrace-managed-mcp/README.md) by [Dynatrace](https://www.dynatrace.com) - MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters.  
<a href="#"><img src="https://img.shields.io/badge/version-1.1.1-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [langwatch](marketplace/langwatch/README.md) by [LangWatch](https://langwatch.ai) - Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch.  
<a href="#"><img src="https://img.shields.io/badge/version-1.2.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [pup](marketplace/pup/README.md) by Datadog - Datadog API CLI with 49 command groups, 300+ subcommands. Skills and domain agents for monitoring, logs, APM, security, and infrastructure.  
<a href="#"><img src="https://img.shields.io/badge/version-1.23.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [sentry](marketplace/sentry/README.md) by [Sentry](https://sentry.io) - Set up Sentry, debug production issues, and configure application monitoring.  
<a href="#"><img src="https://img.shields.io/badge/version-1.4.0-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [signoz](marketplace/signoz/README.md) by [SigNoz](https://signoz.io) - Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts  
<a href="#"><img src="https://img.shields.io/badge/version-2026.9.1700-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

- [sumo-logic](marketplace/sumo-logic/README.md) by [Sumo Logic](https://www.sumologic.com) - Query Sumo Logic logs, alerts, dashboards, and SIEM insights directly from Copilot. Connects to the Sumo Logic MCP server for natural language observability investigations.  
<a href="#"><img src="https://img.shields.io/badge/version-1.0.1-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

### Observability

- [oddyssey](marketplace/oddyssey/README.md) by [using-system](https://github.com/using-system) - CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack - or remote ones on any OpenTelemetry backend - and feed the next spec-driven improvement loop. · also in Instrumentation, Backends  
<a href="#"><img src="https://img.shields.io/badge/version-1.13.1-6b6b6b?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/created-at/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="created-at"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/stars/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/forks/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="forks"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/watchers/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="watchers"></a>

<!-- /otelyssey:plugins -->
