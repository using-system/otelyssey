# observability

Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation.

- Repository: [BastiDood/skills](https://github.com/BastiDood/skills), the plugin at `plugins/observability` in it
- Categories: `instrumentation`
- Version: 0.2.3 (`main`, commit `a0999a9beb0c`)
- Author: [Basti Ortiz](https://bastidood.dev/)
- License: MPL-2.0
- Keywords: `claude`, `codex`, `cursor`, `skills`
- Stars 15, forks 0, watchers 0 (refreshed 2026-11-12T11:21:19Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install observability@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install observability@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add observability@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install observability --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install observability@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install BastiDood/skills/plugins/observability --ref a0999a9beb0ca5faada8e3d92382df2cfe1dedcb
hermes plugins enable observability
```

OpenClaw:

```text
git clone https://github.com/BastiDood/skills && git -C skills checkout a0999a9beb0ca5faada8e3d92382df2cfe1dedcb
openclaw plugins install ./skills/plugins/observability --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/BastiDood/skills && git -C skills checkout a0999a9beb0ca5faada8e3d92382df2cfe1dedcb
mkdir -p ~/.vibe/plugins/observability && cp -r ./skills/plugins/observability/. ~/.vibe/plugins/observability
```

OpenCode:

```text
git clone https://github.com/BastiDood/skills ~/.opencode-plugins/observability && git -C ~/.opencode-plugins/observability checkout a0999a9beb0ca5faada8e3d92382df2cfe1dedcb
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/observability/plugins/observability/skills"
    ]
  }
}
```
