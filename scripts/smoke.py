"""Install a plugin on the hosts from an ephemeral marketplace, under an isolated HOME."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOSTS = ("copilot", "claude", "codex")
MARKETPLACE = "otelyssey-intake"
# Codex installs with `plugin add`, the other hosts with `plugin install`
INSTALL_VERB = {"codex": "add"}


def ephemeral_marketplace(workdir: Path, name: str, plugin_dir: Path) -> Path:
    """A marketplace directory whose one plugin is a copy of the checked-out plugin."""
    market = workdir / "market"
    if market.exists():
        shutil.rmtree(market)
    shutil.copytree(plugin_dir, market / "plugin", symlinks=True)
    (market / ".claude-plugin").mkdir(parents=True)
    manifest = {
        "name": MARKETPLACE,
        "owner": {"name": "otelyssey"},
        "plugins": [{"name": name, "source": "./plugin"}],
    }
    text = json.dumps(manifest, indent=2) + "\n"
    # the layout the marketplace ships: at the root for Copilot CLI, in .claude-plugin/ for
    # Claude Code, and Codex's own catalog in .agents/plugins/ with a local source
    (market / "marketplace.json").write_text(text)
    (market / ".claude-plugin" / "marketplace.json").write_text(text)
    codex = {
        "name": MARKETPLACE,
        "interface": {"displayName": MARKETPLACE},
        "plugins": [{"name": name, "source": {"source": "local", "path": "./plugin"}}],
    }
    (market / ".agents" / "plugins").mkdir(parents=True)
    (market / ".agents" / "plugins" / "marketplace.json").write_text(
        json.dumps(codex, indent=2) + "\n"
    )
    return market


def _run(args: list[str], home: Path) -> tuple[int, str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_CACHE_HOME": str(home / ".cache"),
        "XDG_DATA_HOME": str(home / ".local" / "share"),
        "CODEX_HOME": str(home / ".codex"),
        "CI": "1",
    }
    try:
        proc = subprocess.run(args, capture_output=True, text=True, env=env, timeout=300, cwd=home)
    except subprocess.TimeoutExpired:
        return 124, f"{' '.join(args)}: timed out after 300 s"
    return proc.returncode, (proc.stdout + proc.stderr)[-4000:]


def install(host: str, marketplace_dir: Path, name: str, home: Path) -> tuple[str, str]:
    """pass, fail or unavailable (the host CLI is not on this machine), with the output.

    The HOME is recreated so a reused workdir never carries a previous registration.
    """
    if shutil.which(host) is None:
        return "unavailable", f"the {host} CLI is not on this machine"
    shutil.rmtree(home, ignore_errors=True)
    # Codex refuses a CODEX_HOME that does not exist
    (home / ".codex").mkdir(parents=True, exist_ok=True)
    code, out = _run([host, "plugin", "marketplace", "add", str(marketplace_dir)], home)
    if code != 0:
        return "fail", f"marketplace add exited {code}\n{out}"
    verb = INSTALL_VERB.get(host, "install")
    code, out = _run([host, "plugin", verb, f"{name}@{MARKETPLACE}"], home)
    if code != 0:
        return "fail", f"plugin {verb} exited {code}\n{out}"
    code, listed = _run([host, "plugin", "list"], home)
    if code != 0 or name not in listed:
        return "fail", f"plugin list does not carry {name}\n{listed}"
    return "pass", f"{host}: installed and listed {name}"


def smoke(
    name: str, plugin_dir: Path, workdir: Path, hosts: tuple[str, ...] = HOSTS
) -> dict[str, dict]:
    """The workdir is made absolute: the hosts run with the isolated HOME as cwd."""
    workdir = workdir.resolve()
    market = ephemeral_marketplace(workdir, name, plugin_dir)
    result: dict[str, dict] = {}
    for host in hosts:
        status, output = install(host, market, name, workdir / f"home-{host}")
        result[host] = {"status": status, "output": output}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="install a plugin on the hosts")
    parser.add_argument("--name", required=True)
    parser.add_argument("--plugin-dir", required=True)
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--hosts", default=",".join(HOSTS))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    hosts = tuple(args.hosts.split(","))
    result = smoke(args.name, Path(args.plugin_dir), Path(args.workdir), hosts)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for host, r in result.items():
            print(f"{host}: {r['status']}")
    statuses = {r["status"] for r in result.values()}
    if "fail" in statuses:
        return 1
    if "unavailable" in statuses:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
