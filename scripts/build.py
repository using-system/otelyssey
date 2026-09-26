"""Generate the listing artifacts from the store: manifest, plugin pages, README list."""

from __future__ import annotations

import argparse
import base64
import json
import re
import shlex
import shutil
import sys
from pathlib import Path
from urllib.parse import quote, urlencode

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
CATEGORY_ICONS = {
    "instrumentation": "🔧",
    "collector": "🔀",
    "backend": "☁️",
    "observability": "👀",
}
CATEGORY_TAGLINES = {
    "instrumentation": "Put the telemetry in: SDKs, semantic conventions, instrumentation advice.",
    "collector": "Route it: the Collector, its configuration, OTTL, pipelines.",
    "backend": "Talk to a backend: query it, its dashboards, alerts and issues.",
    "observability": "Read it back: observe a run through its telemetry, wherever it lands.",
}
# live, from GitHub through shields.io: the README needs no refresh when a count moves; the
# version is the record's, a repository releases with or without a tag. Each badge its color;
# the counts a visitor does not need (created-at, forks, watchers) stay on the plugin page
STAR_COLOR = "e3b341"
VERSION_COLOR = "3b7dd8"
# the stars badge is a star and the count, no word: shields takes a custom logo as a data
# uri, this one a yellow star, and an empty label leaves the logo alone on the left
STAR_LOGO = (
    "data:image/svg+xml;base64,"
    + base64.b64encode(
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            f'<path fill="#{STAR_COLOR}" d="M12 1l3.4 7 7.6 1.1-5.5 5.4 1.3 7.6L12 18.5 '
            '5.2 22.1l1.3-7.6L1 9.1 8.6 8z"/></svg>'
        ).encode()
    ).decode()
)
BADGES = {
    "stars": urlencode({"label": "", "logo": STAR_LOGO, "color": STAR_COLOR}),
    "version": f"color={VERSION_COLOR}",
    "last-commit": "color=2ea44f",
    "license": "color=6b6b6b",
}
BADGE_STYLE = "style=flat-square&labelColor=2b2b2b"
AVATAR_SIZE = 20
# where the OpenCode lines clone a plugin; OpenCode expands `~` in skills.paths and
# substitutes {env:NAME} in the rest of its configuration
OPENCODE_HOME = ".opencode-plugins"
ENV_REF_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def source_of(record: dict) -> dict:
    """The `url` source Claude Code, Copilot CLI and APM all accept: cloned over https, the
    sha checked out (a `github` source, Claude Code clones over ssh, which fails without a
    GitHub key). `path` added when the plugin is in a subdirectory."""
    source = {"source": "url", "url": f"https://github.com/{record['repository']}.git"}
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
            # the plugin.json is the authority, the entry supplements it: Claude Code's
            # default, declared for the scanners that want it explicit
            "strict": True,
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
        # at the root too: the HOL scanner reads it there only, Claude Code ignores it there
        "strict": True,
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


# the backslash first among them: unescaped, a contributor's `\[` would come out `\\[`, an
# escaped backslash and a live bracket
MARKDOWN_ESCAPES = str.maketrans({c: f"\\{c}" for c in "\\[]<>*_`"})


def text(value: str) -> str:
    """Free text in a page: whitespace collapsed; link, tag and emphasis marks escaped."""
    return " ".join(value.split()).translate(MARKDOWN_ESCAPES)


def plugin_page(record: dict) -> str:
    """The urls (homepage, author url) passed the store's https rule; the free text is escaped;
    what stands in a code span (path, ref, keywords) carries no backtick, the store refuses it."""
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
        f"- Version: {text(record['version'])} (`{record['ref']}`, commit `{record['sha'][:12]}`)\n"
        f"- Author: {author_text}\n"
        f"- License: {text(record['license'])}\n"
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
        + opencode_install_lines(record)
    )


def repository_install_lines(record: dict) -> str:
    """The hosts that install from the plugin's repository: Hermes Agent opens with the
    marketplace's pack (every plugin, pinned), then pins this plugin's commit and takes a
    subdirectory; OpenClaw and Mistral Vibe take a clone at the sha, OpenClaw installs the
    directory (its git route wants a native package, its marketplace route drops the path),
    Vibe copies it, having no install command."""
    repository = record["repository"]
    repo_url = f"https://github.com/{repository}"
    clone_dir = repository.rsplit("/", 1)[1]
    name, path, sha = record["name"], record["path"], record["sha"]
    # the store lets a path carry a space or a shell metacharacter: quoted, today's are bare
    hermes_source = shlex.quote(f"{repository}/{path}" if path else repository)
    plugin_dir = shlex.quote(f"{clone_dir}/{path}" if path else clone_dir)
    clone = f"git clone {repo_url} && git -C {clone_dir} checkout {sha}\n"
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
        f"{clone}"
        f"openclaw plugins install ./{plugin_dir} --force --accept-capabilities\n"
        "```\n\n"
        "Mistral Vibe:\n\n"
        "```text\n"
        f"{clone}"
        f"mkdir -p ~/.vibe/plugins/{name} && cp -r ./{plugin_dir}/. ~/.vibe/plugins/{name}\n"
        "```\n"
    )


