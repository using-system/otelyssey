# oneuptime

Work with your OneUptime project from ChatGPT: investigate and respond to incidents and alerts, check monitors and status pages, and query logs, metrics and traces.

- Repository: [OneUptime/oneuptime](https://github.com/OneUptime/oneuptime), the plugin at `packages/App/FeatureSet/MCP/ChatGPTPlugin` in it
- Categories: `backend`
- Version: 1.0.0 (`14.0.96`, commit `216a7fc90cc7`)
- Author: [OneUptime](https://oneuptime.com)
- License: Apache-2.0
- Keywords: `incident management`, `monitoring`, `status page`, `on-call`, `observability`, `alerts`, `logs`
- Homepage: <https://oneuptime.com/docs/ai/mcp-server>
- Stars 7768, forks 482, watchers 27 (refreshed 2026-10-29T10:03:03Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install oneuptime@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install oneuptime@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add oneuptime@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install oneuptime --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install oneuptime@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install OneUptime/oneuptime/packages/App/FeatureSet/MCP/ChatGPTPlugin --ref 216a7fc90cc703f37247996aca8ee3a90cb81d8d
hermes plugins enable oneuptime
```

OpenClaw:

```text
git clone https://github.com/OneUptime/oneuptime && git -C oneuptime checkout 216a7fc90cc703f37247996aca8ee3a90cb81d8d
openclaw plugins install ./oneuptime/packages/App/FeatureSet/MCP/ChatGPTPlugin --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/OneUptime/oneuptime && git -C oneuptime checkout 216a7fc90cc703f37247996aca8ee3a90cb81d8d
mkdir -p ~/.vibe/plugins/oneuptime && cp -r ./oneuptime/packages/App/FeatureSet/MCP/ChatGPTPlugin/. ~/.vibe/plugins/oneuptime
```

OpenCode:

```text
git clone https://github.com/OneUptime/oneuptime ~/.opencode-plugins/oneuptime && git -C ~/.opencode-plugins/oneuptime checkout 216a7fc90cc703f37247996aca8ee3a90cb81d8d
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "oneuptime": {
      "type": "remote",
      "url": "https://oneuptime.com/mcp"
    }
  }
}
```
