"""Read every record's derived fields again from its manifest at its sha, one shot.

The records admitted from the old form carry values the contributor typed; with the
manifest as the source (derive.py), this rewrites description, license, homepage, author
and keywords from the manifest at the record's sha and the repository's metadata. What the
record pins and what the pipeline decided are untouched.
"""

from __future__ import annotations

import argparse
import http.client
import sys
from pathlib import Path

from scripts import derive, stats, store, validate


def resync_store(root: Path, workdir: Path, token: str | None) -> tuple[list[str], dict[str, str]]:
    """The names rewritten, and the names left as they were with the reason."""
    changed: list[str] = []
    skipped: dict[str, str] = {}
    for name, record in store.load_store(root).items():
        check = validate.validate(
            record["repository"],
            record["sha"],
            record["path"],
            name,
            record["version"],
            workdir / name,
        )
        if check["errors"]:
            skipped[name] = "; ".join(check["errors"])
            continue
        try:
            meta = derive.fetch_metadata(record["repository"], token)
        except (OSError, http.client.HTTPException, ValueError) as error:
            skipped[name] = f"metadata unreadable ({error})"
            continue
        updated, kept = derive.resync(record, check["manifest"], meta)
        if kept:
            skipped[name] = "; ".join(kept)
        if updated != record:
            store.write_record(root, updated)
            changed.append(name)
    return changed, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="resync the store's derived fields from the manifests"
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args(argv)
    changed, skipped = resync_store(Path(args.root), Path(args.workdir), stats.token_from_env())
    for name in changed:
        print(f"rewritten: {name}")
    for name, reason in skipped.items():
        print(f"kept: {name} ({reason})", file=sys.stderr)
    if not changed:
        print("nothing to rewrite")
    return 0


if __name__ == "__main__":
    sys.exit(main())
