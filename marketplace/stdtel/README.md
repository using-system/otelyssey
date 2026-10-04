# stdtel

Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot.

- Repository: [amiable-dev/skills-telemetry](https://github.com/amiable-dev/skills-telemetry), the plugin at the root of it
- Categories: `instrumentation`, `backend`
- Version: 0.9.1 (`v0.9.1`, commit `c33a407d7ce6`)
- Author: [amiable-dev](https://github.com/amiable-dev)
- License: MIT
- Keywords: `telemetry`, `opentelemetry`, `skills`, `standards`, `governance`
- Homepage: <https://github.com/amiable-dev/skills-telemetry>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-19T21:29:18Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install stdtel@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install stdtel@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add stdtel@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install stdtel --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install stdtel@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/amiable-dev/skills-telemetry`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install amiable-dev/skills-telemetry --ref c33a407d7ce6d3e686718ccc5a5df5f269f0b9d5
hermes plugins enable stdtel
```

OpenClaw:

```text
git clone https://github.com/amiable-dev/skills-telemetry && git -C skills-telemetry checkout c33a407d7ce6d3e686718ccc5a5df5f269f0b9d5
openclaw plugins install ./skills-telemetry --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/amiable-dev/skills-telemetry && git -C skills-telemetry checkout c33a407d7ce6d3e686718ccc5a5df5f269f0b9d5
mkdir -p ~/.vibe/plugins/stdtel && cp -r ./skills-telemetry/. ~/.vibe/plugins/stdtel
```

OpenCode:

```text
git clone https://github.com/amiable-dev/skills-telemetry ~/.opencode-plugins/stdtel && git -C ~/.opencode-plugins/stdtel checkout c33a407d7ce6d3e686718ccc5a5df5f269f0b9d5
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/stdtel/skills"
    ]
  }
}
```
