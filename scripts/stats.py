"""Stars, forks and watchers of every admitted plugin's repository, from the GitHub API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from scripts import store

COUNTS = ("stars", "forks", "watchers")


def now() -> str:
    return dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def token_from_env() -> str | None:
    """GH_TOKEN, else GITHUB_TOKEN, else nothing (the API then answers at its anonymous rate)."""
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or None


def fetch_raw(repository: str, token: str | None) -> dict:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "otelyssey"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/repos/{repository}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def counts(raw: dict) -> dict:
    """stars, forks, watchers: watchers are the API's subscribers, not its legacy watchers_count."""
    return {
        "stars": int(raw["stargazers_count"]),
        "forks": int(raw["forks_count"]),
        "watchers": int(raw["subscribers_count"]),
    }


def refresh(root: Path, token: str | None) -> tuple[list[str], dict[str, str]]:
    """The names whose counts moved (rewritten), and the names the API refused, with the reason."""
    changed: list[str] = []
    failed: dict[str, str] = {}
    stamp = now()
    for name, record in store.load_store(root).items():
        try:
            new = counts(fetch_raw(record["repository"], token))
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as error:
            failed[name] = f"{record['repository']}: {error}"
            continue
        if any(new[key] != record["stats"][key] for key in COUNTS):
            store.write_record(root, {**record, "stats": {**new, "refreshed_at": stamp}})
            changed.append(name)
    return changed, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="refresh the repository statistics of the store")
    parser.add_argument("--root", default=".")
    parser.add_argument("--failures", default=None, help="write {name: reason} JSON there")
    args = parser.parse_args(argv)
    changed, failed = refresh(Path(args.root), token_from_env())
    for name in changed:
        print(f"refreshed: {name}")
    for name, reason in failed.items():
        print(f"failed: {name} ({reason})", file=sys.stderr)
    if not changed:
        print("no count moved")
    if args.failures:
        Path(args.failures).write_text(json.dumps(failed, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
