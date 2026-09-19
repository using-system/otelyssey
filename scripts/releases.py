"""Follow every admitted plugin's latest release: revalidate it, re-pin the record on a pass."""

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
    """Per record name: status unchanged, updated or failed; the tag looked at; the errors.

    With smoke_fn, a tag that validates is also installed on the hosts (the intake's smoke
    replayed on the checkout) and is re-pinned only when every host passes.
    """
    result: dict[str, dict] = {}
    for name, record in store.load_store(root).items():
        try:
            latest = gitrepo.latest_release(gitrepo.list_tags(record["repository"]))
        except gitrepo.RepositoryError as error:
            errors = [f"repository: tags unreadable ({error})"]
            result[name] = {"status": "failed", "tag": record["ref"], "errors": errors}
            continue
        if latest is None or latest[0] == record["ref"]:
            result[name] = {"status": "unchanged", "tag": record["ref"], "errors": []}
            continue
        tag, _ = latest
        check = validate.validate(
            record["repository"], tag, record["path"], name, "", workdir / name
        )
        if check["errors"]:
            result[name] = {"status": "failed", "tag": tag, "errors": check["errors"]}
            continue
        if smoke_fn is not None:
            checkout = workdir / name / "checkout"
            plugin_dir = checkout / record["path"] if record["path"] else checkout
            errors = _install_errors(smoke_fn(name, plugin_dir, workdir / name / "smoke"))
            if errors:
                result[name] = {"status": "failed", "tag": tag, "errors": errors}
                continue
        version = check["manifest"].get("version") or record["version"]
        store.write_record(root, {**record, "ref": tag, "sha": check["sha"], "version": version})
        result[name] = {"status": "updated", "tag": tag, "errors": []}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="follow the admitted plugins' releases")
    parser.add_argument("--root", default=".")
    parser.add_argument("--workdir", required=True)
    parser.add_argument(
        "--smoke", action="store_true", help="also install a newer tag on the hosts"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = follow(Path(args.root), Path(args.workdir), smoke.smoke if args.smoke else None)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, r in result.items():
            print(f"{name}: {r['status']} {r['tag']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
