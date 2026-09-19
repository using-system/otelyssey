import json
from pathlib import Path

from scripts import validate

PLUGINS = Path(__file__).parent / "fixtures" / "plugins"


def test_valid_manifest_has_no_errors():
    manifest, errors = validate.check_manifest(PLUGINS / "valid", "my-otel-plugin", "1.2.0")
    assert errors == []
    assert manifest["name"] == "my-otel-plugin"


def test_empty_expected_version_skips_the_match():
    _, errors = validate.check_manifest(PLUGINS / "valid", "my-otel-plugin", "")
    assert errors == []


def test_empty_expected_version_still_requires_a_version(tmp_path: Path):
    manifest = json.loads((PLUGINS / "valid" / "plugin.json").read_text())
    del manifest["version"]
    (tmp_path / "plugin.json").write_text(json.dumps(manifest))
    _, errors = validate.check_manifest(tmp_path, "my-otel-plugin", "")
    assert errors == ["plugin.json: version missing"]
    (tmp_path / "plugin.json").write_text(json.dumps({**manifest, "version": ""}))
    _, errors = validate.check_manifest(tmp_path, "my-otel-plugin", "")
    assert errors == ["plugin.json: version missing"]


def test_name_and_version_must_match_the_submission():
    _, errors = validate.check_manifest(PLUGINS / "valid", "other", "9.9.9")
    assert any("name" in e for e in errors)
    assert any("version" in e for e in errors)


def test_bad_name_is_reported_against_the_schema():
    _, errors = validate.check_manifest(PLUGINS / "badname", "My_Plugin", "1.2.0")
    assert any("name" in e and "schema" in e for e in errors)


def test_unknown_root_key_is_reported_against_the_schema(tmp_path: Path):
    text = (PLUGINS / "valid" / "plugin.json").read_text().replace('"license"', '"displayName"')
    (tmp_path / "plugin.json").write_text(text)
    _, errors = validate.check_manifest(tmp_path, "my-otel-plugin", "1.2.0")
    assert any("displayName" in e and "schema" in e for e in errors)


def test_legacy_layout_is_named():
    _, errors = validate.check_manifest(PLUGINS / "legacy", "legacy-plugin", "0.1.0")
    assert any(".claude-plugin/plugin.json" in e for e in errors)


def test_layout_notes_are_not_errors():
    assert validate.check_layout(PLUGINS / "valid") == ([], [])
    errors, notes = validate.check_layout(PLUGINS / "extras")
    assert errors == ["skills/empty: no SKILL.md"]
    assert any(".claude-plugin" in n for n in notes)
    assert any("commands" in n for n in notes)
    assert not any("com.example.tool" in n for n in notes)


def test_layout_notes_ignore_undefined_root_files(tmp_path: Path):
    (tmp_path / "plugin.json").write_text("{}")
    (tmp_path / "CLAUDE.md").write_text("Plugin documentation")
    (tmp_path / "CITATION.cff").write_text("cff-version: 1.2.0")
    (tmp_path / "unexpected-directory").mkdir()

    errors, notes = validate.check_layout(tmp_path)

    assert errors == []
    assert notes == ["unexpected-directory: not an entry the Agent Plugins format defines"]


def test_validate_names_an_unreadable_repository(tmp_path: Path, monkeypatch):
    def failing(repository):
        raise validate.gitrepo.RepositoryError("repository not found")

    monkeypatch.setattr(validate.gitrepo, "list_tags", failing)
    result = validate.validate("contoso/gone", "v1.0.0", "", "x", "1.0.0", tmp_path)
    assert result["sha"] is None
    assert result["errors"] == ["repository: repository not found"]
    assert result["notes"] == []


def test_validate_refuses_a_path_outside_the_checkout(tmp_path: Path, monkeypatch):
    def must_not_be_called(repository):
        raise AssertionError("must not be called")

    monkeypatch.setattr(validate.gitrepo, "list_tags", must_not_be_called)
    for path in ("/etc", "../x"):
        result = validate.validate("contoso/x", "v1.0.0", path, "x", "1.0.0", tmp_path)
        assert result["errors"] == ["path: not a relative directory inside the repository"]
