# respan

Respan for ChatGPT and Codex: inspect LLM logs and traces, and manage prompts, datasets, evaluators, experiments and monitors in your Respan workspace.

- Repository: [respanai/respan](https://github.com/respanai/respan), the plugin at `chatgpt-plugin` in it
- Categories: `backend`, `instrumentation`
- Version: 1.0.0 (`main`, commit `cc9a1e326b81`)
- Author: [Respan](https://respan.ai)
- License: Apache-2.0
- Keywords: `llm`, `observability`, `tracing`, `evals`, `prompts`, `datasets`, `mcp`
- Homepage: <https://respan.ai>
- Stars 52, forks 15, watchers 2 (refreshed 2026-10-22T08:40:25Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install respan@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install respan@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add respan@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install respan --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install respan@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install respanai/respan/chatgpt-plugin --ref cc9a1e326b8191ff32c99bce2d8425d10867ba1f
hermes plugins enable respan
```

OpenClaw:

```text
git clone https://github.com/respanai/respan && git -C respan checkout cc9a1e326b8191ff32c99bce2d8425d10867ba1f
openclaw plugins install ./respan/chatgpt-plugin --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/respanai/respan && git -C respan checkout cc9a1e326b8191ff32c99bce2d8425d10867ba1f
mkdir -p ~/.vibe/plugins/respan && cp -r ./respan/chatgpt-plugin/. ~/.vibe/plugins/respan
```

OpenCode:

```text
git clone https://github.com/respanai/respan ~/.opencode-plugins/respan && git -C ~/.opencode-plugins/respan checkout cc9a1e326b8191ff32c99bce2d8425d10867ba1f
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/respan/chatgpt-plugin/skills"
    ]
  },
  "mcp": {
    "respan": {
      "type": "remote",
      "url": "https://mcp.respan.ai/mcp"
    }
  }
}
```
