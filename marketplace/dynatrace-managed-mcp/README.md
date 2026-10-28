# dynatrace-managed-mcp

MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters.

- Repository: [dynatrace-oss/dynatrace-managed-mcp](https://github.com/dynatrace-oss/dynatrace-managed-mcp), the plugin at the root of it
- Categories: `backend`
- Version: 2.0.0 (`v2.0.0`, commit `857cecf40383`)
- Author: [Dynatrace](https://www.dynatrace.com)
- License: Apache-2.0
- Keywords: `dynatrace`, `dynatrace-managed`, `mcp`, `observability`, `monitoring`, `apm`, `logs`, `metrics`, `slo`
- Homepage: <https://github.com/dynatrace-oss/dynatrace-managed-mcp#readme>
- Stars 33, forks 15, watchers 0 (refreshed 2026-10-27T09:04:13Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install dynatrace-managed-mcp@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install dynatrace-managed-mcp@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add dynatrace-managed-mcp@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install dynatrace-managed-mcp --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install dynatrace-managed-mcp@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/dynatrace-oss/dynatrace-managed-mcp`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install dynatrace-oss/dynatrace-managed-mcp --ref 857cecf40383335b90fffb8bf67c5b0dd2447a64
hermes plugins enable dynatrace-managed-mcp
```

OpenClaw:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp && git -C dynatrace-managed-mcp checkout 857cecf40383335b90fffb8bf67c5b0dd2447a64
openclaw plugins install ./dynatrace-managed-mcp --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp && git -C dynatrace-managed-mcp checkout 857cecf40383335b90fffb8bf67c5b0dd2447a64
mkdir -p ~/.vibe/plugins/dynatrace-managed-mcp && cp -r ./dynatrace-managed-mcp/. ~/.vibe/plugins/dynatrace-managed-mcp
```

OpenCode:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp ~/.opencode-plugins/dynatrace-managed-mcp && git -C ~/.opencode-plugins/dynatrace-managed-mcp checkout 857cecf40383335b90fffb8bf67c5b0dd2447a64
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/dynatrace-managed-mcp/skills"
    ]
  },
  "mcp": {
    "dynatrace-managed": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@dynatrace-oss/dynatrace-managed-mcp-server@<3"
      ],
      "environment": {
        "DT_ENVIRONMENT_CONFIGS": "{env:DT_ENVIRONMENT_CONFIGS}"
      }
    }
  }
}
```
