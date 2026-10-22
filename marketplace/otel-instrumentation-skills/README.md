# otel-instrumentation-skills

OpenTelemetry signal quality with durable workflows and fresh, version-correct upstream evidence.

- Repository: [rknightion/otel-instrumentation-skills](https://github.com/rknightion/otel-instrumentation-skills), the plugin at `plugins/otel-instrumentation-skills` in it
- Categories: `instrumentation`, `collector`
- Version: 2.0.0 (`main`, commit `d007ea95f1c1`)
- Author: Rob Knight
- License: Apache-2.0
- Keywords: `opentelemetry`, `instrumentation`, `collector`, `semantic-conventions`
- Stars 1, forks 0, watchers 0 (refreshed 2026-10-22T08:40:25Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install otel-instrumentation-skills@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install otel-instrumentation-skills@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add otel-instrumentation-skills@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install otel-instrumentation-skills --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install otel-instrumentation-skills@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install rknightion/otel-instrumentation-skills/plugins/otel-instrumentation-skills --ref d007ea95f1c17684345239da92e6d42e0f393d08
hermes plugins enable otel-instrumentation-skills
```

OpenClaw:

```text
git clone https://github.com/rknightion/otel-instrumentation-skills && git -C otel-instrumentation-skills checkout d007ea95f1c17684345239da92e6d42e0f393d08
openclaw plugins install ./otel-instrumentation-skills/plugins/otel-instrumentation-skills --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/rknightion/otel-instrumentation-skills && git -C otel-instrumentation-skills checkout d007ea95f1c17684345239da92e6d42e0f393d08
mkdir -p ~/.vibe/plugins/otel-instrumentation-skills && cp -r ./otel-instrumentation-skills/plugins/otel-instrumentation-skills/. ~/.vibe/plugins/otel-instrumentation-skills
```

OpenCode:

```text
git clone https://github.com/rknightion/otel-instrumentation-skills ~/.opencode-plugins/otel-instrumentation-skills && git -C ~/.opencode-plugins/otel-instrumentation-skills checkout d007ea95f1c17684345239da92e6d42e0f393d08
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/otel-instrumentation-skills/plugins/otel-instrumentation-skills/skills"
    ]
  }
}
```
