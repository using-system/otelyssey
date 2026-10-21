# trogonstack-datadog

Datadog observability skills for designing, redesigning, and auditing dashboards with proper widget selection, layout patterns, template variables, and operational readiness validation using the pup CLI, and for checking metrics against Datadog's no-cost metrics before creating custom ones

- Repository: [TrogonStack/agentskills](https://github.com/TrogonStack/agentskills), the plugin at `plugins/trogonstack-datadog` in it
- Categories: `backend`, `instrumentation`
- Version: 0.5.0 (`main`, commit `8a6be53417e3`)
- Author: [TrogonStack](https://github.com/TrogonStack)
- License: MIT
- Keywords: `trogonstack`, `datadog`, `observability`, `dashboards`
- Homepage: <https://github.com/TrogonStack/agentskills/tree/main/plugins/trogonstack-datadog>
- Stars 0, forks 0, watchers 0 (refreshed 2026-10-21T19:17:30Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install trogonstack-datadog@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install trogonstack-datadog@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add trogonstack-datadog@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install trogonstack-datadog --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install trogonstack-datadog@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install TrogonStack/agentskills/plugins/trogonstack-datadog --ref 8a6be53417e3f6b472e0919fa922a4514810c29a
hermes plugins enable trogonstack-datadog
```

OpenClaw:

```text
git clone https://github.com/TrogonStack/agentskills && git -C agentskills checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
openclaw plugins install ./agentskills/plugins/trogonstack-datadog --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/TrogonStack/agentskills && git -C agentskills checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
mkdir -p ~/.vibe/plugins/trogonstack-datadog && cp -r ./agentskills/plugins/trogonstack-datadog/. ~/.vibe/plugins/trogonstack-datadog
```

OpenCode:

```text
git clone https://github.com/TrogonStack/agentskills ~/.opencode-plugins/trogonstack-datadog && git -C ~/.opencode-plugins/trogonstack-datadog checkout 8a6be53417e3f6b472e0919fa922a4514810c29a
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/trogonstack-datadog/plugins/trogonstack-datadog/skills"
    ]
  }
}
```
