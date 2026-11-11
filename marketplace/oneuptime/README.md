# oneuptime

Work with your OneUptime project from your coding agent: investigate and respond to incidents and alerts, check monitors and status pages, and query logs, metrics and traces.

- Repository: [OneUptime/oneuptime-agent-plugin](https://github.com/OneUptime/oneuptime-agent-plugin), the plugin at the root of it
- Categories: `backend`, `instrumentation`
- Version: 14.0.103 (`main`, commit `d0664f5126b6`)
- Author: [OneUptime](https://oneuptime.com)
- License: Apache-2.0
- Keywords: `incident management`, `monitoring`, `status page`, `on-call`, `observability`, `alerts`, `logs`
- Homepage: <https://oneuptime.com/docs/ai/mcp-server>
- Stars 0, forks 0, watchers 0 (refreshed 2026-11-11T13:53:35Z)

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

Kiro: Import power from GitHub, `https://github.com/OneUptime/oneuptime-agent-plugin`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install OneUptime/oneuptime-agent-plugin --ref d0664f5126b6571b8a7cfcb2fdc63f46b12c2ba6
hermes plugins enable oneuptime
```

OpenClaw:

```text
git clone https://github.com/OneUptime/oneuptime-agent-plugin && git -C oneuptime-agent-plugin checkout d0664f5126b6571b8a7cfcb2fdc63f46b12c2ba6
openclaw plugins install ./oneuptime-agent-plugin --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/OneUptime/oneuptime-agent-plugin && git -C oneuptime-agent-plugin checkout d0664f5126b6571b8a7cfcb2fdc63f46b12c2ba6
mkdir -p ~/.vibe/plugins/oneuptime && cp -r ./oneuptime-agent-plugin/. ~/.vibe/plugins/oneuptime
```

OpenCode:

```text
git clone https://github.com/OneUptime/oneuptime-agent-plugin ~/.opencode-plugins/oneuptime && git -C ~/.opencode-plugins/oneuptime checkout d0664f5126b6571b8a7cfcb2fdc63f46b12c2ba6
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/oneuptime/skills"
    ]
  },
  "mcp": {
    "oneuptime": {
      "type": "remote",
      "url": "https://oneuptime.com/mcp"
    }
  }
}
```
