# otelyssey

A marketplace of OpenTelemetry agent plugins in the
[Agent Plugins](https://agent-plugins.org/) format, run by the repository
itself: a contributor submits a plugin once, through an issue, and the
repository validates it, admits it, follows its releases and lists it.

Add the marketplace, then install a plugin, from a shell:

```text
claude plugin marketplace add using-system/otelyssey
copilot plugin marketplace add using-system/otelyssey
```

## Plugins

<!-- otelyssey:table -->
| Plugin | Description | Category | Repository | Stars | Forks | Watchers |
| --- | --- | --- | --- | ---: | ---: | ---: |
<!-- /otelyssey:table -->

## Submit a plugin

Open a [plugin submission](https://github.com/using-system/otelyssey/issues/new?template=submit-plugin.yml):
a public GitHub repository holding a `plugin.json` in the Agent Plugins
format, a release tag, and a subject that is OpenTelemetry. The
repository checks the format, installs the plugin, judges its relevance
and its novelty, talks to you on the issue, and lists it. Every night it
follows your releases and refreshes your repository's statistics.

The design is in
[docs/superpowers/specs/2026-09-19-otelyssey-design.md](docs/superpowers/specs/2026-09-19-otelyssey-design.md).