def opencode_mcp(record: dict) -> dict:
    """The record's MCP servers in OpenCode's shape: stdio a local command array, streamable
    http a remote url; sse, which OpenCode's remote entry does not name, is left out. The
    plugin's root and data directories stand for ${PLUGIN_ROOT} and ${PLUGIN_DATA} and a
    `./` command or cwd, any other ${NAME} is read from the user's environment."""
    clone = f"{{env:HOME}}/{OPENCODE_HOME}/{record['name']}"
    root = f"{clone}/{record['path']}" if record["path"] else clone
    data = f"{{env:HOME}}/{OPENCODE_HOME}/.data/{record['name']}"

    def value(text: str) -> str:
        text = text.replace("${PLUGIN_ROOT}", root).replace("${PLUGIN_DATA}", data)
        return ENV_REF_RE.sub(r"{env:\1}", text)

    def local(path: str) -> str:
        return value(f"{root}{path[1:]}" if path.startswith("./") else path)

    servers: dict = {}
    for name, server in record["mcp"].items():
        if server["type"] == "stdio":
            entry = {"type": "local", "command": [local(server["command"])]}
            entry["command"] += [value(a) for a in server.get("args", [])]
            if "cwd" in server:
                entry["cwd"] = local(server["cwd"])
            if server.get("env"):
                entry["environment"] = {k: value(v) for k, v in server["env"].items()}
        elif server["type"] == "streamable-http":
            entry = {"type": "remote", "url": value(server["url"])}
            if server.get("headers"):
                entry["headers"] = {k: value(v) for k, v in server["headers"].items()}
        else:
            continue
        servers[name] = entry
    return servers


def opencode_install_lines(record: dict) -> str:
    """OpenCode has no marketplace and installs no plugin: the plugin is cloned at the sha, and
    its configuration names the skills directory and the MCP servers. Nothing when the plugin
    carries neither."""
    name, path = record["name"], record["path"]
    config: dict = {}
    if record["skills"]:
        skills = (
            f"~/{OPENCODE_HOME}/{name}/{path}/skills"
            if path
            else f"~/{OPENCODE_HOME}/{name}/skills"
        )
        config["skills"] = {"paths": [skills]}
    mcp = opencode_mcp(record)
    if mcp:
        config["mcp"] = mcp
    if not config:
        return ""
    clone_dir = f"~/{OPENCODE_HOME}/{name}"
    return (
        "\nOpenCode:\n\n"
        "```text\n"
        f"git clone https://github.com/{record['repository']} {clone_dir}"
        f" && git -C {clone_dir} checkout {record['sha']}\n"
        "```\n\n"
        "Then merge into `~/.config/opencode/opencode.json`:\n\n"
        "```json\n"
        f"{json.dumps(config, indent=2, ensure_ascii=False)}\n"
        "```\n"
    )


def badge(kind: str, record: dict) -> str:
    """A badge that goes nowhere: GitHub links a bare image to itself (and drops an anchor
    without href), so the anchor points at `#`, the nearest thing to no link."""
    style = f"{BADGE_STYLE}&{BADGES[kind]}"
    if kind == "version":
        # shields' static badge: a dash or an underscore in the message is doubled
        message = record["version"].replace("-", "--").replace("_", "__")
        src = f"https://img.shields.io/badge/version-{quote(message)}-{VERSION_COLOR}?{style}"
    else:
        src = f"https://img.shields.io/github/{kind}/{record['repository']}?{style}"
    return f'<a href="#"><img src="{src}" alt="{kind}"></a>'


def avatar(record: dict) -> str:
    """The organisation's picture, GitHub's own for the repository's owner (the store's
    repository rule keeps the owner to letters, digits and dashes)."""
    owner = record["repository"].split("/")[0]
    return (
        f'<img src="https://github.com/{owner}.png?size={2 * AVATAR_SIZE}" '
        f'width="{AVATAR_SIZE}" height="{AVATAR_SIZE}" alt="">'
    )


def readme_entry(record: dict) -> str:
    """One list item: the owner's avatar, the plugin linked to its page, its author, its
    description; its badges below."""
    author = record["author"]
    author_name = text(author["name"])
    author_text = f"[{author_name}]({author['url']})" if author.get("url") else author_name
    # listed once, under the principal category; the others named in the line
    others = ", ".join(CATEGORY_TITLES[c] for c in record["categories"][1:])
    also = f" · also in {others}" if others else ""
    return (
        f"- {avatar(record)} **[{record['name']}](marketplace/{record['name']}/README.md)** "
        f"by {author_text} — {text(record['description'])}{also}  \n"
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
            sections.append(
                f"### {CATEGORY_ICONS[category]} {CATEGORY_TITLES[category]}\n\n"
                f"{CATEGORY_TAGLINES[category]}\n\n{entries}"
            )
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
