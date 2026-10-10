# save-toolkit

Application-engineering and site-reliability agents and reusable skills.

- Repository: [latent-sre/save-toolkit](https://github.com/latent-sre/save-toolkit), the plugin at the root of it
- Categories: `observability`, `backend`, `instrumentation`, `collector`
- Version: 0.51.1 (`main`, commit `34634c25179c`)
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
hermes plugins install latent-sre/save-toolkit --ref 34634c25179c71a3965df29eebf7332cc277cc67
hermes plugins enable save-toolkit
```

OpenClaw:

```text
git clone https://github.com/latent-sre/save-toolkit && git -C save-toolkit checkout 34634c25179c71a3965df29eebf7332cc277cc67
openclaw plugins install ./save-toolkit --force --accept-capabilities
```

Mistral Vibe:

```text
git clone https://github.com/latent-sre/save-toolkit && git -C save-toolkit checkout 34634c25179c71a3965df29eebf7332cc277cc67
mkdir -p ~/.vibe/plugins/save-toolkit && cp -r ./save-toolkit/. ~/.vibe/plugins/save-toolkit
```

OpenCode:

```text
git clone https://github.com/latent-sre/save-toolkit ~/.opencode-plugins/save-toolkit && git -C ~/.opencode-plugins/save-toolkit checkout 34634c25179c71a3965df29eebf7332cc277cc67
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
