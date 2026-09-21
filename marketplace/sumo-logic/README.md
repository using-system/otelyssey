# sumo-logic

Query Sumo Logic logs, alerts, dashboards, and SIEM insights directly from Copilot. Connects to the Sumo Logic MCP server for natural language observability investigations.

- Repository: [SumoLogic/sumologic-ai-plugins](https://github.com/SumoLogic/sumologic-ai-plugins), the plugin at the root of it
- Categories: `backend`
- Version: 1.0.1 (`v1.0.1`, commit `f905b914984f`)
- Author: [Sumo Logic](https://www.sumologic.com)
- License: Apache-2.0
- Keywords: `sumo-logic`, `observability`, `logs`, `mcp`, `monitoring`, `alerts`, `copilot`, `devops`, `search`, `security`
- Homepage: <https://www.sumologic.com/help/docs/api/mcp-server/>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-20T15:10:54Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install sumo-logic@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install sumo-logic@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add sumo-logic@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install sumo-logic --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install sumo-logic@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/SumoLogic/sumologic-ai-plugins`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install SumoLogic/sumologic-ai-plugins --ref f905b914984fabb5e0571290eafd3013c277d9b1
hermes plugins enable sumo-logic
```

OpenClaw:

```text
git clone https://github.com/SumoLogic/sumologic-ai-plugins && git -C sumologic-ai-plugins checkout f905b914984fabb5e0571290eafd3013c277d9b1
openclaw plugins install ./sumologic-ai-plugins --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/SumoLogic/sumologic-ai-plugins && git -C sumologic-ai-plugins checkout f905b914984fabb5e0571290eafd3013c277d9b1
mkdir -p ~/.vibe/plugins/sumo-logic && cp -r ./sumologic-ai-plugins/. ~/.vibe/plugins/sumo-logic
```
