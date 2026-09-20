"""Validate a plugin at a commit: the manifest against the Agent Plugins schema, the layout."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

from scripts import gitrepo, store

SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
# The 1.0.0 schema as published on 2026-09-19: $schema and name required, no other root key
# (additionalProperties false), name's pattern, the optional string fields, author's three
# string sub-fields, keywords a list of strings, extensions an object of objects.
ROOT_KEYS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
OPTIONAL_STRINGS = ("version", "description", "homepage", "repository", "license")
AUTHOR_KEYS = {"name", "email", "url"}
KNOWN_ENTRIES = {"plugin.json", "skills", "mcp.json", "README.md", "LICENSE", "CHANGELOG.md"}
NAMESPACE_RE = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")  # a reverse-domain extension directory
VERSION_RE = re.compile(r"^[^\s`]+$")


def check_manifest(
    plugin_dir: Path, expected_name: str, expected_version: str
) -> tuple[dict, list[str]]:
    """The manifest read and every error.

    An empty expected_name or expected_version skips that match; the manifest must still carry
    both, they are the name and the version the record takes.
    """
    errors: list[str] = []
    manifest_path = plugin_dir / "plugin.json"
    if not manifest_path.is_file():
        if (plugin_dir / ".claude-plugin" / "plugin.json").is_file():
            errors.append(
                "plugin.json: missing at the plugin's root; .claude-plugin/plugin.json is the "
                "pre-standard layout, the Agent Plugins format puts plugin.json at the root"
            )
        else:
            errors.append("plugin.json: missing at the plugin's root")
        return {}, errors
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError as error:
        return {}, [f"plugin.json: not JSON ({error})"]
    if not isinstance(manifest, dict):
        return {}, ["plugin.json: not an object"]
    unknown = sorted(set(manifest) - ROOT_KEYS)
    if unknown:
        errors.append(f"plugin.json: unknown keys {', '.join(unknown)} (schema)")
    if manifest.get("$schema") != SCHEMA_URL:
        errors.append(f"plugin.json: $schema must be {SCHEMA_URL} (schema)")
    name = manifest.get("name")
    if not isinstance(name, str) or not 1 <= len(name) <= 64 or not store.NAME_RE.match(name):
        errors.append("plugin.json: name does not match the Agent Plugins pattern (schema)")
    for field in OPTIONAL_STRINGS:
        if field in manifest and not isinstance(manifest[field], str):
            errors.append(f"plugin.json: {field} must be a string (schema)")
    author = manifest.get("author")
    if author is not None and (
        not isinstance(author, dict)
        or set(author) - AUTHOR_KEYS
        or not all(isinstance(v, str) for v in author.values())
    ):
        errors.append("plugin.json: author is an object of name, email, url strings (schema)")
    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords)
    ):
        errors.append("plugin.json: keywords must be a list of strings (schema)")
    extensions = manifest.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or not all(isinstance(v, dict) for v in extensions.values())
    ):
        errors.append("plugin.json: extensions is an object whose values are objects (schema)")
    if expected_name and isinstance(name, str) and name != expected_name:
        errors.append(f"plugin.json: name is {name!r}, the submission says {expected_name!r}")
    version = manifest.get("version")
    if isinstance(version, str) and version and not VERSION_RE.match(version):
        # the version stands in backticks on the line the review rules on
        errors.append("plugin.json: version carries whitespace or a backtick")
    if not expected_version:
        if not version:
            errors.append("plugin.json: version missing")
    elif version != expected_version:
        errors.append(
            f"plugin.json: version is {version!r}, the submission says {expected_version!r}"
        )
    return manifest, errors


def check_layout(plugin_dir: Path) -> list[str]:
    """Notes: the directories the format does not define, and a `skills/` entry without
    SKILL.md, which is not a skill and which a client skips rather than refuses the plugin for.

    Known: plugin.json, skills/, mcp.json, README, LICENSE, CHANGELOG, dotfiles, and a
    reverse-domain directory (an extension namespace, `com.example.tool`). A plain file next
    to plugin.json is never a note: the format tolerates any file, and a plugin at its
    repository's root sits next to all of the repository's files.
    """
    notes: list[str] = []
    for entry in sorted(plugin_dir.iterdir()):
        if entry.name == ".claude-plugin":
            notes.append(".claude-plugin: pre-standard layout carried next to plugin.json")
        elif not entry.is_dir() or entry.name.startswith(".") or entry.name in KNOWN_ENTRIES:
            continue
        elif NAMESPACE_RE.match(entry.name):
            continue
        else:
            notes.append(f"{entry.name}: not an entry the Agent Plugins format defines")
    skills = plugin_dir / "skills"
    if skills.is_dir():
        for skill in sorted(skills.iterdir()):
            if skill.is_dir() and not (skill / "SKILL.md").is_file():
                notes.append(f"skills/{skill.name}: not a skill, no SKILL.md")
    return notes


def validate(
    repository: str,
    ref: str,
    path: str,
    expected_name: str,
    expected_version: str,
    workdir: Path,
) -> dict:
    """sha, manifest, errors and notes of the plugin at the ref (a tag, a branch, a full sha);
    never raises on a bad input."""
    result: dict = {"sha": None, "manifest": {}, "errors": [], "notes": []}
    if path.startswith("/") or ".." in path.split("/"):
        result["errors"].append("path: not a relative directory inside the repository")
        return result
    try:
        sha = gitrepo.resolve(repository, ref)
        result["sha"] = sha
        checkout = workdir / "checkout"
        gitrepo.clone_at(repository, sha, checkout)
    except (LookupError, gitrepo.RepositoryError) as error:
        result["errors"].append(f"repository: {error}")
        return result
    plugin_dir = checkout / path if path else checkout
    if not plugin_dir.is_dir():
        result["errors"].append(f"path {path!r}: no such directory at {ref}")
        return result
    manifest, errors = check_manifest(plugin_dir, expected_name, expected_version)
    result["manifest"] = manifest
    result["errors"] = errors
    result["notes"] = check_layout(plugin_dir)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="validate a plugin at a ref")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--ref", required=True, help="a tag, a branch, or a full commit sha")
    parser.add_argument("--path", default="")
    parser.add_argument("--name", default="", help="empty skips the name match")
    parser.add_argument("--version", default="", help="empty skips the version match")
    parser.add_argument("--workdir", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    workdir = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="otelyssey-"))
    result = validate(args.repository, args.ref, args.path, args.name, args.version, workdir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for error in result["errors"]:
            print(error)
        for note in result["notes"]:
            print(f"note: {note}")
        if not result["errors"]:
            print(f"valid at {result['sha']}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
