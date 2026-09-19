import json
from pathlib import Path

from scripts import build, store

FIXTURES = Path(__file__).parent / "fixtures"
EMPTY_README = "# x\n\n<!-- otelyssey:table -->\n<!-- /otelyssey:table -->\n"


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
    assert entry["source"] == {
        "source": "github",
        "repo": "using-system/oddyssey",
        "path": "marketplace/oddyssey",
        "ref": "v1.13.0",
        "sha": "1" * 40,
    }
    assert entry["version"] == "1.13.0"
    assert entry["category"] == "workflow"


def test_root_plugin_has_no_path():
    record = dict(records()["oddyssey"])
    record["path"] = ""
    [entry] = build.marketplace_json({"oddyssey": record})["plugins"]
    assert entry["source"] == {
        "source": "github",
        "repo": "using-system/oddyssey",
        "ref": "v1.13.0",
        "sha": "1" * 40,
    }


def test_render_json_is_stable():
    payload = build.marketplace_json(records())
    assert build.render_json(payload) == json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def test_plugin_page_carries_the_facts():
    page = build.plugin_page(records()["oddyssey"])
    assert page.startswith("# oddyssey\n")
    for fragment in (
        "workflow",
        "https://github.com/using-system/oddyssey",
        "v1.13.0",
        "1.13.0",
        "MIT",
        "claude plugin marketplace add using-system/otelyssey",
        "claude plugin install oddyssey@otelyssey",
        "copilot plugin install oddyssey@otelyssey",
        "https://github.com/using-system/otelyssey/issues/1",
    ):
        assert fragment in page, fragment


def test_readme_table_has_one_row_per_record():
    lines = build.readme_table(records()).splitlines()
    assert lines[0].startswith("| Plugin | Description | Category | Repository | Stars |")
    assert lines[1].startswith("| --- |")
    assert len(lines) == 3
    assert "[oddyssey](marketplace/oddyssey/README.md)" in lines[2]
    assert "[using-system/oddyssey](https://github.com/using-system/oddyssey)" in lines[2]


def test_readme_table_of_an_empty_store_is_the_header():
    assert len(build.readme_table({}).splitlines()) == 2


def test_readme_table_escapes_pipes_and_newlines():
    record = dict(records()["oddyssey"])
    record["description"] = "a | b\nc"
    lines = build.readme_table({"oddyssey": record}).splitlines()
    assert len(lines) == 3
    assert "a \\| b c" in lines[2]


def test_splice_replaces_only_between_markers():
    text = "intro\n\n<!-- otelyssey:table -->\nold\n<!-- /otelyssey:table -->\n\noutro\n"
    out = build.splice(text, "| new |\n")
    assert out == "intro\n\n<!-- otelyssey:table -->\n| new |\n<!-- /otelyssey:table -->\n\noutro\n"


def test_build_is_idempotent(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    first = build.build(root, check=False)
    assert set(first) == {
        ".claude-plugin/marketplace.json",
        "marketplace/oddyssey/README.md",
        "README.md",
    }
    assert build.build(root, check=True) == []
    assert build.main(["--check", "--root", str(root)]) == 0


def test_build_on_an_empty_store(tmp_path: Path):
    (tmp_path / ".store").mkdir()
    (tmp_path / "README.md").write_text(EMPTY_README)
    assert build.build(tmp_path, check=False) == [".claude-plugin/marketplace.json", "README.md"]
    manifest = json.loads((tmp_path / ".claude-plugin" / "marketplace.json").read_text())
    assert manifest["plugins"] == []
    assert not (tmp_path / "marketplace").exists()


def test_check_fails_when_an_artifact_is_stale(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    build.build(root, check=False)
    (root / ".claude-plugin" / "marketplace.json").write_text("{}\n")
    assert build.main(["--check", "--root", str(root)]) == 1


def test_build_removes_the_page_of_a_withdrawn_plugin(tmp_path: Path):
    root = root_with_fixture(tmp_path)
    build.build(root, check=False)
    (root / ".store" / "oddyssey.json").unlink()
    assert "marketplace/oddyssey/README.md" in build.build(root, check=False)
    assert not (root / "marketplace" / "oddyssey").exists()
