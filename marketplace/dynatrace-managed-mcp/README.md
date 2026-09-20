# dynatrace-managed-mcp

MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters, the telemetry Dynatrace ingests from OneAgent and over OTLP.

- Category: `backend`
- Repository: [dynatrace-oss/dynatrace-managed-mcp](https://github.com/dynatrace-oss/dynatrace-managed-mcp), the plugin at the root of it
- Version: 1.1.1 (`main`, commit `52959ebce94e`)
- Author: [Dynatrace](https://www.dynatrace.com)
- License: Apache-2.0
- Keywords: `dynatrace`, `dynatrace-managed`, `mcp`, `observability`, `monitoring`, `apm`, `logs`, `metrics`, `slo`, `opentelemetry`
- Homepage: <https://github.com/dynatrace-oss/dynatrace-managed-mcp#readme>
- Stars 29, forks 12, watchers 1 (refreshed 2026-09-20T08:38:53Z)
- Admitted from [issue #51](https://github.com/using-system/otelyssey/issues/51) on 2026-09-20

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install dynatrace-managed-mcp@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install dynatrace-managed-mcp@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add dynatrace-managed-mcp@otelyssey
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install dynatrace-managed-mcp@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/dynatrace-oss/dynatrace-managed-mcp`.
