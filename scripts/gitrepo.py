"""Read a public GitHub repository through git: its tags, its default branch, a ref's commit,
a shallow checkout; and the ref the marketplace follows."""

from __future__ import annotations

import http.client
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
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


def parse_head(ls_remote_output: str) -> tuple[str, str]:
    """The default branch and its commit, from `git ls-remote --symref <url> HEAD`."""
    branch = sha = ""
    for line in ls_remote_output.splitlines():
        parts = line.split("\t")
        if len(parts) != 2 or parts[1] != "HEAD":
            continue
        if parts[0].startswith("ref: refs/heads/"):
            branch = parts[0][len("ref: refs/heads/") :]
        elif SHA_RE.match(parts[0]):
            sha = parts[0]
    if not branch or not sha:
        raise RepositoryError("no default branch")
    return branch, sha


def default_branch(repository: str) -> tuple[str, str]:
    """The default branch and its head commit."""
    return parse_head(_git(["ls-remote", "--symref", repo_url(repository), "HEAD"], timeout=60))


def resolve(repository: str, ref: str) -> str:
    """The commit of a tag or a branch, the tag first when a name is both; a full sha stands
    for itself."""
    if SHA_RE.match(ref):
        return ref
    tags = list_tags(repository)
    if ref in tags:
        return tags[ref]
    heads = _git(["ls-remote", "--heads", repo_url(repository), ref], timeout=60)
    for line in heads.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and parts[1] == f"refs/heads/{ref}":
            return parts[0]
    raise LookupError(f"{repository} has no tag or branch {ref}")


def has_file(repository: str, sha: str, path: str) -> bool:
    """Whether the file is at the commit, asked of raw.githubusercontent.com without a clone."""
    url = f"https://raw.githubusercontent.com/{repository}/{sha}/{urllib.parse.quote(path)}"
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status == 200
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise RepositoryError(f"{url}: HTTP {error.code}") from error
    except (OSError, http.client.HTTPException) as error:
        # URLError, timeouts and ssl errors are OSErrors; a dropped or malformed response is
        # an HTTPException: every network failure is the repository's, never a crash
        raise RepositoryError(f"{url}: {error}") from error


def release(repository: str, path: str) -> tuple[str, str, bool]:
    """The ref the marketplace follows and its commit, and whether it is a tag.

    The latest release tag, when the plugin's manifest is at it; otherwise the default
    branch and its head: a repository whose tags predate the plugin is followed on its
    branch until a tag carries it.
    """
    latest = latest_release(list_tags(repository))
    manifest = f"{path}/plugin.json" if path else "plugin.json"
    if latest is not None and has_file(repository, latest[1], manifest):
        return latest[0], latest[1], True
    branch, sha = default_branch(repository)
    return branch, sha, False


def clone_at(repository: str, sha: str, dest: Path) -> None:
    """One commit, no history, no credentials."""
    dest.mkdir(parents=True, exist_ok=True)
    _git(["init", "-q"], cwd=dest)
    _git(["remote", "add", "origin", repo_url(repository)], cwd=dest)
    _git(["fetch", "-q", "--depth", "1", "origin", sha], cwd=dest)
    _git(["checkout", "-q", "FETCH_HEAD"], cwd=dest)
