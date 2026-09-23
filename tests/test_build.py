import json
from pathlib import Path

import pytest

from scripts import build, store

FIXTURES = Path(__file__).parent / "fixtures"
EMPTY_README = "# x\n\n<!-- otelyssey:plugins -->\n<!-- /otelyssey:plugins -->\n"


def records():
    return store.load_store(FIXTURES / "store-root")


def root_with_fixture(tmp_path: Path) -> Path:
    (tmp_path / ".store").mkdir()
    src = FIXTURES / "store-root" / ".store" / "oddyssey.json"
    (tmp_path / ".store" / "oddyssey.json").write_bytes(src.read_bytes())
    (tmp_path / "README.md").write_text(EMPTY_README)
    return tmp_path


def test_fixture_is_canonical():
    text = (FIXTURES / "store-root" / ".store" / "oddyssey.json").read_text()
    assert text == store.canonical(json.loads(text))


def test_marketplace_entry_pins_the_admitted_commit():
    payload = build.marketplace_json(records())
    assert payload["name"] == "otelyssey"
    assert payload["owner"] == {"name": "using-system", "url": "https://github.com/using-system"}
    [entry] = payload["plugins"]
    assert entry["name"] == "oddyssey"
    # the url form: Claude Code and Copilot CLI clone it over https and check out the sha
    # (a github source, Claude Code clones over ssh; verified 2026-09-21)
    assert entry["source"] == {
        "source": "url",
        "url": "https://github.com/using-system/oddyssey.git",
        "path": "marketplace/oddyssey",
        "ref": "v1.13.0",
        "sha": "1" * 40,
    }
    assert entry["strict"] is True
    assert entry["version"] == "1.13.0"
    # a scalar in the catalogs: the principal category
    assert entry["category"] == "observability"


def test_root_plugin_has_no_path():
    record = dict(records()["oddyssey"])
    record["path"] = ""
    [entry] = build.marketplace_json({"oddyssey": record})["plugins"]
    assert entry["source"] == {
        "source": "url",
        "url": "https://github.com/using-system/oddyssey.git",
        "ref": "v1.13.0",
        "sha": "1" * 40,
    }


def test_render_json_is_stable():
    payload = build.marketplace_json(records())
    assert build.render_json(payload) == json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def test_codex_marketplace_uses_git_backed_sources_pinned_at_the_sha():
    # Codex reads .agents/plugins/marketplace.json: url for a plugin at its repository's
    # root, git-subdir with a ./-prefixed path otherwise, ref and sha on both
    payload = build.codex_marketplace_json(records())
    assert payload["name"] == "otelyssey"
    assert payload["interface"] == {"displayName": "otelyssey"}
    [entry] = payload["plugins"]
    assert entry["name"] == "oddyssey"
    assert entry["source"] == {
        "source": "git-subdir",
        "url": "https://github.com/using-system/oddyssey.git",
        "path": "./marketplace/oddyssey",
        "ref": "v1.13.0",
        "sha": records()["oddyssey"]["sha"],
    }
    assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    assert entry["category"] == "Observability"
    assert entry["description"] == records()["oddyssey"]["description"]
    assert entry["version"] == "1.13.0" and entry["keywords"] == records()["oddyssey"]["keywords"]
    assert entry["author"] == records()["oddyssey"]["author"]
    root_plugin = {**records()["oddyssey"], "path": ""}
    [entry] = build.codex_marketplace_json({"oddyssey": root_plugin})["plugins"]
    assert entry["source"] == {
        "source": "url",
        "url": "https://github.com/using-system/oddyssey.git",
        "ref": "v1.13.0",
        "sha": root_plugin["sha"],
    }


def test_hermes_pack_pins_every_plugin_at_its_sha():
    # Hermes refuses a tag or a branch in ref: the sha, never the record's ref
    record = records()["oddyssey"]
    assert build.hermes_pack(records()) == (
        "name: otelyssey\n"
        "description: OpenTelemetry agent plugins admitted by otelyssey, at the admitted commits\n"
        "plugins:\n"
        "  - repo: using-system/oddyssey\n"
        '    subdir: "marketplace/oddyssey"\n'
        f'    ref: "{record["sha"]}"\n'
    )
    root_plugin = {**record, "path": ""}
    assert "subdir" not in build.hermes_pack({"oddyssey": root_plugin})
    # a path the store accepts that a plain YAML scalar would cut at the comment
    odd = build.hermes_pack({"oddyssey": {**record, "path": "plugins #x"}})
    assert '    subdir: "plugins #x"\n' in odd


