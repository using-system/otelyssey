# signoz

Official SigNoz plugin for MCP setup, docs, queries, dashboards, and alerts

- Repository: [SigNoz/agent-skills](https://github.com/SigNoz/agent-skills), the plugin at `plugins/signoz` in it
- Categories: `backend`
- Version: 2026.10.2300 (`main`, commit `6bd555327dee`)
- Author: [SigNoz](https://signoz.io)
- License: MIT
- Keywords: `signoz`, `opentelemetry`, `observability`, `mcp`, `clickhouse`, `tracing`, `logging`
- Homepage: <https://signoz.io>
- Stars 19, forks 14, watchers 2 (refreshed 2026-10-20T08:36:53Z)

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
hermes plugins install SigNoz/agent-skills/plugins/signoz --ref 6bd555327dee977d14d6d850b1cfb9fe872df102
hermes plugins enable signoz
```

OpenClaw:

```text
git clone https://github.com/SigNoz/agent-skills && git -C agent-skills checkout 6bd555327dee977d14d6d850b1cfb9fe872df102
openclaw plugins install ./agent-skills/plugins/signoz --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/SigNoz/agent-skills && git -C agent-skills checkout 6bd555327dee977d14d6d850b1cfb9fe872df102
mkdir -p ~/.vibe/plugins/signoz && cp -r ./agent-skills/plugins/signoz/. ~/.vibe/plugins/signoz
```

OpenCode:

```text
git clone https://github.com/SigNoz/agent-skills ~/.opencode-plugins/signoz && git -C ~/.opencode-plugins/signoz checkout 6bd555327dee977d14d6d850b1cfb9fe872df102
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/signoz/plugins/signoz/skills"
    ]
  },
  "mcp": {
    "signoz": {
      "type": "remote",
      "url": "https://not-setup/mcp"
    }
  }
}
```
