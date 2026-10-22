# oddyssey

CLI toolbox for Observability-Driven Development (ODD): coding agents observe local runs on an OpenTelemetry/Grafana stack - or remote ones on any OpenTelemetry backend - and feed the next spec-driven improvement loop.

- Repository: [using-system/oddyssey](https://github.com/using-system/oddyssey), the plugin at `marketplace/oddyssey` in it
- Categories: `observability`, `instrumentation`, `backend`
- Version: 1.13.3 (`v1.13.3`, commit `bad606e2031e`)
- Author: [using-system](https://github.com/using-system)
- License: MIT
- Keywords: `claude-code`, `claude-code-plugin`, `claude-skills`, `mcp`, `ai-agents`, `observability`, `opentelemetry`, `developer-tools`
- Homepage: <https://github.com/using-system/oddyssey#readme>
- Stars 10, forks 2, watchers 0 (refreshed 2026-10-08T10:39:33Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install oddyssey@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install oddyssey@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add oddyssey@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install oddyssey --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install oddyssey@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install using-system/oddyssey/marketplace/oddyssey --ref bad606e2031e644dc72b38d17c8282c5f0b292a0
hermes plugins enable oddyssey
```

OpenClaw:

```text
git clone https://github.com/using-system/oddyssey && git -C oddyssey checkout bad606e2031e644dc72b38d17c8282c5f0b292a0
openclaw plugins install ./oddyssey/marketplace/oddyssey --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/using-system/oddyssey && git -C oddyssey checkout bad606e2031e644dc72b38d17c8282c5f0b292a0
mkdir -p ~/.vibe/plugins/oddyssey && cp -r ./oddyssey/marketplace/oddyssey/. ~/.vibe/plugins/oddyssey
```

OpenCode:

```text
git clone https://github.com/using-system/oddyssey ~/.opencode-plugins/oddyssey && git -C ~/.opencode-plugins/oddyssey checkout bad606e2031e644dc72b38d17c8282c5f0b292a0
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/oddyssey/marketplace/oddyssey/skills"
    ]
  },
  "mcp": {
    "oddyssey": {
      "type": "local",
      "command": [
        "uvx",
        "--refresh-package",
        "oddyssey-mcp",
        "oddyssey-mcp==1.13.3"
      ]
    }
  }
}
```
