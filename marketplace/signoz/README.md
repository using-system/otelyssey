# signoz

Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts. Thirteen skills for an OpenTelemetry-native backend: setting up observability and the OpenTelemetry Collector, generating and explaining queries, creating and investigating alerts and dashboards, reducing telemetry cost, and writing ClickHouse queries against OpenTelemetry data.

- Category: `backend`
- Repository: [SigNoz/agent-skills](https://github.com/SigNoz/agent-skills), the plugin at `plugins/signoz` in it
- Version: 2026.9.200 (`main`, commit `4cdc848eb480`)
- Author: [SigNoz](https://signoz.io)
- License: MIT
- Keywords: `signoz`, `opentelemetry`, `observability`, `mcp`, `clickhouse`, `tracing`, `logging`
- Homepage: <https://signoz.io>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-20T00:44:57Z)
- Admitted from [issue #50](https://github.com/using-system/otelyssey/issues/50) on 2026-09-20

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install signoz@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install signoz@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add signoz@otelyssey
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install signoz@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```
