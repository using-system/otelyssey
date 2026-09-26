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
import tempfile
from pathlib import Path

from scripts import derive, stats, store, validate


def resync_store(
    root: Path, workdir: Path, token: str | None
) -> tuple[list[str], dict[str, list[str]], dict[str, str]]:
    """The names rewritten, the fields each record kept for want of a source, and the names
    left untouched with the reason."""
    rewritten: list[str] = []
    kept: dict[str, list[str]] = {}
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
        updated, missing = derive.resync(record, check, meta)
        if missing:
            kept[name] = [e.removeprefix(derive.MISSING).split(",", 1)[0] for e in missing]
        if updated == record:
            continue
        try:
            store.write_record(root, updated)
        except ValueError as error:
            # the manifest's values break a rule of the store: the record stays as it was
            skipped[name] = f"refused by the store ({error})"
            continue
        rewritten.append(name)
    return rewritten, kept, skipped


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="resync the store's derived fields from the manifests"
    )
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--workdir", default=None, help="an empty directory; a fresh one by default"
    )
    args = parser.parse_args(argv)
    workdir = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="otelyssey-"))
    rewritten, kept, skipped = resync_store(Path(args.root), workdir, stats.token_from_env())
    for name in rewritten:
        print(f"rewritten: {name}")
    for name, fields in kept.items():
        print(f"kept: {name}: {', '.join(fields)}", file=sys.stderr)
    for name, reason in skipped.items():
        print(f"skipped: {name} ({reason})", file=sys.stderr)
    if not rewritten:
        print("nothing to rewrite")
    # something the pipeline could not derive, or a record it could not rewrite: a failed check
    return 1 if kept or skipped else 0


if __name__ == "__main__":
    sys.exit(main())
