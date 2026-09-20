# langwatch

Records which repository and branch each coding-agent session worked in, and teaches the agent to read its own traces back from LangWatch.

- Categories: `instrumentation`
- Repository: [langwatch/agent-plugin](https://github.com/langwatch/agent-plugin), the plugin at the root of it
- Version: 1.2.0 (`v1.2.0`, commit `5ca4f7addc97`)
- Author: [LangWatch](https://langwatch.ai)
- License: MIT
- Keywords: `langwatch`, `observability`, `telemetry`, `traces`, `coding-agent`
- Homepage: <https://docs.langwatch.ai>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-20T00:09:29Z)
- Admitted from [issue #42](https://github.com/using-system/otelyssey/issues/42) on 2026-09-20

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install langwatch@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install langwatch@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add langwatch@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install langwatch --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install langwatch@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/langwatch/agent-plugin`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install langwatch/agent-plugin --ref 5ca4f7addc97fd2bb8cfdfe3f086fc7c5407b88d
hermes plugins enable langwatch
```

OpenClaw:

```text
openclaw plugins install git:langwatch/agent-plugin@5ca4f7addc97fd2bb8cfdfe3f086fc7c5407b88d --force
```

Mistral Vibe:

```text
git clone https://github.com/langwatch/agent-plugin && git -C agent-plugin checkout 5ca4f7addc97fd2bb8cfdfe3f086fc7c5407b88d
mkdir -p ~/.vibe/plugins/langwatch && cp -r agent-plugin/. ~/.vibe/plugins/langwatch
```
