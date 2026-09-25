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
### 🧭 Instrumentation

Put the telemetry in: SDKs, semantic conventions, instrumentation advice.

- <img src="https://github.com/BastiDood.png?size=40" width="20" height="20" alt=""> **[observability](marketplace/observability/README.md)** by [Basti Ortiz](https://bastidood.dev/) — Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation.  
<a href="#"><img src="https://img.shields.io/github/stars/BastiDood/skills?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-0.1.7-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/BastiDood/skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/ollygarden.png?size=40" width="20" height="20" alt=""> **[opentelemetry-agent-skills](marketplace/opentelemetry-agent-skills/README.md)** by [OllyGarden](https://github.com/ollygarden) — Vendor-neutral OpenTelemetry skills for AI coding agents, grounded in upstream sources: SDK setup per language, the Collector and OCB, OTTL, declarative configuration, semantic conventions, upgrades and migrations. · also in Collector  
<a href="#"><img src="https://img.shields.io/github/stars/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.0.0-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/ollygarden/opentelemetry-agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/amiable-dev.png?size=40" width="20" height="20" alt=""> **[stdtel](marketplace/stdtel/README.md)** by [amiable-dev](https://github.com/amiable-dev) — Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot. · also in Backends  
<a href="#"><img src="https://img.shields.io/github/stars/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-0.4.0-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/amiable-dev/skills-telemetry?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

### 🏛️ Backends

Talk to a backend: query it, its dashboards, alerts and issues.

- <img src="https://github.com/Arize-ai.png?size=40" width="20" height="20" alt=""> **[arize-phoenix](marketplace/arize-phoenix/README.md)** by [Arize AI](https://arize.com) — Connect to your Phoenix instance to debug, evaluate, and improve LLM applications.  
<a href="#"><img src="https://img.shields.io/github/stars/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-0.1.0-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/Arize-ai/phoenix?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/dynatrace-oss.png?size=40" width="20" height="20" alt=""> **[dynatrace-managed-mcp](marketplace/dynatrace-managed-mcp/README.md)** by [Dynatrace](https://www.dynatrace.com) — MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters.  
<a href="#"><img src="https://img.shields.io/github/stars/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.1.1-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/dynatrace-oss/dynatrace-managed-mcp?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/langwatch.png?size=40" width="20" height="20" alt=""> **[langwatch](marketplace/langwatch/README.md)** by [LangWatch](https://langwatch.ai) — Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch.  
<a href="#"><img src="https://img.shields.io/github/stars/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.2.0-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/langwatch/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/DataDog.png?size=40" width="20" height="20" alt=""> **[pup](marketplace/pup/README.md)** by Datadog — Datadog API CLI with 49 command groups, 300+ subcommands. Skills and domain agents for monitoring, logs, APM, security, and infrastructure.  
<a href="#"><img src="https://img.shields.io/github/stars/DataDog/pup?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.23.2-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/DataDog/pup?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/getsentry.png?size=40" width="20" height="20" alt=""> **[sentry](marketplace/sentry/README.md)** by [Sentry](https://sentry.io) — Set up Sentry, debug production issues, and configure application monitoring.  
<a href="#"><img src="https://img.shields.io/github/stars/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.4.0-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/getsentry/agent-plugin?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/SigNoz.png?size=40" width="20" height="20" alt=""> **[signoz](marketplace/signoz/README.md)** by [SigNoz](https://signoz.io) — Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts  
<a href="#"><img src="https://img.shields.io/github/stars/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-2026.9.2500-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/SigNoz/agent-skills?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

- <img src="https://github.com/SumoLogic.png?size=40" width="20" height="20" alt=""> **[sumo-logic](marketplace/sumo-logic/README.md)** by [Sumo Logic](https://www.sumologic.com) — Query Sumo Logic logs, alerts, dashboards, and SIEM insights directly from Copilot. Connects to the Sumo Logic MCP server for natural language observability investigations.  
<a href="#"><img src="https://img.shields.io/github/stars/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.0.1-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/SumoLogic/sumologic-ai-plugins?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

### 🔭 Observability

Read it back: observe a run through its telemetry, wherever it lands.

- <img src="https://github.com/using-system.png?size=40" width="20" height="20" alt=""> **[oddyssey](marketplace/oddyssey/README.md)** by [using-system](https://github.com/using-system) — CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack - or remote ones on any OpenTelemetry backend - and feed the next spec-driven improvement loop. · also in Instrumentation, Backends  
<a href="#"><img src="https://img.shields.io/github/stars/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2UzYjM0MSIgZD0iTTEyIDFsMy40IDcgNy42IDEuMS01LjUgNS40IDEuMyA3LjZMMTIgMTguNSA1LjIgMjIuMWwxLjMtNy42TDEgOS4xIDguNiA4eiIvPjwvc3ZnPg%3D%3D&color=e3b341" alt="stars"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/badge/version-1.13.1-3b7dd8?style=flat-square&labelColor=2b2b2b&color=3b7dd8" alt="version"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/last-commit/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=2ea44f" alt="last-commit"></a>&nbsp;&nbsp;<a href="#"><img src="https://img.shields.io/github/license/using-system/oddyssey?style=flat-square&labelColor=2b2b2b&color=6b6b6b" alt="license"></a>

<!-- /otelyssey:plugins -->
