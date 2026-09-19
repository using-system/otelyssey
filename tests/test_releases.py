import json
from pathlib import Path

from scripts import releases

TAGS = {"v1.13.0": "1" * 40, "v1.14.0": "2" * 40}


def store_with(tmp_path: Path) -> Path:
    src = Path(__file__).parent / "fixtures" / "store-root" / ".store" / "oddyssey.json"
    (tmp_path / ".store").mkdir()
    (tmp_path / ".store" / "oddyssey.json").write_bytes(src.read_bytes())
    return tmp_path


def fake_validate(result: dict):
    def validate(repository, tag, path, name, version, workdir):
        assert version == ""
        return result

    return validate


def test_unchanged_when_the_latest_tag_is_the_admitted_one(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: {"v1.13.0": "1" * 40})
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "unchanged"


def test_updated_when_a_newer_tag_validates(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    passing = {"sha": "2" * 40, "manifest": {"version": "1.14.0"}, "errors": [], "notes": []}
    monkeypatch.setattr(releases.validate, "validate", fake_validate(passing))
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "updated"
    record = json.loads((root / ".store" / "oddyssey.json").read_text())
    assert (record["ref"], record["sha"], record["version"]) == ("v1.14.0", "2" * 40, "1.14.0")


def test_failed_keeps_the_record(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    failing = {"sha": "2" * 40, "manifest": {}, "errors": ["plugin.json: missing"], "notes": []}
    monkeypatch.setattr(releases.validate, "validate", fake_validate(failing))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["tag"]) == ("failed", "v1.14.0")
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"


def test_unreadable_tags_are_a_failure_not_a_crash(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)

    def failing(repository):
        raise releases.gitrepo.RepositoryError("gone")

    monkeypatch.setattr(releases.gitrepo, "list_tags", failing)
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert result["status"] == "failed"
    assert "gone" in result["errors"][0]
