# arize-phoenix

Connect to your Phoenix instance to debug, evaluate, and improve LLM applications.

- Repository: [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix), the plugin at `plugins/codex/arize-phoenix` in it
- Categories: `backend`
- Version: 0.1.0 (`main`, commit `767847c33864`)
- Author: [Arize AI](https://arize.com)
- License: Apache-2.0
- Keywords: `phoenix`, `arize`, `observability`, `tracing`, `evals`, `llm`, `mcp`
- Homepage: <https://arize.com/docs/phoenix>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-20T15:29:33Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install arize-phoenix@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install arize-phoenix@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add arize-phoenix@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install arize-phoenix --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install arize-phoenix@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install Arize-ai/phoenix/plugins/codex/arize-phoenix --ref 767847c3386492f9783b623cf78e3eee47d0cea3
hermes plugins enable arize-phoenix
```

OpenClaw:

```text
git clone https://github.com/Arize-ai/phoenix && git -C phoenix checkout 767847c3386492f9783b623cf78e3eee47d0cea3
openclaw plugins install ./phoenix/plugins/codex/arize-phoenix --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/Arize-ai/phoenix && git -C phoenix checkout 767847c3386492f9783b623cf78e3eee47d0cea3
mkdir -p ~/.vibe/plugins/arize-phoenix && cp -r ./phoenix/plugins/codex/arize-phoenix/. ~/.vibe/plugins/arize-phoenix
```
