"""Generate the listing artifacts from the store: manifest, plugin pages, README list."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from scripts import store

MARKETPLACE_NAME = "otelyssey"
MARKETPLACE_REPO = "using-system/otelyssey"
OWNER = {"name": "using-system", "url": "https://github.com/using-system"}
LIST_START = "<!-- otelyssey:plugins -->"
LIST_END = "<!-- /otelyssey:plugins -->"
CATEGORY_TITLES = {
    "instrumentation": "Instrumentation",
    "collector": "Collector",
    "conventions": "Semantic conventions",
    "backend": "Backends",
    "workflow": "Workflows",
}
# live, from GitHub through shields.io: the README needs no refresh when a count moves
BADGES = ("v/release", "created-at", "last-commit", "license", "stars", "forks", "watchers")
BADGE_STYLE = "style=flat-square&labelColor=2b2b2b&color=6b6b6b"


def source_of(record: dict) -> dict:
    """The `github` source both hosts accept, `path` added when the plugin is in a subdirectory."""
    source = {"source": "github", "repo": record["repository"]}
    if record["path"]:
        source["path"] = record["path"]
    source["ref"] = record["ref"]
    source["sha"] = record["sha"]
    return source


def marketplace_json(records: dict[str, dict]) -> dict:
    plugins = []
    for name in sorted(records):
        record = records[name]
        entry = {
            "name": record["name"],
            "source": source_of(record),
            "description": record["description"],
            "version": record["version"],
            "category": record["category"],
            "keywords": record["keywords"],
            "license": record["license"],
            "author": record["author"],
        }
        if record["homepage"]:
            entry["homepage"] = record["homepage"]
        plugins.append(entry)
    return {
        "name": MARKETPLACE_NAME,
        "owner": OWNER,
        "description": "A self-run marketplace of OpenTelemetry agent plugins",
        "plugins": plugins,
    }


def render_json(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


MARKDOWN_ESCAPES = str.maketrans({c: f"\\{c}" for c in "[]<>*_`"})


def text(value: str) -> str:
    """Free text in a page: whitespace collapsed; link, tag and emphasis marks escaped."""
    return " ".join(value.split()).translate(MARKDOWN_ESCAPES)


def plugin_page(record: dict) -> str:
    """The urls (homepage, author url) passed the store's https rule; the free text is escaped."""
    repo_url = f"https://github.com/{record['repository']}"
    where = f"`{record['path']}` in" if record["path"] else "the root of"
    keywords = ", ".join(f"`{k}`" for k in record["keywords"]) or "none"
    author = record["author"]
    author_name = text(author["name"])
    author_text = f"[{author_name}]({author['url']})" if author.get("url") else author_name
    homepage = f"\n- Homepage: <{record['homepage']}>" if record["homepage"] else ""
    stats = record["stats"]
    issue_url = f"https://github.com/{MARKETPLACE_REPO}/issues/{record['submitted_in']}"
    return (
        f"# {record['name']}\n\n"
        f"{text(record['description'])}\n\n"
        f"- Category: `{record['category']}`\n"
        f"- Repository: [{record['repository']}]({repo_url}), the plugin at {where} it\n"
        f"- Version: {record['version']} (tag `{record['ref']}`, commit `{record['sha'][:12]}`)\n"
        f"- Author: {author_text}\n"
        f"- License: {record['license']}\n"
        f"- Keywords: {keywords}{homepage}\n"
        f"- Stars {stats['stars']}, forks {stats['forks']}, watchers {stats['watchers']}"
        f" (refreshed {stats['refreshed_at']})\n"
        f"- Admitted from [issue #{record['submitted_in']}]({issue_url})"
        f" on {record['admitted_at']}\n\n"
        "## Install\n\n"
        "Claude Code:\n\n"
        "```text\n"
        f"claude plugin marketplace add {MARKETPLACE_REPO}\n"
        f"claude plugin install {record['name']}@{MARKETPLACE_NAME}\n"
        "```\n\n"
        "GitHub Copilot CLI:\n\n"
        "```text\n"
        f"copilot plugin marketplace add {MARKETPLACE_REPO}\n"
        f"copilot plugin install {record['name']}@{MARKETPLACE_NAME}\n"
        "```\n"
    )


def badge(kind: str, repository: str) -> str:
    alt = kind.rsplit("/", 1)[-1]
    src = f"https://img.shields.io/github/{kind}/{repository}?{BADGE_STYLE}"
    return f'<img src="{src}" alt="{alt}">'


def readme_entry(record: dict) -> str:
    """One list item: the plugin, its author, its description, its page; its badges below."""
    author = record["author"]
    author_name = text(author["name"])
    author_text = f"[{author_name}]({author['url']})" if author.get("url") else author_name
    repo = record["repository"]
    return (
        f"- [{record['name']}](https://github.com/{repo}) by {author_text} - "
        f"{text(record['description'])} · [install](marketplace/{record['name']}/README.md)  \n"
        + "&nbsp;&nbsp;".join(badge(kind, repo) for kind in BADGES)
        + "\n\n"
    )


def readme_list(records: dict[str, dict]) -> str:
    """The plugins by category, in the store's category order, the empty categories left out."""
    if not records:
        return "No plugin listed yet.\n"
    sections = []
    for category in store.CATEGORIES:
        names = sorted(name for name, r in records.items() if r["category"] == category)
        if names:
            entries = "".join(readme_entry(records[name]) for name in names)
            sections.append(f"### {CATEGORY_TITLES[category]}\n\n{entries}")
    return "".join(sections)


def splice(text: str, listing: str) -> str:
    if LIST_START not in text or LIST_END not in text:
        raise SystemExit("README.md: the list markers are missing")
    start = text.index(LIST_START) + len(LIST_START)
    end = text.index(LIST_END)
    return text[:start] + "\n" + listing + text[end:]


def build(root: Path, check: bool) -> list[str]:
    """Write (or, under check, only compare) the artifacts; the relative paths that differ."""
    records = store.load_store(root)
    readme = (root / "README.md").read_text(encoding="utf-8")
    manifest = render_json(marketplace_json(records))
    wanted = {
        # Copilot CLI looks at the root first, Claude Code in .claude-plugin/ only: one
        # content, twice
        "marketplace.json": manifest,
        ".claude-plugin/marketplace.json": manifest,
        "README.md": splice(readme, readme_list(records)),
    }
    for name, record in records.items():
        wanted[f"marketplace/{name}/README.md"] = plugin_page(record)
    changed: list[str] = []
    for relative, content in wanted.items():
        path = root / relative
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            changed.append(relative)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    pages = (root / "marketplace").glob("*/README.md") if (root / "marketplace").is_dir() else []
    for path in pages:
        if path.parent.name in records:
            continue
        changed.append(str(path.relative_to(root)))
        if not check:
            shutil.rmtree(path.parent)
    return sorted(changed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="generate the marketplace artifacts from the store"
    )
    parser.add_argument("--check", action="store_true", help="compare only; exit 1 when stale")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    changed = build(Path(args.root), check=args.check)
    for relative in changed:
        print(("stale: " if args.check else "wrote: ") + relative)
    if not changed:
        print("up to date")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
