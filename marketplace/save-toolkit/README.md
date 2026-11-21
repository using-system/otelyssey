# save-toolkit

Application-engineering and site-reliability agents and reusable skills.

- Repository: [latent-sre/save-toolkit](https://github.com/latent-sre/save-toolkit), the plugin at the root of it
- Categories: `observability`, `backend`, `instrumentation`, `collector`
- Version: 0.52.11 (`main`, commit `c7f0a315c4d9`)
- Author: [latent-sre](https://github.com/latent-sre)
- License: MIT
- Keywords: `agents`, `skills`, `sre`, `observability`, `pcf`
- Homepage: <https://github.com/latent-sre/save-toolkit>
- Stars 0, forks 0, watchers 0 (refreshed 2026-09-26T13:06:21Z)

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install save-toolkit@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install save-toolkit@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add save-toolkit@otelyssey
```

Grok Build:

```text
grok plugin marketplace add using-system/otelyssey
grok plugin install save-toolkit --trust
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install save-toolkit@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```

Kiro: Import power from GitHub, `https://github.com/latent-sre/save-toolkit`.

Hermes Agent:

```text
hermes plugins pack install https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml
hermes plugins install latent-sre/save-toolkit --ref c7f0a315c4d9aa0b0e33baf185f30ea1f31a1fb5
hermes plugins enable save-toolkit
```

OpenClaw:

```text
git clone https://github.com/latent-sre/save-toolkit && git -C save-toolkit checkout c7f0a315c4d9aa0b0e33baf185f30ea1f31a1fb5
openclaw plugins install ./save-toolkit --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/latent-sre/save-toolkit && git -C save-toolkit checkout c7f0a315c4d9aa0b0e33baf185f30ea1f31a1fb5
mkdir -p ~/.vibe/plugins/save-toolkit && cp -r ./save-toolkit/. ~/.vibe/plugins/save-toolkit
```

OpenCode:

```text
git clone https://github.com/latent-sre/save-toolkit ~/.opencode-plugins/save-toolkit && git -C ~/.opencode-plugins/save-toolkit checkout c7f0a315c4d9aa0b0e33baf185f30ea1f31a1fb5
```

Then merge into `~/.config/opencode/opencode.json`:

```json
{
  "skills": {
    "paths": [
      "~/.opencode-plugins/save-toolkit/skills"
    ]
  }
}
```
