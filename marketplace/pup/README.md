# pup

Datadog API CLI with 49 command groups, 300+ subcommands. Skills and domain agents for monitoring, logs, APM, security, and infrastructure.

- Repository: [DataDog/pup](https://github.com/DataDog/pup), the plugin at the root of it
- Categories: `backend`
- Version: 1.23.0 (`v1.23.0`, commit `4c0d8720d94f`)
- Author: Datadog
- License: Apache-2.0
- Keywords: `datadog`, `monitoring`, `logs`, `apm`, `metrics`, `security`, `infrastructure`
- Homepage: <https://github.com/DataDog/pup#readme>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-21T19:18:23Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install pup@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install pup@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add pup@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install pup --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install pup@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/DataDog/pup`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install DataDog/pup --ref 4c0d8720d94f787dc70b4c1672fa8ee4872811ad
hermes plugins enable pup
```

OpenClaw:

```text
git clone https://github.com/DataDog/pup && git -C pup checkout 4c0d8720d94f787dc70b4c1672fa8ee4872811ad
openclaw plugins install ./pup --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/DataDog/pup && git -C pup checkout 4c0d8720d94f787dc70b4c1672fa8ee4872811ad
mkdir -p ~/.vibe/plugins/pup && cp -r ./pup/. ~/.vibe/plugins/pup
```
