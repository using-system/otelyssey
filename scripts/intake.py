"""Turn a submission issue's body (the rendered issue form) into a candidate record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from scripts import store

LABELS = (
    "Plugin name",
    "Description",
    "GitHub repository",
    "Path inside the repository",
    "Release tag",
    "Version",
    "License",
    "Author name",
    "Author URL",
    "Homepage",
    "Keywords",
    "Category",
)
EMPTY = "_No response_"
URL_RE = re.compile(r"^https://\S+$")
TAG_RE = re.compile(r"^v?\d+\.\d+\.\d+$")


def parse_form(body: str) -> dict[str, str]:
    """`### Label` sections to their trimmed value; GitHub's `_No response_` is an empty value."""
    fields: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("### "):
            if current is not None:
                fields[current] = "\n".join(lines).strip()
            current = line[4:].strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        fields[current] = "\n".join(lines).strip()
    return {k: ("" if v == EMPTY else v) for k, v in fields.items()}


def candidate(fields: dict[str, str], issue_number: int) -> tuple[dict, list[str]]:
    """The record the form describes (without sha, version, admitted_at, stats) and its errors."""
    errors = [f"{label}: section missing from the form" for label in LABELS if label not in fields]
    if errors:
        return {}, errors
    for label in LABELS:
        if "-->" in fields[label]:
            errors.append(f"{label}: must not contain -->")
    author = {"name": fields["Author name"].strip()}
    if fields["Author URL"].strip():
        author["url"] = fields["Author URL"].strip()
    record = {
        "name": fields["Plugin name"].strip(),
        "description": " ".join(fields["Description"].split()),
        "category": fields["Category"].strip(),
        "repository": fields["GitHub repository"].strip(),
        "path": fields["Path inside the repository"].strip().strip("/"),
        "ref": fields["Release tag"].strip(),
        "author": author,
        "license": fields["License"].strip(),
        "homepage": fields["Homepage"].strip(),
        "keywords": [k.strip().lower() for k in fields["Keywords"].split(",") if k.strip()],
        "submitted_in": issue_number,
        "submitted_version": fields["Version"].strip(),
    }
    if not store.NAME_RE.match(record["name"]):
        errors.append(
            "Plugin name: lowercase letters, digits, dots and hyphens (Agent Plugins name)"
        )
    if not record["description"]:
        errors.append("Description: empty")
    if record["category"] not in store.CATEGORIES:
        errors.append(f"Category: one of {', '.join(store.CATEGORIES)}")
    if not store.REPO_RE.match(record["repository"]):
        errors.append("GitHub repository: owner/repo")
    if ".." in record["path"].split("/"):
        errors.append("Path inside the repository: a relative directory")
    if not TAG_RE.match(record["ref"]):
        errors.append("Release tag: a release tag, vX.Y.Z")
    if not record["submitted_version"]:
        errors.append("Version: empty")
    if not record["license"]:
        errors.append("License: empty")
    if not author["name"]:
        errors.append("Author name: empty")
    if author.get("url") and not URL_RE.match(author["url"]):
        errors.append("Author URL: an https URL")
    if record["homepage"] and not URL_RE.match(record["homepage"]):
        errors.append("Homepage: an https URL")
    if not record["keywords"]:
        errors.append("Keywords: at least one")
    return record, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="parse a submission issue body into a candidate")
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    body = Path(args.body_file).read_text(encoding="utf-8")
    record, errors = candidate(parse_form(body), args.issue)
    if args.json:
        print(json.dumps({"candidate": record, "errors": errors}, indent=2))
    else:
        for error in errors:
            print(error)
        if not errors:
            print(f"candidate {record['name']} at {record['repository']} {record['ref']}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
