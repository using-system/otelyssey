# vllm-on-tap

Serve vLLM presets on demand - locally, Kubernetes (KServe), Azure (Container Apps), AWS (ECS) or GCP (Cloud Run) - with their traces over OTLP, and tear them down again.

- Repository: [using-system/vllm-on-tap](https://github.com/using-system/vllm-on-tap), the plugin at the root of it
- Categories: `instrumentation`
- Version: 0.2.0 (`v0.2.0`, commit `872726f4b552`)
- Author: [using-system](https://github.com/using-system)
- License: MIT
- Keywords: `vllm`, `inference`, `llm`, `azure`, `azure-container-apps`, `gpu`, `opentelemetry`
- Homepage: <https://github.com/using-system/vllm-on-tap#readme>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-26T18:04:58Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install vllm-on-tap@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install vllm-on-tap@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add vllm-on-tap@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install vllm-on-tap --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install vllm-on-tap@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/using-system/vllm-on-tap`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install using-system/vllm-on-tap --ref 872726f4b552cedf097bc4a2394597af61dd7131
hermes plugins enable vllm-on-tap
```

OpenClaw:

```text
git clone https://github.com/using-system/vllm-on-tap && git -C vllm-on-tap checkout 872726f4b552cedf097bc4a2394597af61dd7131
openclaw plugins install ./vllm-on-tap --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/using-system/vllm-on-tap && git -C vllm-on-tap checkout 872726f4b552cedf097bc4a2394597af61dd7131
mkdir -p ~/.vibe/plugins/vllm-on-tap && cp -r ./vllm-on-tap/. ~/.vibe/plugins/vllm-on-tap
```

OpenCode:

```text
git clone https://github.com/using-system/vllm-on-tap ~/.opencode-plugins/vllm-on-tap && git -C ~/.opencode-plugins/vllm-on-tap checkout 872726f4b552cedf097bc4a2394597af61dd7131
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/vllm-on-tap/skills"
    ]
  }
}
```
