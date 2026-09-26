# sentry

Set up Sentry, debug production issues, and configure application monitoring.

- Repository: [getsentry/agent-plugin](https://github.com/getsentry/agent-plugin), the plugin at the root of it
- Categories: `backend`
- Version: 1.4.0 (`v1.4.0`, commit `3dfc0eab9afb`)
- Author: [Sentry](https://sentry.io)
- License: MIT
- Keywords: `sentry`, `debugging`, `monitoring`, `error-tracking`
- Homepage: <https://sentry.io>
- Stars 3, forks 0, watchers 0 (refreshed 2026-09-20T12:38:02Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install sentry@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install sentry@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add sentry@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install sentry --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install sentry@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/getsentry/agent-plugin`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install getsentry/agent-plugin --ref 3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5
hermes plugins enable sentry
```

OpenClaw:

```text
git clone https://github.com/getsentry/agent-plugin && git -C agent-plugin checkout 3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5
openclaw plugins install ./agent-plugin --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/getsentry/agent-plugin && git -C agent-plugin checkout 3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5
mkdir -p ~/.vibe/plugins/sentry && cp -r ./agent-plugin/. ~/.vibe/plugins/sentry
```

OpenCode:

```text
git clone https://github.com/getsentry/agent-plugin ~/.opencode-plugins/sentry && git -C ~/.opencode-plugins/sentry checkout 3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/sentry/skills"
    ]
  },
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp?utm_source=plugin"
    }
  }
}
```