def test_hermes_pack_is_not_written_for_an_empty_store(tmp_path: Path):
    root = tmp_path
    (root / ".store").mkdir()
    (root / "README.md").write_text(EMPTY_README)
    (root / "hermes-pack.yaml").write_text("name: stale\nplugins: []\n")
    assert "hermes-pack.yaml" in build.build(root, check=True)
    build.build(root, check=False)
    assert not (root / "hermes-pack.yaml").exists()
    assert build.build(root, check=True) == []


def test_plugin_page_carries_the_facts():
    page = build.plugin_page(records()["oddyssey"])
    assert page.startswith("# oddyssey\n")
    # the repository first among the facts; the admission issue is not a fact of the plugin
    assert page.split("\n\n")[2].startswith("- Repository: [using-system/oddyssey](")
    assert "Admitted from" not in page and "issues/1" not in page
    for fragment in (
        "- Categories: `observability`, `instrumentation`",
        "https://github.com/using-system/oddyssey",
        "1.13.0 (`v1.13.0`, commit `111111111111`)",
        "MIT",
        "claude plugin marketplace add using-system/otelyssey",
        "claude plugin install oddyssey@otelyssey",
        "copilot plugin install oddyssey@otelyssey",
        "codex plugin marketplace add using-system/otelyssey",
        "codex plugin add oddyssey@otelyssey",
        "grok plugin marketplace add using-system/otelyssey",
        "grok plugin install oddyssey --trust",
        '"chat.plugins.marketplaces": ["using-system/otelyssey"]',
        "apm marketplace add using-system/otelyssey",
        "apm install oddyssey@otelyssey --target copilot",
    ):
        assert fragment in page, fragment
    # Kiro imports a power from a repository url: only a plugin at the repository's root
    assert "Import power from GitHub" not in page
    root_plugin = {**records()["oddyssey"], "path": ""}
    assert "Import power from GitHub, `https://github.com/using-system/oddyssey`" in (
        build.plugin_page(root_plugin)
    )


def test_repository_install_lines_pin_the_commit_and_follow_the_path():
    record = records()["oddyssey"]
    sha = record["sha"]
    page = build.plugin_page(record)
    assert f"hermes plugins install using-system/oddyssey/marketplace/oddyssey --ref {sha}" in page
    assert "hermes plugins enable oddyssey" in page
    assert (
        "hermes plugins pack install "
        "https://raw.githubusercontent.com/using-system/otelyssey/main/hermes-pack.yaml\n"
        "hermes plugins install using-system/oddyssey/marketplace/oddyssey --ref"
    ) in page
    # OpenClaw installs the directory of a clone at the sha: its git route wants a native
    # package and its marketplace route drops the path (verified 2026-09-21 on 2026.9.5)
    assert (
        "openclaw plugins install ./oddyssey/marketplace/oddyssey --force --accept-capabilities"
    ) in page
    assert "--marketplace" not in page and "git:" not in page
    assert (
        f"git clone https://github.com/using-system/oddyssey && git -C oddyssey checkout {sha}"
        in page
    )
    assert (
        "mkdir -p ~/.vibe/plugins/oddyssey && "
        "cp -r ./oddyssey/marketplace/oddyssey/. ~/.vibe/plugins/oddyssey"
    ) in page
    root = build.plugin_page({**record, "path": ""})
    assert f"hermes plugins install using-system/oddyssey --ref {sha}" in root
    assert "openclaw plugins install ./oddyssey --force --accept-capabilities" in root
    assert "cp -r ./oddyssey/. ~/.vibe/plugins/oddyssey" in root
    # a path the store accepts but a shell would split: quoted on the lines that carry it
    odd = build.plugin_page({**record, "path": "my plugins/otel"})
    assert "hermes plugins install 'using-system/oddyssey/my plugins/otel' --ref" in odd
    assert "cp -r ./'oddyssey/my plugins/otel'/. ~/.vibe/plugins/oddyssey" in odd
    assert "openclaw plugins install ./'oddyssey/my plugins/otel' --force" in odd


def test_readme_install_block_carries_the_pack_url():
    # the README's head is prose: the literal there must not drift from the constant
    readme = (FIXTURES.parent.parent / "README.md").read_text(encoding="utf-8")
    assert build.HERMES_PACK_URL in readme


