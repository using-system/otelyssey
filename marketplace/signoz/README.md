# signoz

Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts

- Category: `backend`
- Repository: [SigNoz/agent-skills](https://github.com/SigNoz/agent-skills), the plugin at `plugins/signoz` in it
- Version: 2026.9.200 (`main`, commit `4cdc848eb480`)
- Author: [SigNoz](https://signoz.io)
- License: MIT
- Keywords: `signoz`, `opentelemetry`, `observability`, `mcp`, `clickhouse`, `tracing`, `logging`
- Homepage: <https://signoz.io>
- Stars 16, forks 11, watchers 2 (refreshed 2026-09-20T08:38:53Z)
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

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install signoz --trust
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

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install SigNoz/agent-skills/plugins/signoz --ref 4cdc848eb480f02bc07d06cb8d4f8486f635cbd6
hermes plugins enable signoz
```

OpenClaw:

```text
git clone https://github.com/using-system/otelyssey
openclaw plugins install signoz --marketplace ./otelyssey
```

Mistral Vibe:

```text
git clone https://github.com/SigNoz/agent-skills && git -C agent-skills checkout 4cdc848eb480f02bc07d06cb8d4f8486f635cbd6
mkdir -p ~/.vibe/plugins/signoz && cp -r agent-skills/plugins/signoz/. ~/.vibe/plugins/signoz
```
