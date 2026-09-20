import json
from pathlib import Path

import pytest

from scripts import store

RECORD = {
    "name": "oddyssey",
    "description": "Observability-Driven Development for CLI coding agents.",
    "categories": ["observability", "instrumentation"],
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
        ("categories", ["misc"], "categories"),
        ("categories", [], "categories"),
        ("categories", ["backend", "backend"], "categories"),
        ("categories", "backend", "categories"),
        ("repository", "not-a-repo", "repository"),
        ("sha", "abc", "sha"),
        ("stats", {"stars": 1}, "stats"),
        ("homepage", "javascript:alert(1)", "homepage"),
        ("homepage", "https://contoso.example/a b", "homepage"),
        ("author", {"name": "x", "url": "javascript:alert(1)"}, "author.url"),
        ("author", {"name": "x", "email": "a b@example"}, "author.email"),
        ("author", {"name": "x", "email": ""}, "author.email"),
        ("author", {"name": "x", "url": 1}, "author.url"),
        ("author", {"name": "x", "email": None}, "author.email"),
        ("ref", "v1.0.0\n", "ref: control character"),
        ("version", "1.0.0\nx", "version: control character"),
        ("description", "a \x1b[31mred", "description: control character"),
        ("name", "a\x7fb", "name: control character"),
        ("path", "a\tb", "path: control character"),
        ("license", "MIT\r", "license: control character"),
        ("homepage", "https://e.example/\x01", "homepage: control character"),
        ("keywords", ["ok", "bad\n"], "keywords: control character"),
        ("author", {"name": "x\n"}, "author.name: control character"),
        ("author", {"name": "x", "email": "a@b\x00"}, "author.email: control character"),
        ("author", {"name": "x", "url": "https://e.example/\n"}, "author.url: control character"),
        (
            "author",
            {"name": "x", "url": "https://e.example/)[x](https://evil.example)"},
            "author.url",
        ),
        ("homepage", "https://e.example/<a>", "homepage"),
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


def test_author_email_and_url_are_optional():
    author = {"name": "x", "email": "x@example.com", "url": "https://contoso.example"}
    assert store.validate_record({**RECORD, "author": author}) == []
    assert store.validate_record({**RECORD, "homepage": ""}) == []
