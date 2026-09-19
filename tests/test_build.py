import json
from pathlib import Path

from scripts import build, store

FIXTURES = Path(__file__).parent / "fixtures"


def records():
    return store.load_store(FIXTURES / "store-root")


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
