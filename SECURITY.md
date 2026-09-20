# Security Policy

## Supported versions

`main` is the marketplace; there is no other version. Fixes land on
`main` and reach every client at its next read of the catalogs.

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use
GitHub's private vulnerability reporting:
[Report a vulnerability](https://github.com/using-system/otelyssey/security/advisories/new).

You can expect an acknowledgement within a few days.

## Scope

- The pipeline: the intake, review, admission and nightly workflows,
  the scripts they run, the GitHub App and its token, the agentic
  workflows' bounds.
- The generated artifacts: the catalogs the clients read
  (`marketplace.json`, `.claude-plugin/`, `.agents/plugins/`,
  `.grok-plugin/`, `hermes-pack.yaml`) and the pages under
  `marketplace/`.
- The smoke: the hosts' own install of a submitted plugin under an
  isolated HOME on the runner.

A vulnerability in a **listed plugin** belongs to that plugin's
repository: the marketplace pins a commit and installs what the hosts
install, it does not audit the plugin's code. A plugin whose repository
is compromised can be withdrawn: report it here, privately, and the
record is deleted.
