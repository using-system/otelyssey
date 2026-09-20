"""The store: one JSON record per admitted plugin under .store/, the only source of truth."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CATEGORIES = ("instrumentation", "collector", "backend", "observability")
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
REPO_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9._-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
URL_RE = re.compile(r"^https://[^\s()<>\[\]]+$")  # no whitespace, no markdown link character
FIELDS = (
    "name",
    "description",
    "categories",
    "repository",
    "path",
    "ref",
    "sha",
    "version",
    "author",
    "license",
    "homepage",
    "keywords",
    "submitted_in",
    "admitted_at",
    "stats",
)
STATS = ("stars", "forks", "watchers", "refreshed_at")


def _is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _clean(value: str) -> bool:
    """No control character: a value that fits one key=value line and one page line."""
    return not any(ord(c) < 32 or c == "\x7f" for c in value)


def validate_record(record: dict) -> list[str]:
    """Every rule the record breaks, one line each, empty when it is valid."""
    errors = [f"{field}: missing" for field in FIELDS if field not in record]
    unknown = sorted(set(record) - set(FIELDS))
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")
    if errors:
        return errors
    if not isinstance(record["name"], str) or not NAME_RE.match(record["name"]):
        errors.append("name: not an Agent Plugins name (lowercase, digits, . and -)")
    if not isinstance(record["description"], str) or not record["description"].strip():
        errors.append("description: empty")
    categories = record["categories"]
    if (
        not isinstance(categories, list)
        or not categories
        or any(c not in CATEGORIES for c in categories)
        or len(set(categories)) != len(categories)
    ):
        errors.append(
            f"categories: a non-empty list of distinct values among {', '.join(CATEGORIES)}"
        )
    if not isinstance(record["repository"], str) or not REPO_RE.match(record["repository"]):
        errors.append("repository: not owner/repo")
    path = record["path"]
    if not isinstance(path, str) or path.startswith("/") or ".." in path:
        errors.append("path: not a relative directory inside the repository")
    if not _is_text(record["ref"]):
        errors.append("ref: empty")
    if not isinstance(record["sha"], str) or not SHA_RE.match(record["sha"]):
        errors.append("sha: not a 40-hex commit")
    if not _is_text(record["version"]):
        errors.append("version: empty")
    author = record["author"]
    if not isinstance(author, dict) or not _is_text(author.get("name")):
        errors.append("author: needs a name")
    elif set(author) - {"name", "email", "url"}:
        errors.append("author: only name, email, url")
    else:
        url, email = author.get("url"), author.get("email")
        if "url" in author and (not isinstance(url, str) or not URL_RE.match(url)):
            errors.append("author.url: not an https URL without spaces or ()<>[]")
        if "email" in author and (not _is_text(email) or any(c.isspace() for c in email)):
            errors.append("author.email: empty or carries whitespace")
    if not _is_text(record["license"]):
        errors.append("license: empty")
    if not isinstance(record["homepage"], str) or (
        record["homepage"] and not URL_RE.match(record["homepage"])
    ):
        errors.append("homepage: not an https URL without spaces or ()<>[] (empty allowed)")
    keywords = record["keywords"]
    if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
        errors.append("keywords: not a list of strings")
    if not isinstance(record["submitted_in"], int) or record["submitted_in"] <= 0:
        errors.append("submitted_in: not an issue number")
    if not isinstance(record["admitted_at"], str) or not DATE_RE.match(record["admitted_at"]):
        errors.append("admitted_at: not YYYY-MM-DD")
    stats = record["stats"]
    if not isinstance(stats, dict) or set(stats) != set(STATS):
        errors.append(f"stats: exactly {', '.join(STATS)}")
    else:
        for key in ("stars", "forks", "watchers"):
            if not isinstance(stats[key], int) or stats[key] < 0:
                errors.append(f"stats.{key}: not a count")
        if not isinstance(stats["refreshed_at"], str) or not STAMP_RE.match(stats["refreshed_at"]):
            errors.append("stats.refreshed_at: not an RFC3339 UTC stamp")
    texts = [(f, record[f]) for f in ("name", "description", "path", "ref", "version", "license")]
    texts.append(("homepage", record["homepage"]))
    if isinstance(keywords, list):
        texts.append(("keywords", "".join(k for k in keywords if isinstance(k, str))))
    if isinstance(author, dict):
        texts += [(f"author.{k}", v) for k, v in author.items() if k in ("name", "email", "url")]
    for field, value in texts:
        if isinstance(value, str) and not _clean(value):
            errors.append(f"{field}: control character")
    return errors


def canonical(record: dict) -> str:
    """The one serialization the store carries: field order fixed, 2-space indent, final newline."""
    ordered = {field: record[field] for field in FIELDS}
    ordered["stats"] = {key: record["stats"][key] for key in STATS}
    return json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"


def write_record(root: Path, record: dict) -> Path:
    errors = validate_record(record)
    if errors:
        raise ValueError("; ".join(errors))
    directory = root / ".store"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record['name']}.json"
    path.write_text(canonical(record), encoding="utf-8")
    return path


def load_store(root: Path) -> dict[str, dict]:
    """Every record, keyed and sorted by name. A file whose name and record disagree raises."""
    records: dict[str, dict] = {}
    for path in sorted((root / ".store").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if path.stem != record.get("name"):
            raise ValueError(f"{path.name}: file name and record name differ")
        records[record["name"]] = record
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="check, or rewrite in canonical form, the store")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate every record")
    mode.add_argument("--write", action="store_true", help="validate, then rewrite canonically")
    parser.add_argument("--root", default=".", help="the repository root")
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not (root / ".store").is_dir():
        print(f"{root / '.store'}: no such directory", file=sys.stderr)
        return 2
    paths = sorted((root / ".store").glob("*.json"))
    failures = 0
    for path in paths:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as error:
            print(f"{path.name}: not JSON ({error})", file=sys.stderr)
            failures += 1
            continue
        errors = validate_record(record)
        if not errors and path.stem != record["name"]:
            errors.append("file name and record name differ")
        for error in errors:
            print(f"{path.name}: {error}", file=sys.stderr)
        if errors:
            failures += 1
        elif args.write and path.read_text(encoding="utf-8") != canonical(record):
            write_record(root, record)
            print(f"{path.name}: rewritten in canonical form")
    print(f"{len(paths)} record(s), {failures} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
