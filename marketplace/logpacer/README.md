# logpacer

Connect your coding agent to the hosted LogPacer MCP server, with skills for setting up collection, instrumenting apps and investigating logs.

- Repository: [LogPacer/logpacer-marketplace](https://github.com/LogPacer/logpacer-marketplace), the plugin at the root of it
- Categories: `backend`, `instrumentation`
- Version: 0.1.2 (`main`, commit `e1d62893fe42`)
- Author: [LogPacer](https://logpacer.com)
- License: MIT
- Keywords: `logpacer`, `logs`, `observability`, `mcp`, `otlp`, `metrics`, `traces`
- Homepage: <https://logpacer.com>
- Stars 0, forks 0, watchers 0 (refreshed 2026-11-11T12:46:26Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install logpacer@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install logpacer@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add logpacer@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install logpacer --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install logpacer@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/LogPacer/logpacer-marketplace`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install LogPacer/logpacer-marketplace --ref e1d62893fe420523e50eadecbd1d882adb795a67
hermes plugins enable logpacer
```

OpenClaw:

```text
git clone https://github.com/LogPacer/logpacer-marketplace && git -C logpacer-marketplace checkout e1d62893fe420523e50eadecbd1d882adb795a67
openclaw plugins install ./logpacer-marketplace --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/LogPacer/logpacer-marketplace && git -C logpacer-marketplace checkout e1d62893fe420523e50eadecbd1d882adb795a67
mkdir -p ~/.vibe/plugins/logpacer && cp -r ./logpacer-marketplace/. ~/.vibe/plugins/logpacer
```

OpenCode:

```text
git clone https://github.com/LogPacer/logpacer-marketplace ~/.opencode-plugins/logpacer && git -C ~/.opencode-plugins/logpacer checkout e1d62893fe420523e50eadecbd1d882adb795a67
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/logpacer/skills"
    ]
  },
  "mcp": {
    "logpacer": {
      "type": "remote",
      "url": "https://app.logpacer.com/mcp"
    }
  }
}
```
