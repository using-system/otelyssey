# grafana-mcp

For self-hosted Grafana, or any Grafana with a service-account token: dashboards, Prometheus, Loki, alerting, incidents, and OnCall via the Grafana MCP server, run locally in Docker.

- Repository: [grafana/ai-marketplace](https://github.com/grafana/ai-marketplace), the plugin at `kiro/grafana-mcp` in it
- Categories: `backend`
- Version: 0.3.1 (`main`, commit `77a6f1a277c3`)
- Author: Grafana Labs
- License: Apache-2.0
- Keywords: `grafana`, `mcp`, `observability`, `dashboards`, `prometheus`, `loki`, `alerting`, `incidents`, `oncall`, `monitoring`
- Homepage: <https://github.com/grafana/ai-marketplace/tree/main/plugins/grafana-mcp>
- Stars 20, forks 6, watchers 0 (refreshed 2026-11-12T11:21:19Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install grafana-mcp@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install grafana-mcp@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add grafana-mcp@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install grafana-mcp --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install grafana-mcp@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install grafana/ai-marketplace/kiro/grafana-mcp --ref 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
hermes plugins enable grafana-mcp
```

OpenClaw:

```text
git clone https://github.com/grafana/ai-marketplace && git -C ai-marketplace checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
openclaw plugins install ./ai-marketplace/kiro/grafana-mcp --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/grafana/ai-marketplace && git -C ai-marketplace checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
mkdir -p ~/.vibe/plugins/grafana-mcp && cp -r ./ai-marketplace/kiro/grafana-mcp/. ~/.vibe/plugins/grafana-mcp
```

OpenCode:

```text
git clone https://github.com/grafana/ai-marketplace ~/.opencode-plugins/grafana-mcp && git -C ~/.opencode-plugins/grafana-mcp checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/grafana-mcp/kiro/grafana-mcp/skills"
    ]
  },
  "mcp": {
    "grafana": {
      "type": "local",
      "command": [
        "docker",
        "run",
        "--rm",
        "-i",
        "-e",
        "GRAFANA_URL",
        "-e",
        "GRAFANA_SERVICE_ACCOUNT_TOKEN",
        "grafana/mcp-grafana",
        "-t",
        "stdio"
      ],
      "environment": {
        "GRAFANA_URL": "{env:GRAFANA_URL}",
        "GRAFANA_SERVICE_ACCOUNT_TOKEN": "{env:GRAFANA_SERVICE_ACCOUNT_TOKEN}"
      }
    }
  }
}
```
