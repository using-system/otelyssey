"""Turn a submission issue's body (the rendered issue form) into a candidate.

The form has one field, the URL of the plugin's plugin.json on GitHub: it gives the
repository and the path, nothing else. The ref is the repository's latest release tag when
it carries the plugin, otherwise its default branch, resolved here, never the URL's; every
other field is read from the manifest at that commit, by the derivation, after the
validation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from scripts import gitrepo, store

LABELS = ("plugin.json URL",)
EMPTY = "_No response_"
HOSTS = ("github.com", "www.github.com", "raw.githubusercontent.com")
BAD_URL = (
    "plugin.json URL: the URL of plugin.json on GitHub, as GitHub shows it "
    "(https://github.com/owner/repo/blob/main/plugin.json), on a branch or tag without a slash"
)
SEGMENT_RE = re.compile(r"^[^\x00-\x1f\x7f]+$")


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


def parse_url(url: str) -> tuple[str, str]:
    """The repository (owner/repo) and the plugin's directory the URL points at, or ValueError.

    github.com/<owner>/<repo>/blob|raw/<ref>/<path>/plugin.json and
    raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>/plugin.json; the ref is one segment
    (a branch with a slash cannot be told from the path) and is not used.
    """
    parts = urlsplit(url.strip())
    if parts.scheme != "https" or parts.netloc.lower() not in HOSTS or parts.query:
        raise ValueError(BAD_URL)
    segments = [unquote(s) for s in parts.path.split("/") if s]
    if parts.netloc.lower() == "raw.githubusercontent.com":
        head, rest = segments[:2], segments[2:]
    else:
        head, rest = segments[:2], segments[2:]
        if len(rest) < 1 or rest[0] not in ("blob", "raw"):
            raise ValueError(BAD_URL)
        rest = rest[1:]
    # after owner and repo: the ref, then the path, then plugin.json
    if len(head) != 2 or len(rest) < 2 or rest[-1] != "plugin.json":
        raise ValueError(BAD_URL)
    repository = "/".join(head)
    repository = repository[:-4] if repository.endswith(".git") else repository
    path_segments = rest[1:-1]
    if not store.REPO_RE.match(repository) or any(
        s in (".", "..") or not SEGMENT_RE.match(s) for s in path_segments
    ):
        raise ValueError(BAD_URL)
    return repository, "/".join(path_segments)


def candidate(fields: dict[str, str], issue_number: int) -> tuple[dict, list[str]]:
    """The repository and the path the URL names, the issue; or the errors."""
    errors = [f"{label}: section missing from the form" for label in LABELS if label not in fields]
    if errors:
        return {}, errors
    try:
        repository, path = parse_url(fields["plugin.json URL"])
    except ValueError as error:
        return {}, [str(error)]
    return {"repository": repository, "path": path, "submitted_in": issue_number}, []


def resolve_ref(repository: str, path: str) -> tuple[str, str, list[str]]:
    """The ref the marketplace follows (see gitrepo.release) and its commit, or the error."""
    try:
        ref, sha, _ = gitrepo.release(repository, path)
    except gitrepo.RepositoryError as error:
        return "", "", [f"GitHub repository: cannot be read ({error})"]
    return ref, sha, []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="parse a submission issue body into a candidate")
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument(
        "--no-resolve", action="store_true", help="skip resolving the repository's ref"
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    body = Path(args.body_file).read_text(encoding="utf-8")
    record, errors = candidate(parse_form(body), args.issue)
    if not errors and not args.no_resolve:
        ref, sha, errors = resolve_ref(record["repository"], record["path"])
        if not errors:
            record["ref"] = ref
            record["sha"] = sha
    if args.json:
        print(json.dumps({"candidate": record, "errors": errors}, indent=2))
    else:
        for error in errors:
            print(error)
        if not errors:
            print(f"candidate at {record['repository']} {record['path']!r} {record.get('ref', '')}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
