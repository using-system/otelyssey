# sentry

Set up Sentry, debug production issues, and configure application monitoring: skills to debug an issue, fix stack traces, create alerts and set up releases, with the Sentry MCP server; Sentry ingests OpenTelemetry natively over OTLP.

- Category: `backend`
- Repository: [getsentry/agent-plugin](https://github.com/getsentry/agent-plugin), the plugin at the root of it
- Version: 1.4.0 (`v1.4.0`, commit `3dfc0eab9afb`)
- Author: [Sentry](https://sentry.io)
- License: MIT
- Keywords: `sentry`, `debugging`, `monitoring`, `error-tracking`, `opentelemetry`
- Homepage: <https://sentry.io>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-20T10:40:30Z)
- Admitted from [issue #75](https://github.com/using-system/otelyssey/issues/75) on 2026-09-20

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
openclaw plugins install git:getsentry/agent-plugin@3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5 --force
```

Mistral Vibe:

```text
git clone https://github.com/getsentry/agent-plugin && git -C agent-plugin checkout 3dfc0eab9afb9fc649c10db1e3e247bbcd0f7be5
mkdir -p ~/.vibe/plugins/sentry && cp -r agent-plugin/. ~/.vibe/plugins/sentry
```
