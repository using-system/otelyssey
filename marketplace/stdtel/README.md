# stdtel

Telemetry for standards-as-skills: attributes token cost and policy outcomes to individual skills across Claude Code and GitHub Copilot.

- Category: `instrumentation`
- Repository: [amiable-dev/skills-telemetry](https://github.com/amiable-dev/skills-telemetry), the plugin at the root of it
- Version: 0.4.0 (`v0.4.0`, commit `a95d23afc261`)
- Author: [amiable-dev](https://github.com/amiable-dev)
- License: MIT
- Keywords: `telemetry`, `opentelemetry`, `skills`, `standards`, `governance`
- Homepage: <https://github.com/amiable-dev/skills-telemetry>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-19T21:29:18Z)
- Admitted from [issue #29](https://github.com/using-system/otelyssey/issues/29) on 2026-09-19

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
hermes plugins install amiable-dev/skills-telemetry --ref a95d23afc26150737a4eb6894b96a7235fa8f8da
hermes plugins enable stdtel
```

OpenClaw:

```text
openclaw plugins install git:amiable-dev/skills-telemetry@a95d23afc26150737a4eb6894b96a7235fa8f8da --force
```

Mistral Vibe:

```text
git clone https://github.com/amiable-dev/skills-telemetry && git -C skills-telemetry checkout a95d23afc26150737a4eb6894b96a7235fa8f8da
mkdir -p ~/.vibe/plugins/stdtel && cp -r skills-telemetry/. ~/.vibe/plugins/stdtel
```
