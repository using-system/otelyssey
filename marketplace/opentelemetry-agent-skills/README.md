# opentelemetry-agent-skills

Vendor-neutral OpenTelemetry skills for AI coding agents, grounded in upstream sources: SDK setup per language, the Collector and OCB, OTTL, declarative configuration, semantic conventions, upgrades and migrations.

- Repository: [ollygarden/opentelemetry-agent-skills](https://github.com/ollygarden/opentelemetry-agent-skills), the plugin at the root of it
- Categories: `instrumentation`, `collector`
- Version: 1.0.0 (`main`, commit `cbdb25cd88ef`)
- Author: [OllyGarden](https://github.com/ollygarden)
- License: Apache-2.0
- Keywords: `opentelemetry`, `otel`, `observability`, `collector`, `semantic-conventions`, `skills`
- Homepage: <https://github.com/ollygarden/opentelemetry-agent-skills>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-21T19:01:29Z)

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
hermes plugins install ollygarden/opentelemetry-agent-skills --ref cbdb25cd88ef66d086bc39fed8180b13bfb91e70
hermes plugins enable opentelemetry-agent-skills
```

OpenClaw:

```text
git clone https://github.com/ollygarden/opentelemetry-agent-skills && git -C opentelemetry-agent-skills checkout cbdb25cd88ef66d086bc39fed8180b13bfb91e70
openclaw plugins install ./opentelemetry-agent-skills --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/ollygarden/opentelemetry-agent-skills && git -C opentelemetry-agent-skills checkout cbdb25cd88ef66d086bc39fed8180b13bfb91e70
mkdir -p ~/.vibe/plugins/opentelemetry-agent-skills && cp -r ./opentelemetry-agent-skills/. ~/.vibe/plugins/opentelemetry-agent-skills
```
