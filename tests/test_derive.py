import json
from pathlib import Path

from scripts import derive, store

CANDIDATE = {
    "repository": "contoso/my-otel-plugin",
    "path": "plugins/otel",
    "submitted_in": 7,
    "ref": "v1.2.0",
    "sha": "1" * 40,
}
MANIFEST = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": "my-otel-plugin",
    "version": "1.2.0",
    "description": "  Queries   traces\nin Tempo. ",
    "author": {
        "name": "Contoso",
        "url": "https://contoso.example",
        "email": "otel@contoso.example",
    },
    "homepage": "https://contoso.example/plugin",
    "license": "Apache-2.0",
    "keywords": ["OpenTelemetry", "tempo", ""],
}
RAW = {
    "description": "The Contoso plugins",
    "license": {"spdx_id": "MIT"},
    "homepage": "https://contoso.example",
    "topics": ["observability", "otel"],
    "owner": {"login": "contoso", "html_url": "https://github.com/contoso"},
}


def validation(manifest: dict) -> dict:
    return {"sha": "1" * 40, "manifest": manifest, "errors": [], "notes": []}


def test_the_manifest_is_the_source_of_every_field():
    record, errors, filled = derive.derive(CANDIDATE, validation(MANIFEST), derive.metadata(RAW))
    assert errors == [] and filled == []
    assert record == {
        "name": "my-otel-plugin",
        "description": "Queries traces in Tempo.",
        "repository": "contoso/my-otel-plugin",
        "path": "plugins/otel",
        "ref": "v1.2.0",
        "sha": "1" * 40,
        "version": "1.2.0",
        "author": {
            "name": "Contoso",
            "email": "otel@contoso.example",
            "url": "https://contoso.example",
        },
        "license": "Apache-2.0",
        "homepage": "https://contoso.example/plugin",
        "keywords": ["opentelemetry", "tempo"],
        "submitted_in": 7,
    }
    # the store's order, without the fields the admission adds
    assert list(record) == [
        f for f in store.FIELDS if f not in ("category", "admitted_at", "stats")
    ]
    assert (
        store.validate_record(
            {
                **record,
                "category": "backend",
                "admitted_at": "2026-09-20",
                "stats": {
                    "stars": 0,
                    "forks": 0,
                    "watchers": 0,
                    "refreshed_at": "2026-09-20T00:00:00Z",
                },
            }
        )
        == []
    )


def test_the_repository_fills_what_the_manifest_leaves_out():
    bare = {"$schema": MANIFEST["$schema"], "name": "my-otel-plugin", "version": "1.2.0"}
    record, errors, filled = derive.derive(CANDIDATE, validation(bare), derive.metadata(RAW))
    assert errors == []
    assert filled == ["description", "license", "homepage", "author", "keywords"]
    assert record["description"] == "The Contoso plugins"
    assert record["license"] == "MIT"
    assert record["homepage"] == "https://contoso.example"
    assert record["author"] == {"name": "contoso", "url": "https://github.com/contoso"}
    assert record["keywords"] == ["observability", "otel"]


def test_what_neither_gives_is_an_error_the_contributor_fixes_in_the_manifest():
    bare = {"$schema": MANIFEST["$schema"], "name": "my-otel-plugin", "version": "1.2.0"}
    empty = derive.metadata({"license": {"spdx_id": "NOASSERTION"}, "owner": {}})
    record, errors, filled = derive.derive(CANDIDATE, validation(bare), empty)
    assert errors == [
        "plugin.json: no description, and the repository has none either: add a description",
        "plugin.json: no license, and the repository has none either: add a license",
        "plugin.json: no author, and the repository's owner could not be read",
    ]
    assert record["keywords"] == [] and filled == []


def test_an_author_or_a_homepage_url_the_store_refuses_is_dropped_not_copied():
    manifest = {**MANIFEST, "homepage": "ftp://x", "author": {"name": "C", "url": "http://x"}}
    record, errors, _ = derive.derive(CANDIDATE, validation(manifest), derive.metadata(RAW))
    assert errors == []
    assert record["homepage"] == ""
    assert record["author"] == {"name": "C"}


def test_metadata_reads_the_api_object_defensively():
    assert derive.metadata({}) == {
        "description": "",
        "license": "",
        "homepage": "",
        "topics": [],
        "owner": {"name": "", "url": ""},
    }
    assert derive.metadata({"license": None, "topics": [1, "a"], "owner": None})["topics"] == ["a"]


def test_main_writes_the_derivation(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.setattr(derive, "fetch_metadata", lambda repository, token: derive.metadata(RAW))
    (tmp_path / "candidate.json").write_text(json.dumps({"candidate": CANDIDATE, "errors": []}))
    (tmp_path / "validation.json").write_text(json.dumps(validation(MANIFEST)))
    out = tmp_path / "derived.json"
    code = derive.main(
        [
            "--candidate",
            str(tmp_path / "candidate.json"),
            "--validation",
            str(tmp_path / "validation.json"),
            "--out",
            str(out),
        ]
    )
    assert code == 0
    data = json.loads(out.read_text())
    assert data["errors"] == [] and data["record"]["name"] == "my-otel-plugin"


def test_main_exits_2_when_the_plugin_does_not_validate_or_the_api_fails(
    tmp_path: Path, capsys, monkeypatch
):
    (tmp_path / "candidate.json").write_text(json.dumps({"candidate": CANDIDATE, "errors": []}))
    (tmp_path / "validation.json").write_text(json.dumps({**validation(MANIFEST), "errors": ["x"]}))
    args = [
        "--candidate",
        str(tmp_path / "candidate.json"),
        "--validation",
        str(tmp_path / "validation.json"),
        "--out",
        str(tmp_path / "d.json"),
    ]
    assert derive.main(args) == 2
    (tmp_path / "validation.json").write_text(json.dumps(validation(MANIFEST)))

    def failing(repository, token):
        raise TimeoutError("slow")

    monkeypatch.setattr(derive, "fetch_metadata", failing)
    assert derive.main(args) == 2
    assert not (tmp_path / "d.json").exists()
    assert "metadata unreadable" in capsys.readouterr().err
