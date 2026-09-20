# observability

Opinionated guidance for clear and operationally useful OpenTelemetry instrumentation: one language-agnostic skill on spans as operation records, named log events, attributes under the OpenTelemetry semantic conventions, and exception recording, for adding or reviewing instrumentation in any OpenTelemetry SDK.

- Category: `instrumentation`
- Repository: [BastiDood/skills](https://github.com/BastiDood/skills), the plugin at `plugins/observability` in it
- Version: 0.1.7 (`main`, commit `9dfab1713cb2`)
- Author: [Basti Ortiz](https://bastidood.dev/)
- License: MPL-2.0
- Keywords: `opentelemetry`, `instrumentation`, `semantic-conventions`, `spans`, `logs`, `best-practices`
- Homepage: <https://github.com/BastiDood/skills#readme>
- Stars 14, forks 0, watchers 0 (refreshed 2026-09-20T08:38:53Z)
- Admitted from [issue #57](https://github.com/using-system/otelyssey/issues/57) on 2026-09-20

## Install

Claude Code:

```text
claude plugin marketplace add using-system/otelyssey
claude plugin install observability@otelyssey
```

GitHub Copilot CLI:

```text
copilot plugin marketplace add using-system/otelyssey
copilot plugin install observability@otelyssey
```

Codex CLI:

```text
codex plugin marketplace add using-system/otelyssey
codex plugin add observability@otelyssey
```

APM:

```text
apm marketplace add using-system/otelyssey
apm install observability@otelyssey --target copilot
```

VS Code, in `settings.json`:

```json
"chat.plugins.marketplaces": ["using-system/otelyssey"]
```
