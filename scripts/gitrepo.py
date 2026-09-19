"""Read a public GitHub repository through git: its tags, a tag's commit, a shallow checkout."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "/bin/true"}


class RepositoryError(Exception):
    """A repository that cannot be read: private, deleted, mistyped, or unreachable."""


def repo_url(repository: str) -> str:
    return f"https://github.com/{repository}.git"


def parse_tags(ls_remote_output: str) -> dict[str, str]:
    """Tag name to commit sha; a peeled `^{}` line wins over the tag object's own sha."""
    tags: dict[str, str] = {}
    for line in ls_remote_output.splitlines():
        parts = line.split("\t")
        if len(parts) != 2 or not parts[1].startswith("refs/tags/"):
            continue
        sha, ref = parts
        name = ref[len("refs/tags/") :]
        if name.endswith("^{}"):
            tags[name[:-3]] = sha
        else:
            tags.setdefault(name, sha)
    return tags


def semver_key(tag: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.match(tag)
    return tuple(int(x) for x in match.groups()) if match else None


def latest_release(tags: dict[str, str]) -> tuple[str, str] | None:
    releases = [(semver_key(t), t) for t in tags if semver_key(t) is not None]
    if not releases:
        return None
    _, tag = max(releases)
    return tag, tags[tag]


def _git(args: list[str], cwd: Path | None = None, timeout: int = 300) -> str:
    try:
        return subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            env=GIT_ENV,
            timeout=timeout,
        ).stdout
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip().splitlines()
        raise RepositoryError(detail[-1] if detail else "git failed") from error
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RepositoryError(str(error)) from error


def list_tags(repository: str) -> dict[str, str]:
    """Every tag with its commit, through `git ls-remote --tags` (peeled lines included)."""
    return parse_tags(_git(["ls-remote", "--tags", repo_url(repository)], timeout=60))


def resolve(repository: str, tag: str) -> str:
    tags = list_tags(repository)
    if tag not in tags:
        raise LookupError(f"{repository} has no tag {tag}")
    return tags[tag]


def clone_at(repository: str, sha: str, dest: Path) -> None:
    """One commit, no history, no credentials."""
    dest.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q"], cwd=dest)
    _git(["remote", "add", "origin", repo_url(repository)], cwd=dest)
    _git(["fetch", "-q", "--depth", "1", "origin", sha], cwd=dest)
    _git(["checkout", "-q", "FETCH_HEAD"], cwd=dest)
