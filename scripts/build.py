"""Generate the listing artifacts from the store: manifest, plugin pages, README table."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts import store

MARKETPLACE_NAME = "otelyssey"
MARKETPLACE_REPO = "using-system/otelyssey"
OWNER = {"name": "using-system", "url": "https://github.com/using-system"}
TABLE_START = "<!-- otelyssey:table -->"
TABLE_END = "<!-- /otelyssey:table -->"


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


def plugin_page(record: dict) -> str:
    repo_url = f"https://github.com/{record['repository']}"
    where = f"`{record['path']}` in" if record["path"] else "the root of"
    keywords = ", ".join(f"`{k}`" for k in record["keywords"]) or "none"
    author = record["author"]
    author_text = f"[{author['name']}]({author['url']})" if author.get("url") else author["name"]
    homepage = f"\n- Homepage: <{record['homepage']}>" if record["homepage"] else ""
    stats = record["stats"]
    issue_url = f"https://github.com/{MARKETPLACE_REPO}/issues/{record['submitted_in']}"
    return (
        f"# {record['name']}\n\n"
        f"{record['description']}\n\n"
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


def cell(text: str) -> str:
    """One markdown table cell: whitespace collapsed to spaces, pipes escaped."""
    return " ".join(text.split()).replace("|", "\\|")


def readme_table(records: dict[str, dict]) -> str:
    lines = [
        "| Plugin | Description | Category | Repository | Stars | Forks | Watchers |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for name in sorted(records):
        r = records[name]
        s = r["stats"]
        repo = f"[{r['repository']}](https://github.com/{r['repository']})"
        lines.append(
            f"| [{name}](marketplace/{name}/README.md) | {cell(r['description'])} | "
            f"{cell(r['category'])} | "
            f"{repo} | {s['stars']} | {s['forks']} | {s['watchers']} |"
        )
    return "\n".join(lines) + "\n"


def splice(text: str, table: str) -> str:
    start = text.index(TABLE_START) + len(TABLE_START)
    end = text.index(TABLE_END)
    return text[:start] + "\n" + table + text[end:]


def build(root: Path, check: bool) -> list[str]:
    """Write (or, under check, only compare) the artifacts; the relative paths that differ."""
    records = store.load_store(root)
    readme = (root / "README.md").read_text(encoding="utf-8")
    wanted = {
        ".claude-plugin/marketplace.json": render_json(marketplace_json(records)),
        "README.md": splice(readme, readme_table(records)),
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
            path.unlink()
            path.parent.rmdir()
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
