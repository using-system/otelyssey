"""Follow every admitted plugin's latest release: revalidate it, re-pin the record on a pass."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts import gitrepo, store, validate


def follow(root: Path, workdir: Path) -> dict[str, dict]:
    """Per record name: status unchanged, updated or failed; the tag looked at; the errors."""
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
        version = check["manifest"].get("version") or record["version"]
        store.write_record(root, {**record, "ref": tag, "sha": check["sha"], "version": version})
        result[name] = {"status": "updated", "tag": tag, "errors": []}
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="follow the admitted plugins' releases")
    parser.add_argument("--root", default=".")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = follow(Path(args.root), Path(args.workdir))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, r in result.items():
            print(f"{name}: {r['status']} {r['tag']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
