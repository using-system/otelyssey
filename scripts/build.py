"""Generate the listing artifacts from the store: manifest, plugin pages, README list."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

from scripts import store

MARKETPLACE_NAME = "otelyssey"
MARKETPLACE_REPO = "using-system/otelyssey"
HERMES_PACK_URL = f"https://raw.githubusercontent.com/{MARKETPLACE_REPO}/main/hermes-pack.yaml"
OWNER = {"name": "using-system", "url": "https://github.com/using-system"}
LIST_START = "<!-- otelyssey:plugins -->"
LIST_END = "<!-- /otelyssey:plugins -->"
CATEGORY_TITLES = {
    "instrumentation": "Instrumentation",
    "collector": "Collector",
    "backend": "Backends",
    "observability": "Observability",
}
# live, from GitHub through shields.io: the README needs no refresh when a count moves; the
# version is the record's, a repository releases with or without a tag
BADGES = ("version", "created-at", "last-commit", "license", "stars", "forks", "watchers")
BADGE_STYLE = "style=flat-square&labelColor=2b2b2b&color=6b6b6b"


def source_of(record: dict) -> dict:
    """The `github` source both hosts accept, `path` added when the plugin is in a subdirectory."""
    source = {"source": "github", "repo": record["repository"]}
    if record["path"]:
        source["path"] = record["path"]
    source["ref"] = record["ref"]
    source["sha"] = record["sha"]
    return source


def codex_source_of(record: dict) -> dict:
    """The git-backed source Codex accepts: `url` for a plugin at its repository's root,
    `git-subdir` with a `./`-prefixed path otherwise; `ref` and `sha` on both."""
    url = f"https://github.com/{record['repository']}.git"
    if record["path"]:
        return {
            "source": "git-subdir",
            "url": url,
            "path": f"./{record['path']}",
            "ref": record["ref"],
            "sha": record["sha"],
        }
    return {"source": "url", "url": url, "ref": record["ref"], "sha": record["sha"]}


def codex_marketplace_json(records: dict[str, dict]) -> dict:
    """The catalog `codex plugin marketplace add` reads at .agents/plugins/marketplace.json."""
    plugins = []
    for name in sorted(records):
        record = records[name]
        # the manifest fields Codex lists before the install, when it has no manifest yet
        entry = {
            "name": record["name"],
            "description": record["description"],
            "version": record["version"],
            "keywords": record["keywords"],
            "author": record["author"],
            "source": codex_source_of(record),
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            # a scalar in the catalogs: the principal category
            "category": CATEGORY_TITLES[record["categories"][0]],
        }
        if record["homepage"]:
            entry["homepage"] = record["homepage"]
        plugins.append(entry)
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": MARKETPLACE_NAME},
        "plugins": plugins,
    }


def marketplace_json(records: dict[str, dict]) -> dict:
    plugins = []
    for name in sorted(records):
        record = records[name]
        entry = {
            "name": record["name"],
            "source": source_of(record),
            "description": record["description"],
            "version": record["version"],
            "category": record["categories"][0],
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


def hermes_pack(records: dict[str, dict]) -> str:
    """The plugin pack `hermes plugins pack install` reads: every plugin pinned at its sha (a
    tag or a branch is refused), `subdir` for a plugin in a subdirectory. Written by hand:
    the file is small and flat, the values are the store's (owner/repo, a path, a sha); the
    path and the sha are double-quoted, a JSON string being a YAML one: the store's path rule
    is loose, a sha of decimal digits reads as an int."""
    lines = [
        f"name: {MARKETPLACE_NAME}",
        "description: OpenTelemetry agent plugins admitted by otelyssey, at the admitted commits",
        "plugins:",
    ]
    for name in sorted(records):
        record = records[name]
        lines.append(f"  - repo: {record['repository']}")
        if record["path"]:
            lines.append(f"    subdir: {json.dumps(record['path'], ensure_ascii=False)}")
        # quoted too: a sha of forty decimal digits would read as an int, and Hermes refuses it
        lines.append(f'    ref: "{record["sha"]}"')
    return "\n".join(lines) + "\n"


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
    return (
        f"# {record['name']}\n\n"
        f"{text(record['description'])}\n\n"
        f"- Repository: [{record['repository']}]({repo_url}), the plugin at {where} it\n"
        f"- Categories: {', '.join(f'`{c}`' for c in record['categories'])}\n"
        f"- Version: {record['version']} (`{record['ref']}`, commit `{record['sha'][:12]}`)\n"
        f"- Author: {author_text}\n"
        f"- License: {record['license']}\n"
        f"- Keywords: {keywords}{homepage}\n"
        f"- Stars {stats['stars']}, forks {stats['forks']}, watchers {stats['watchers']}"
        f" (refreshed {stats['refreshed_at']})\n\n"
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
        "```\n\n"
        "Codex CLI:\n\n"
        "```text\n"
        f"codex plugin marketplace add {MARKETPLACE_REPO}\n"
        f"codex plugin add {record['name']}@{MARKETPLACE_NAME}\n"
        "```\n\n"
        "Grok Build:\n\n"
        "```text\n"
        f"grok plugin marketplace add {MARKETPLACE_REPO}\n"
        f"grok plugin install {record['name']} --trust\n"
        "```\n\n"
        "APM:\n\n"
        "```text\n"
        f"apm marketplace add {MARKETPLACE_REPO}\n"
        f"apm install {record['name']}@{MARKETPLACE_NAME} --target copilot\n"
        "```\n\n"
        "VS Code, in `settings.json`:\n\n"
        "```json\n"
        f'"chat.plugins.marketplaces": ["{MARKETPLACE_REPO}"]\n'
        "```\n"
        # Kiro imports a power from its repository's url: a plugin at the root only
        + (f"\nKiro: Import power from GitHub, `{repo_url}`.\n" if not record["path"] else "")
        + repository_install_lines(record)
    )


def repository_install_lines(record: dict) -> str:
    """The hosts that install from the plugin's repository: Hermes Agent opens with the
    marketplace's pack (every plugin, pinned), then pins this plugin's commit and takes a
    subdirectory; OpenClaw's git install takes the root only (a subdirectory goes through a
    clone of this marketplace, read locally); Mistral Vibe has no install command."""
    repository = record["repository"]
    repo_url = f"https://github.com/{repository}"
    clone_dir = repository.rsplit("/", 1)[1]
    name, path, sha = record["name"], record["path"], record["sha"]
    # the store lets a path carry a space or a shell metacharacter: quoted, today's are bare
    hermes_source = shlex.quote(f"{repository}/{path}" if path else repository)
    vibe_source = shlex.quote(f"{clone_dir}/{path}" if path else clone_dir)
    if path:
        openclaw = (
            f"git clone https://github.com/{MARKETPLACE_REPO}\n"
            f"openclaw plugins install {name} --marketplace ./{MARKETPLACE_NAME}\n"
        )
    else:
        openclaw = f"openclaw plugins install git:{repository}@{sha} --force\n"
    return (
        "\nHermes Agent:\n\n"
        "```text\n"
        # the pack, every plugin pinned, first; the two lines below install this one alone
        f"hermes plugins pack install {HERMES_PACK_URL}\n"
        f"hermes plugins install {hermes_source} --ref {sha}\n"
        f"hermes plugins enable {name}\n"
        "```\n\n"
        "OpenClaw:\n\n"
        "```text\n"
        f"{openclaw}"
        "```\n\n"
        "Mistral Vibe:\n\n"
        "```text\n"
        f"git clone {repo_url} && git -C {clone_dir} checkout {sha}\n"
        f"mkdir -p ~/.vibe/plugins/{name} && cp -r {vibe_source}/. ~/.vibe/plugins/{name}\n"
        "```\n"
    )


def badge(kind: str, record: dict) -> str:
    """A badge that goes nowhere: GitHub links a bare image to itself (and drops an anchor
    without href), so the anchor points at `#`, the nearest thing to no link."""
    if kind == "version":
        # shields' static badge: a dash or an underscore in the message is doubled
        message = record["version"].replace("-", "--").replace("_", "__")
        src = f"https://img.shields.io/badge/version-{quote(message)}-6b6b6b?{BADGE_STYLE}"
    else:
        src = f"https://img.shields.io/github/{kind}/{record['repository']}?{BADGE_STYLE}"
    return f'<a href="#"><img src="{src}" alt="{kind}"></a>'


def readme_entry(record: dict) -> str:
    """One list item: the plugin linked to its page, its author, its description; its badges
    below."""
    author = record["author"]
    author_name = text(author["name"])
    author_text = f"[{author_name}]({author['url']})" if author.get("url") else author_name
    # listed once, under the principal category; the others named in the line
    others = ", ".join(CATEGORY_TITLES[c] for c in record["categories"][1:])
    also = f" · also in {others}" if others else ""
    return (
        f"- [{record['name']}](marketplace/{record['name']}/README.md) by {author_text} - "
        f"{text(record['description'])}{also}  \n"
        + "&nbsp;&nbsp;".join(badge(kind, record) for kind in BADGES)
        + "\n\n"
    )


def readme_list(records: dict[str, dict]) -> str:
    """The plugins by principal category, in the store's category order, the empty categories
    left out."""
    if not records:
        return "No plugin listed yet.\n"
    sections = []
    for category in store.CATEGORIES:
        names = sorted(name for name, r in records.items() if r["categories"][0] == category)
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
    codex = render_json(codex_marketplace_json(records))
    wanted = {
        # Copilot CLI looks at the root first, Claude Code and VS Code in .claude-plugin/:
        # one content, twice; Codex reads its own catalog, with git-backed sources, and
        # Grok Build reads the same content at its own place (the github form gives it
        # nothing, verified on 1.0.34)
        "marketplace.json": manifest,
        ".claude-plugin/marketplace.json": manifest,
        ".agents/plugins/marketplace.json": codex,
        ".grok-plugin/marketplace.json": codex,
        "README.md": splice(readme, readme_list(records)),
    }
    if records:
        # Hermes Agent installs the whole pack, pinned, after a review screen; it refuses
        # an empty one, so an empty store has no pack
        wanted["hermes-pack.yaml"] = hermes_pack(records)
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
    pack = root / "hermes-pack.yaml"
    if not records and pack.exists():
        changed.append(pack.name)
        if not check:
            pack.unlink()
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
