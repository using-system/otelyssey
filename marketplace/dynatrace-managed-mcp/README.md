# dynatrace-managed-mcp

MCP server for Dynatrace Managed (self-hosted): query logs, metrics, events, entities, problems, security vulnerabilities and SLOs across one or more clusters.

- Repository: [dynatrace-oss/dynatrace-managed-mcp](https://github.com/dynatrace-oss/dynatrace-managed-mcp), the plugin at the root of it
- Categories: `backend`
- Version: 1.1.1 (`main`, commit `52959ebce94e`)
- Author: [Dynatrace](https://www.dynatrace.com)
- License: Apache-2.0
- Keywords: `dynatrace`, `dynatrace-managed`, `mcp`, `observability`, `monitoring`, `apm`, `logs`, `metrics`, `slo`
- Homepage: <https://github.com/dynatrace-oss/dynatrace-managed-mcp#readme>
- Stars 31, forks 12, watchers 0 (refreshed 2026-09-25T08:52:49Z)

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
hermes plugins install dynatrace-oss/dynatrace-managed-mcp --ref 52959ebce94eb5e814f2cf807f8208edf3ee4ca0
hermes plugins enable dynatrace-managed-mcp
```

OpenClaw:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp && git -C dynatrace-managed-mcp checkout 52959ebce94eb5e814f2cf807f8208edf3ee4ca0
openclaw plugins install ./dynatrace-managed-mcp --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp && git -C dynatrace-managed-mcp checkout 52959ebce94eb5e814f2cf807f8208edf3ee4ca0
mkdir -p ~/.vibe/plugins/dynatrace-managed-mcp && cp -r ./dynatrace-managed-mcp/. ~/.vibe/plugins/dynatrace-managed-mcp
```

OpenCode:

```text
git clone https://github.com/dynatrace-oss/dynatrace-managed-mcp ~/.opencode-plugins/dynatrace-managed-mcp && git -C ~/.opencode-plugins/dynatrace-managed-mcp checkout 52959ebce94eb5e814f2cf807f8208edf3ee4ca0
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
        "@dynatrace-oss/dynatrace-managed-mcp-server@<2"
      ],
      "environment": {
        "DT_ENVIRONMENT_CONFIGS": "{env:DT_ENVIRONMENT_CONFIGS}"
      }
    }
  }
}
```
