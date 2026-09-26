import json
from pathlib import Path

from scripts import derive, resync, store, validate
from tests.test_derive import MANIFEST, RAW

RECORD = {
    "name": "my-otel-plugin",
    "description": "typed in the form",
    "categories": ["backend"],
    "repository": "contoso/my-otel-plugin",
    "path": "",
    "ref": "v1.2.0",
    "sha": "1" * 40,
    "version": "1.2.0",
    "author": {"name": "Typed"},
    "license": "MIT",
    "homepage": "",
    "keywords": ["typed"],
    "skills": False,
    "mcp": {},
    "submitted_in": 7,
    "admitted_at": "2026-09-19",
    "stats": {"stars": 0, "forks": 0, "watchers": 0, "refreshed_at": "2026-09-20T00:00:00Z"},
}


def a_store(tmp_path: Path, record: dict) -> Path:
    (tmp_path / ".store").mkdir()
    store.write_record(tmp_path, record)
    return tmp_path


def validating(manifest: dict):
    return lambda *a, **k: {
        "sha": "1" * 40,
        "manifest": manifest,
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }


def test_a_record_is_rewritten_from_its_manifest(tmp_path: Path, monkeypatch):
    root = a_store(tmp_path, RECORD)
    monkeypatch.setattr(validate, "validate", validating(MANIFEST))
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata(RAW))
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work", None)
    assert (rewritten, kept, skipped) == (["my-otel-plugin"], {}, {})
    record = json.loads((root / ".store" / "my-otel-plugin.json").read_text())
    assert record["description"] == "Queries traces in Tempo."
    assert record["categories"] == ["backend"]


def test_an_unchanged_record_is_not_written(tmp_path: Path, monkeypatch):
    root = a_store(tmp_path, RECORD)
    monkeypatch.setattr(validate, "validate", validating(MANIFEST))
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata(RAW))
    resync.resync_store(root, tmp_path / "work", None)
    before = (root / ".store" / "my-otel-plugin.json").stat().st_mtime_ns
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work2", None)
    assert (rewritten, kept, skipped) == ([], {}, {})
    assert (root / ".store" / "my-otel-plugin.json").stat().st_mtime_ns == before


def test_a_record_that_no_longer_validates_or_whose_api_fails_is_skipped(
    tmp_path: Path, monkeypatch
):
    root = a_store(tmp_path, RECORD)
    monkeypatch.setattr(
        validate,
        "validate",
        lambda *a, **k: {
            "sha": None,
            "manifest": {},
            "skills": False,
            "mcp": {},
            "errors": ["gone"],
            "notes": [],
        },
    )
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work", None)
    assert (rewritten, kept, skipped) == ([], {}, {"my-otel-plugin": "gone"})
    monkeypatch.setattr(validate, "validate", validating(MANIFEST))

    def failing(repository, token):
        raise TimeoutError("slow")

    monkeypatch.setattr(derive, "fetch_metadata", failing)
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work2", None)
    assert skipped == {"my-otel-plugin": "metadata unreadable (slow)"}
    assert json.loads((root / ".store" / "my-otel-plugin.json").read_text()) == RECORD


def test_a_field_neither_source_gives_is_kept_and_reported(tmp_path: Path, monkeypatch):
    root = a_store(tmp_path, RECORD)
    bare = {"$schema": MANIFEST["$schema"], "name": "my-otel-plugin", "version": "1.2.0"}
    monkeypatch.setattr(validate, "validate", validating(bare))
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata({}))
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work", None)
    assert kept == {"my-otel-plugin": ["description", "license", "author"]}
    assert rewritten == ["my-otel-plugin"] and skipped == {}
    record = json.loads((root / ".store" / "my-otel-plugin.json").read_text())
    assert record["author"] == {"name": "Typed"} and record["keywords"] == []


def test_a_manifest_the_store_refuses_leaves_the_record_as_it_was(tmp_path: Path, monkeypatch):
    root = a_store(tmp_path, RECORD)
    monkeypatch.setattr(validate, "validate", validating({**MANIFEST, "description": "red \x1b"}))
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata(RAW))
    rewritten, kept, skipped = resync.resync_store(root, tmp_path / "work", None)
    assert rewritten == [] and "refused by the store" in skipped["my-otel-plugin"]
    assert json.loads((root / ".store" / "my-otel-plugin.json").read_text()) == RECORD


def test_main_exits_1_when_something_was_kept_or_skipped(tmp_path: Path, monkeypatch, capsys):
    root = a_store(tmp_path, RECORD)
    monkeypatch.setattr(validate, "validate", validating(MANIFEST))
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata(RAW))
    assert resync.main(["--root", str(root), "--workdir", str(tmp_path / "w1")]) == 0
    assert capsys.readouterr().out == "rewritten: my-otel-plugin\n"
    monkeypatch.setattr(
        validate,
        "validate",
        lambda *a, **k: {
            "sha": None,
            "manifest": {},
            "skills": False,
            "mcp": {},
            "errors": ["gone"],
            "notes": [],
        },
    )
    assert resync.main(["--root", str(root), "--workdir", str(tmp_path / "w2")]) == 1
    out = capsys.readouterr()
    assert out.out == "nothing to rewrite\n" and out.err == "skipped: my-otel-plugin (gone)\n"
