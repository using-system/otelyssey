# pepe

Find why an HTTP endpoint is slow and prove a fix: ping it by phase, load-test it, see which operation inside the service the time goes to (from its OpenTelemetry spans), and compare before and after. A skill and pepe's MCP server, under guardrails.

- Repository: [omarmhaimdat/pepe](https://github.com/omarmhaimdat/pepe), the plugin at the root of it
- Categories: `observability`, `instrumentation`
- Version: 0.59.0 (`v0.59.0`, commit `066acd23c4c8`)
- Author: [Omar Mhaimdat](https://github.com/omarmhaimdat)
- License: MIT
- Keywords: `http`, `load-testing`, `latency`, `performance`, `opentelemetry`, `benchmark`, `mcp`
- Homepage: <https://pepe.mhaimdat.com/docs/agents.html>
- Stars 97, forks 3, watchers 1 (refreshed 2026-11-12T11:21:19Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install pepe@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install pepe@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add pepe@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install pepe --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install pepe@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/omarmhaimdat/pepe`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install omarmhaimdat/pepe --ref 066acd23c4c8d07af177aee9c632c3969ad108aa
hermes plugins enable pepe
```

OpenClaw:

```text
git clone https://github.com/omarmhaimdat/pepe && git -C pepe checkout 066acd23c4c8d07af177aee9c632c3969ad108aa
openclaw plugins install ./pepe --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/omarmhaimdat/pepe && git -C pepe checkout 066acd23c4c8d07af177aee9c632c3969ad108aa
mkdir -p ~/.vibe/plugins/pepe && cp -r ./pepe/. ~/.vibe/plugins/pepe
```

OpenCode:

```text
git clone https://github.com/omarmhaimdat/pepe ~/.opencode-plugins/pepe && git -C ~/.opencode-plugins/pepe checkout 066acd23c4c8d07af177aee9c632c3969ad108aa
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/pepe/skills"
    ]
  },
  "mcp": {
    "pepe": {
      "type": "local",
      "command": [
        "pepe",
        "mcp",
        "--max-requests",
        "10000",
        "--max-rate",
        "500",
        "--max-concurrency",
        "64"
      ]
    }
  }
}
```
