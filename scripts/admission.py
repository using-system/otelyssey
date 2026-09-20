"""The store record of an admitted submission, read back from the intake comment.

The review rules and labels; this script writes. The candidate block is an HTML comment the
agents never see (the GitHub MCP server strips it): the admission workflow reads the comment
through the REST API, where it is intact. The one value the review contributes is the
category, an enum read from its ruling line.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from scripts import report, store

BLOCK_RE = re.compile(re.escape(report.CANDIDATE_MARK) + r"(.*?) -->", re.DOTALL)
RULING_RE = re.compile(r"(?:^|\n)Ruling: admissible - .* in `([^`\n]*)`[ \t]*(?:\n|$)")


def candidate_from_comment(body: str) -> dict:
    """The candidate record of the last block in the comment; the intake writes one."""
    blocks = BLOCK_RE.findall(body)
    if not blocks:
        raise ValueError("no candidate block in the intake comment")
    try:
        candidate = json.loads(blocks[-1])
    except ValueError as error:
        raise ValueError(f"candidate block: not JSON ({error})") from None
    if not isinstance(candidate, dict):
        raise ValueError("candidate block: not an object")
    return candidate


def category_from_ruling(body: str) -> str:
    """The category the ruling line names, one of the store's; the last such line wins."""
    found = RULING_RE.findall(body)
    if not found:
        raise ValueError("the ruling names no category")
    category = found[-1]
    if category not in store.CATEGORIES:
        raise ValueError(f"the ruling's category {category!r} is not one of the store's")
    return category


def admitted(candidate: dict, issue: int, today: str, now: str, category: str) -> dict:
    """The candidate with the ruled category, `admitted_at` and zero `stats`, in the store's
    field order."""
    if candidate.get("submitted_in") != issue:
        raise ValueError(
            f"submitted_in: {candidate.get('submitted_in')!r} is not the issue {issue}"
        )
    record = {
        **candidate,
        "category": category,
        "admitted_at": today,
        "stats": {"stars": 0, "forks": 0, "watchers": 0, "refreshed_at": now},
    }
    return {field: record[field] for field in store.FIELDS if field in record}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="write the store record of an admitted submission")
    parser.add_argument("--comment-file", required=True, help="the intake comment's raw body")
    parser.add_argument("--ruling-file", required=True, help="the review's ruling, raw body")
    parser.add_argument("--issue", required=True, type=int, help="the submission issue's number")
    parser.add_argument("--root", default=".", help="the repository root")
    args = parser.parse_args(argv)
    try:
        body = Path(args.comment_file).read_text(encoding="utf-8")
        ruling = Path(args.ruling_file).read_text(encoding="utf-8")
    except OSError as error:
        print(error, file=sys.stderr)
        return 2
    moment = datetime.now(UTC)
    try:
        candidate = candidate_from_comment(body)
        record = admitted(
            candidate,
            args.issue,
            moment.strftime("%Y-%m-%d"),
            moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
            category_from_ruling(ruling),
        )
        path = store.write_record(Path(args.root), record)
    except ValueError as error:
        print(error)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
