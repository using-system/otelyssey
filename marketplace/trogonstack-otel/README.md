# trogonstack-otel

OpenTelemetry skills for naming metrics and spans following OTel Semantic Conventions

- Repository: [TrogonStack/agentskills](https://github.com/TrogonStack/agentskills), the plugin at `plugins/trogonstack-otel` in it
- Categories: `instrumentation`
- Version: 0.2.0 (`main`, commit `8a6be53417e3`)
- Author: [TrogonStack](https://github.com/TrogonStack)
- License: MIT
- Keywords: `trogonstack`, `opentelemetry`, `observability`, `semantic-conventions`
- Homepage: <https://github.com/TrogonStack/agentskills/tree/main/plugins/trogonstack-otel>
- Stars 11, forks 3, watchers 0 (refreshed 2026-10-22T08:40:25Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install trogonstack-otel@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install trogonstack-otel@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add trogonstack-otel@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install trogonstack-otel --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install trogonstack-otel@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install TrogonStack/agentskills/plugins/trogonstack-otel --ref 8a6be53417e3f6b472e0919fa922a4514810c29a
hermes plugins enable trogonstack-otel
```

OpenClaw:

```text
git clone https://github.com/TrogonStack/agentskills && git -C agentskills checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
openclaw plugins install ./agentskills/plugins/trogonstack-otel --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/TrogonStack/agentskills && git -C agentskills checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
mkdir -p ~/.vibe/plugins/trogonstack-otel && cp -r ./agentskills/plugins/trogonstack-otel/. ~/.vibe/plugins/trogonstack-otel
```

OpenCode:

```text
git clone https://github.com/TrogonStack/agentskills ~/.opencode-plugins/trogonstack-otel && git -C ~/.opencode-plugins/trogonstack-otel checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/trogonstack-otel/plugins/trogonstack-otel/skills"
    ]
  }
}
```