def test_readme_list_groups_the_plugins_by_category_with_live_badges():
    text = build.readme_list(records())
    # listed once, under the principal category; the other named in the line
    assert text.startswith("### 🔭 Observability\n\nRead it back: ")
    assert f"### {build.CATEGORY_ICONS['instrumentation']} Instrumentation" not in text
    (tagline, blank_after_tagline, entry, badges, blank) = text.splitlines()[2:7]
    assert tagline == build.CATEGORY_TAGLINES["observability"] and blank_after_tagline == ""
    # the owner's avatar, then the name linked to the page, not to the repository
    assert entry.startswith(
        '- <img src="https://github.com/using-system.png?size=40" width="20" height="20" '
        'alt=""> **[oddyssey](marketplace/oddyssey/README.md)** by '
    )
    assert " — " in entry and entry.endswith(" · also in Instrumentation  ")
    assert "https://github.com/using-system/oddyssey" not in entry
    assert "[install]" not in text
    # four badges, each its color, none a link
    assert badges.count('<a href="#">') == 4 and badges.endswith('alt="license"></a>')
    single = {**records()["oddyssey"], "categories": ["observability"]}
    assert "also" not in build.readme_entry(single)
    kinds = ("stars", "version", "last-commit", "license")
    record = records()["oddyssey"]
    assert badges == "&nbsp;&nbsp;".join(build.badge(k, record) for k in kinds)
    # the stars badge: a star drawn by shields from an inline svg, no word, the count
    assert badges.startswith(
        '<a href="#"><img src="https://img.shields.io/github/stars/using-system/oddyssey?'
        "style=flat-square&labelColor=2b2b2b&label=&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2C"
    )
    assert "&color=e3b341" in badges and "logo=github" not in badges
    assert "color=3b7dd8" in badges and "color=2ea44f" in badges and "color=6b6b6b" in badges
    for absent in ("created-at", "forks", "watchers"):
        assert absent not in text
    assert blank == ""
    assert text.endswith('alt="license"></a>\n\n') and "\n\n\n" not in text
    assert "Stars" not in text and "| " not in text


def test_version_badge_is_static_and_escapes_shields_separators():
    record = {**records()["oddyssey"], "version": "1.0.0-rc_1"}
    assert 'src="https://img.shields.io/badge/version-1.0.0--rc__1-3b7dd8?' in (
        build.badge("version", record)
    )
    assert "github/v/release" not in build.badge("version", record)


def test_every_category_has_a_title_an_icon_and_a_tagline():
    for table in (build.CATEGORY_TITLES, build.CATEGORY_ICONS, build.CATEGORY_TAGLINES):
        assert set(table) == set(store.CATEGORIES)


def test_readme_list_orders_the_categories_as_the_store_does_and_skips_empty_ones():
    first = records()["oddyssey"]
    second = {**first, "name": "col-b", "categories": ["collector"], "repository": "a/col-b"}
    third = {**first, "name": "col-a", "categories": ["collector"], "repository": "a/col-a"}
    text = build.readme_list({"oddyssey": first, "col-b": second, "col-a": third})
    headings = [line for line in text.splitlines() if line.startswith("### ")]
    assert headings == ["### 🚢 Collector", "### 🔭 Observability"]
    # two entries in one category, after the tagline: name order, one blank line between them
    lines = text.splitlines()
    assert lines[2] == build.CATEGORY_TAGLINES["collector"] and lines[3] == ""
    assert "**[col-a](" in lines[4] and lines[5].startswith("<a ") and lines[6] == ""
    assert "**[col-b](" in lines[7] and lines[8].startswith("<a ") and lines[9] == ""
    assert lines[10] == "### 🔭 Observability"


def test_readme_list_of_an_empty_store_says_so():
    assert build.readme_list({}) == "No plugin listed yet.\n"


def test_readme_list_escapes_markdown_in_the_free_text():
    record = dict(records()["oddyssey"])
    record["description"] = "a [b](c) <d>\ne"
    record["author"] = {"name": "x_y"}
    entry = build.readme_list({"oddyssey": record}).splitlines()[4]
    assert "a \\[b\\](c) \\<d\\> e" in entry
    assert " by x\\_y — " in entry


def test_splice_replaces_only_between_markers():
    text = "intro\n\n<!-- otelyssey:plugins -->\nold\n<!-- /otelyssey:plugins -->\n\noutro\n"
    out = build.splice(text, "new\n")
    assert out == text.replace("old", "new")


