import json
from pathlib import Path

import pytest

from scripts import store

RECORD = {
    "name": "oddyssey",
    "description": "Observability-Driven Development for CLI coding agents.",
    "category": "workflow",
    "repository": "using-system/oddyssey",
    "path": "marketplace/oddyssey",
    "ref": "v1.13.0",
    "sha": "0" * 40,
    "version": "1.13.0",
    "author": {"name": "using-system", "url": "https://github.com/using-system"},
    "license": "MIT",
    "homepage": "https://github.com/using-system/oddyssey#readme",
    "keywords": ["opentelemetry", "observability"],
    "submitted_in": 1,
    "admitted_at": "2026-09-19",
    "stats": {"stars": 0, "forks": 0, "watchers": 0, "refreshed_at": "2026-09-19T00:00:00Z"},
}


def test_valid_record_has_no_errors():
    assert store.validate_record(RECORD) == []


@pytest.mark.parametrize(
    "field,value,fragment",
    [
        ("name", "Bad_Name", "name"),
        ("category", "misc", "category"),
        ("repository", "not-a-repo", "repository"),
        ("sha", "abc", "sha"),
        ("stats", {"stars": 1}, "stats"),
    ],
)
def test_invalid_field_is_named(field, value, fragment):
    errors = store.validate_record({**RECORD, field: value})
    assert errors and any(fragment in e for e in errors)


def test_missing_field_is_named():
    record = dict(RECORD)
    del record["license"]
    assert any("license" in e for e in store.validate_record(record))


def test_write_and_load_round_trip(tmp_path: Path):
    path = store.write_record(tmp_path, RECORD)
    assert path == tmp_path / ".store" / "oddyssey.json"
    assert json.loads(path.read_text()) == RECORD
    assert store.load_store(tmp_path) == {"oddyssey": RECORD}


def test_write_is_canonical(tmp_path: Path):
    store.write_record(tmp_path, RECORD)
    first = (tmp_path / ".store" / "oddyssey.json").read_bytes()
    store.write_record(tmp_path, dict(reversed(list(RECORD.items()))))
    assert (tmp_path / ".store" / "oddyssey.json").read_bytes() == first


def test_check_reports_a_bad_record(tmp_path: Path, capsys):
    (tmp_path / ".store").mkdir()
    (tmp_path / ".store" / "x.json").write_text(json.dumps({**RECORD, "name": "y"}))
    assert store.main(["--check", "--root", str(tmp_path)]) == 1
    assert "x.json" in capsys.readouterr().err


def test_check_passes_an_empty_store(tmp_path: Path, capsys):
    (tmp_path / ".store").mkdir()
    assert store.main(["--check", "--root", str(tmp_path)]) == 0
    assert "0 record(s), 0 failing" in capsys.readouterr().out


def test_write_rewrites_a_valid_record_canonically(tmp_path: Path):
    (tmp_path / ".store").mkdir()
    loose = tmp_path / ".store" / "oddyssey.json"
    loose.write_text(json.dumps(RECORD))
    assert store.main(["--write", "--root", str(tmp_path)]) == 0
    assert loose.read_text() == store.canonical(RECORD)


def test_check_refuses_a_root_without_a_store(tmp_path: Path, capsys):
    assert store.main(["--check", "--root", str(tmp_path)]) == 2
    assert ".store" in capsys.readouterr().err
