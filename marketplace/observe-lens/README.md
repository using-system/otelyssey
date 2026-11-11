# observe-lens

Read-only investigation skills across CI pipelines (Jenkins, GitHub Actions), CD (Argo CD, Flux, Helm, Kubernetes), databases (PostgreSQL, MySQL, MongoDB) and telemetry (Grafana, Loki, Tempo, Prometheus).

- Repository: [evrentan/observe-lens](https://github.com/evrentan/observe-lens), the plugin at the root of it
- Categories: `observability`, `backend`
- Version: 1.1.0 (`v1.1.0`, commit `888ba18bf68f`)
- Author: [Evren Tan](https://github.com/evrentan)
- License: Apache-2.0
- Keywords: `observability`, `debugging`, `ci`, `cd`, `database`, `grafana`, `skills`
- Homepage: <https://github.com/evrentan/observe-lens>
- Stars 0, forks 0, watchers 0 (refreshed 2026-11-11T12:53:27Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install observe-lens@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install observe-lens@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add observe-lens@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install observe-lens --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install observe-lens@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/evrentan/observe-lens`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install evrentan/observe-lens --ref 888ba18bf68f85247218d347e705b74fea29a636
hermes plugins enable observe-lens
```

OpenClaw:

```text
git clone https://github.com/evrentan/observe-lens && git -C observe-lens checkout 888ba18bf68f85247218d347e705b74fea29a636
openclaw plugins install ./observe-lens --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/evrentan/observe-lens && git -C observe-lens checkout 888ba18bf68f85247218d347e705b74fea29a636
mkdir -p ~/.vibe/plugins/observe-lens && cp -r ./observe-lens/. ~/.vibe/plugins/observe-lens
```

OpenCode:

```text
git clone https://github.com/evrentan/observe-lens ~/.opencode-plugins/observe-lens && git -C ~/.opencode-plugins/observe-lens checkout 888ba18bf68f85247218d347e705b74fea29a636
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/observe-lens/skills"
    ]
  }
}
```