def test_build_is_idempotent(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    first = build.build(root, check=False)
    assert set(first) == {
        "marketplace.json",
        ".claude-plugin/marketplace.json",
        ".agents/plugins/marketplace.json",
        ".grok-plugin/marketplace.json",
        "hermes-pack.yaml",
        "marketplace/oddyssey/README.md",
        "README.md",
    }
    codex = json.loads((root / ".agents" / "plugins" / "marketplace.json").read_text())
    assert codex["plugins"][0]["source"]["source"] == "git-subdir"
    assert (root / "hermes-pack.yaml").read_text().startswith("name: otelyssey\n")
    # Grok Build reads the Codex shape, at its own place
    assert (root / ".grok-plugin" / "marketplace.json").read_text() == (
        root / ".agents" / "plugins" / "marketplace.json"
    ).read_text()
    assert build.build(root, check=True) == []
    # Copilot CLI looks at the root first, Claude Code and VS Code in .claude-plugin/: one content
    assert (root / "marketplace.json").read_bytes() == (
        root / ".claude-plugin" / "marketplace.json"
    ).read_bytes()
    assert build.main(["--check", "--root", str(root)]) == 0


def test_build_on_an_empty_store(tmp_path: Path):
    (tmp_path / ".store").mkdir()
    (tmp_path / "README.md").write_text(EMPTY_README)
    assert build.build(tmp_path, check=False) == [
        ".agents/plugins/marketplace.json",
        ".claude-plugin/marketplace.json",
        ".grok-plugin/marketplace.json",
        "README.md",
        "marketplace.json",
    ]
    manifest = json.loads((tmp_path / ".claude-plugin" / "marketplace.json").read_text())
    assert manifest["plugins"] == []
    assert not (tmp_path / "marketplace").exists()


def test_check_fails_when_an_artifact_is_stale(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    build.build(root, check=False)
    (root / ".claude-plugin" / "marketplace.json").write_text("{}\n")
    assert build.main(["--check", "--root", str(root)]) == 1
    build.build(root, check=False)
    (root / "marketplace.json").write_text("{}\n")
    assert build.main(["--check", "--root", str(root)]) == 1
    build.build(root, check=False)
    (root / ".agents" / "plugins" / "marketplace.json").write_text("{}\n")
    assert build.main(["--check", "--root", str(root)]) == 1
    build.build(root, check=False)
    (root / "hermes-pack.yaml").write_text("name: x\n")
    assert build.main(["--check", "--root", str(root)]) == 1
    build.build(root, check=False)
    (root / ".grok-plugin" / "marketplace.json").write_text("{}\n")
    assert build.main(["--check", "--root", str(root)]) == 1


def test_build_removes_the_page_of_a_withdrawn_plugin(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    build.build(root, check=False)
    (root / ".store" / "oddyssey.json").unlink()
    assert "marketplace/oddyssey/README.md" in build.build(root, check=False)
    assert not (root / "marketplace" / "oddyssey").exists()


def test_plugin_page_escapes_markdown_in_the_license_and_the_version():
    record = {
        **records()["oddyssey"],
        "license": "MIT - [Download the installer](https://evil.example/x.sh) <img src=x>",
        "version": "1.0.1[changelog](https://evil.example/c)<img/src=y>",
    }
    page = build.plugin_page(record)
    # every bracket and angle bracket is escaped: no link, no tag survives
    assert "\\[Download the installer\\](https://evil.example/x.sh) \\<img src=x\\>" in page
    assert "1.0.1\\[changelog\\](https://evil.example/c)\\<img/src=y\\>" in page
    assert " [Download" not in page and " <img" not in page and ")<img" not in page
    # a backslash in the input is escaped too: `\[` would otherwise come out as `\\[`, an
    # escaped backslash and a live bracket (checked with GitHub's renderer)
    evil = {**records()["oddyssey"], "license": "MIT \\[Download\\](https://evil.example/x.sh)"}
    page = build.plugin_page(evil)
    assert "MIT \\\\\\[Download\\\\\\](https://evil.example/x.sh)" in page
    assert "\\\\[" not in page.replace("\\\\\\[", "")


def test_plugin_page_escapes_markdown_in_the_author_and_the_description():
    record = dict(records()["oddyssey"])
    record["author"] = {"name": "x [y] <z>"}
    record["description"] = "a  *b*\n_c_ `d`"
    page = build.plugin_page(record)
    assert page.count("x \\[y\\] \\<z\\>") == 1
    assert "x [y] <z>" not in page
    assert "a \\*b\\* \\_c\\_ \\`d\\`\n" in page


def test_text_collapses_whitespace_and_escapes_markdown():
    assert build.text(" a\n\tb ") == "a b"
    assert build.text("[<*_`>]") == "\\[\\<\\*\\_\\`\\>\\]"


@pytest.mark.parametrize(
    "text", ["# x\n\n<!-- /otelyssey:plugins -->\n", "# x\n\n<!-- otelyssey:plugins -->\n"]
)
def test_splice_names_a_missing_marker(text):
    with pytest.raises(SystemExit, match="README.md: the list markers are missing"):
        build.splice(text, "new\n")


def test_withdrawal_removes_a_page_directory_with_other_files(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    build.build(root, check=False)
    (root / "marketplace" / "oddyssey" / "stray.txt").write_text("x")
    (root / ".store" / "oddyssey.json").unlink()
    assert "marketplace/oddyssey/README.md" in build.build(root, check=False)
    assert not (root / "marketplace" / "oddyssey").exists()
