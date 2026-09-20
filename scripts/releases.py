"""Follow every admitted plugin's releases: a newer tag carrying the plugin, otherwise a new
manifest version on the default branch; revalidate it, re-pin the record on a pass."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path

from scripts import gitrepo, smoke, store, validate

SmokeFn = Callable[[str, Path, Path], dict[str, dict]]


def _install_errors(result: dict[str, dict]) -> list[str]:
    """One line per host whose install did not pass, ending with its output's last line."""
    errors = []
    for host, r in result.items():
        if r["status"] != "pass":
            last = (r["output"].strip().splitlines() or [""])[-1]
            errors.append(f"install on {host}: {r['status']}: {last}")
    return errors


def follow(root: Path, workdir: Path, smoke_fn: SmokeFn | None = None) -> dict[str, dict]:
    """Per record name: status unchanged, updated or failed; the ref looked at; the errors.

    A repository with a release tag carrying the plugin is followed by tag: a tag other than
    the record's is a release. Without one, the default branch is followed by manifest
    version: a head with the record's version, or none, is not a release, valid or not, and
    the record keeps its commit. A record on a tag whose plugin is at neither the latest tag
    nor the head is a failure: the plugin vanished.
    With smoke_fn, a release that validates is also installed on the hosts (the intake's
    smoke replayed on the checkout) and is re-pinned only when every host passes.
    """
    result: dict[str, dict] = {}
    for name, record in store.load_store(root).items():
        try:
            ref, sha, tagged = gitrepo.release(record["repository"], record["path"])
        except gitrepo.RepositoryError as error:
            errors = [f"repository: unreadable ({error})"]
            result[name] = {"status": "failed", "ref": record["ref"], "errors": errors}
            continue
        if ref == record["ref"] and (tagged or sha == record["sha"]):
            result[name] = {"status": "unchanged", "ref": ref, "errors": []}
            continue
        check = validate.validate(
            record["repository"], sha, record["path"], name, "", workdir / name
        )
        version = check["manifest"].get("version")
        if not tagged and version is None and record["ref"] != ref:
            # the record was on a tag, and the plugin is at neither the latest tag nor the head
            errors = ["plugin.json: at neither the latest release tag nor the default branch"]
            result[name] = {"status": "failed", "ref": ref, "errors": errors + check["errors"]}
            continue
        if not tagged and version in (record["version"], None):
            # the head moved without a release: a work-in-progress commit, valid or not
            result[name] = {"status": "unchanged", "ref": ref, "errors": []}
            continue
        if check["errors"]:
            result[name] = {"status": "failed", "ref": ref, "errors": check["errors"]}
            continue
        if smoke_fn is not None:
            checkout = workdir / name / "checkout"
            plugin_dir = checkout / record["path"] if record["path"] else checkout
            errors = _install_errors(smoke_fn(name, plugin_dir, workdir / name / "smoke"))
            if errors:
                result[name] = {"status": "failed", "ref": ref, "errors": errors}
                continue
        try:
            store.write_record(root, {**record, "ref": ref, "sha": sha, "version": version})
        except ValueError as error:
            result[name] = {"status": "failed", "ref": ref, "errors": [f"record: {error}"]}
            continue
        result[name] = {"status": "updated", "ref": ref, "errors": []}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="follow the admitted plugins' releases")
    parser.add_argument("--root", default=".")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--smoke", action="store_true", help="also install a release on the hosts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = follow(Path(args.root), Path(args.workdir), smoke.smoke if args.smoke else None)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, r in result.items():
            print(f"{name}: {r['status']} {r['ref']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
