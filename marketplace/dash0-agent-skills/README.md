# dash0-agent-skills

OpenTelemetry skills and reference documentation for AI coding assistants

- Repository: [dash0hq/agent-skills](https://github.com/dash0hq/agent-skills), the plugin at the root of it
- Categories: `instrumentation`, `collector`
- Version: 1.4.0 (`v1.4.0`, commit `46b52b9212d7`)
- Author: Dash0
- License: Apache-2.0
- Keywords: `otel`, `opentelemetry`, `observability`, `o11y`, `instrumentation`, `monitoring`, `ai-agent`, `skills`, `agentic`, `engineering`, `developer`, `coding`, `productivity`
- Homepage: <https://github.com/dash0hq/agent-skills>
- Stars 102, forks 16, watchers 0 (refreshed 2026-11-13T11:05:08Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install dash0-agent-skills@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install dash0-agent-skills@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add dash0-agent-skills@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install dash0-agent-skills --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install dash0-agent-skills@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/dash0hq/agent-skills`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install dash0hq/agent-skills --ref 46b52b9212d799f02f45faa83af6b041b2aef38b
hermes plugins enable dash0-agent-skills
```

OpenClaw:

```text
git clone https://github.com/dash0hq/agent-skills && git -C agent-skills checkout 46b52b9212d799f02f45faa83af6b041b2aef38b
openclaw plugins install ./agent-skills --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/dash0hq/agent-skills && git -C agent-skills checkout 46b52b9212d799f02f45faa83af6b041b2aef38b
mkdir -p ~/.vibe/plugins/dash0-agent-skills && cp -r ./agent-skills/. ~/.vibe/plugins/dash0-agent-skills
```

OpenCode:

```text
git clone https://github.com/dash0hq/agent-skills ~/.opencode-plugins/dash0-agent-skills && git -C ~/.opencode-plugins/dash0-agent-skills checkout 46b52b9212d799f02f45faa83af6b041b2aef38b
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/dash0-agent-skills/skills"
    ]
  }
}
```
