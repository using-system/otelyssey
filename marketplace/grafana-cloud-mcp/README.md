# grafana-cloud-mcp

For Grafana Cloud: a hosted MCP server with OAuth sign-in for dashboards, metrics, logs, traces, alerts, and incidents. Nothing to install.

- Repository: [grafana/ai-marketplace](https://github.com/grafana/ai-marketplace), the plugin at `kiro/grafana-cloud-mcp` in it
- Categories: `backend`
- Version: 0.3.1 (`main`, commit `77a6f1a277c3`)
- Author: Grafana Labs
- License: Apache-2.0
- Keywords: `grafana`, `mcp`, `cloud`, `observability`, `dashboards`, `prometheus`, `loki`, `tempo`, `alerting`, `incidents`, `oncall`, `monitoring`
- Homepage: <https://github.com/grafana/ai-marketplace/tree/main/plugins/grafana-cloud-mcp>
- Stars 0, forks 0, watchers 0 (refreshed 2026-11-11T12:33:16Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install grafana-cloud-mcp@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install grafana-cloud-mcp@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add grafana-cloud-mcp@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install grafana-cloud-mcp --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install grafana-cloud-mcp@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install grafana/ai-marketplace/kiro/grafana-cloud-mcp --ref 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
hermes plugins enable grafana-cloud-mcp
```

OpenClaw:

```text
git clone https://github.com/grafana/ai-marketplace && git -C ai-marketplace checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
openclaw plugins install ./ai-marketplace/kiro/grafana-cloud-mcp --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/grafana/ai-marketplace && git -C ai-marketplace checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
mkdir -p ~/.vibe/plugins/grafana-cloud-mcp && cp -r ./ai-marketplace/kiro/grafana-cloud-mcp/. ~/.vibe/plugins/grafana-cloud-mcp
```

OpenCode:

```text
git clone https://github.com/grafana/ai-marketplace ~/.opencode-plugins/grafana-cloud-mcp && git -C ~/.opencode-plugins/grafana-cloud-mcp checkout 77a6f1a277c35d3205dc34abf78d85e49ca5ccf1
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/grafana-cloud-mcp/kiro/grafana-cloud-mcp/skills"
    ]
  },
  "mcp": {
    "grafana-cloud": {
      "type": "remote",
      "url": "https://mcp.grafana.com/mcp"
    }
  }
}
```
