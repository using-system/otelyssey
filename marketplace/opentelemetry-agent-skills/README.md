# opentelemetry-agent-skills

Vendor-neutral OpenTelemetry skills for AI coding agents, grounded in upstream sources: SDK setup per language, the Collector and OCB, OTTL, declarative configuration, semantic conventions, upgrades and migrations.

- Repository: [ollygarden/opentelemetry-agent-skills](https://github.com/ollygarden/opentelemetry-agent-skills), the plugin at the root of it
- Categories: `instrumentation`, `collector`
- Version: 1.0.0 (`v1.0.0`, commit `ea1a9401c449`)
- Author: [OllyGarden](https://github.com/ollygarden)
- License: Apache-2.0
- Keywords: `opentelemetry`, `otel`, `observability`, `collector`, `semantic-conventions`, `skills`
- Homepage: <https://github.com/ollygarden/opentelemetry-agent-skills>
- Stars 104, forks 12, watchers 3 (refreshed 2026-10-03T09:12:44Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install opentelemetry-agent-skills@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install opentelemetry-agent-skills@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add opentelemetry-agent-skills@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install opentelemetry-agent-skills --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install opentelemetry-agent-skills@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/ollygarden/opentelemetry-agent-skills`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install ollygarden/opentelemetry-agent-skills --ref ea1a9401c449a43e319a634030bea66390173dff
hermes plugins enable opentelemetry-agent-skills
```

OpenClaw:

```text
git clone https://github.com/ollygarden/opentelemetry-agent-skills && git -C opentelemetry-agent-skills checkout ea1a9401c449a43e319a634030bea66390173dff
openclaw plugins install ./opentelemetry-agent-skills --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/ollygarden/opentelemetry-agent-skills && git -C opentelemetry-agent-skills checkout ea1a9401c449a43e319a634030bea66390173dff
mkdir -p ~/.vibe/plugins/opentelemetry-agent-skills && cp -r ./opentelemetry-agent-skills/. ~/.vibe/plugins/opentelemetry-agent-skills
```

OpenCode:

```text
git clone https://github.com/ollygarden/opentelemetry-agent-skills ~/.opencode-plugins/opentelemetry-agent-skills && git -C ~/.opencode-plugins/opentelemetry-agent-skills checkout ea1a9401c449a43e319a634030bea66390173dff
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/opentelemetry-agent-skills/skills"
    ]
  }
}
```
