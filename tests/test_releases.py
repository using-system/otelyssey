import json
from pathlib import Path

import pytest

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


PASSING = {"sha": "2" * 40, "manifest": {"version": "1.14.0"}, "errors": [], "notes": []}


def test_a_failed_install_keeps_the_record(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.validate, "validate", fake_validate(PASSING))
    calls = []

    def smoke_fn(name, plugin_dir, workdir):
        calls.append((name, plugin_dir, workdir))
        return {
            "copilot": {"status": "fail", "output": "plugin install exited 1\nno such skill"},
            "claude": {"status": "pass", "output": "claude: installed and listed oddyssey"},
        }

    result = releases.follow(root, tmp_path / "work", smoke_fn=smoke_fn)["oddyssey"]
    assert (result["status"], result["tag"]) == ("failed", "v1.14.0")
    assert result["errors"] == ["install on copilot: fail: no such skill"]
    assert calls == [
        (
            "oddyssey",
            tmp_path / "work" / "oddyssey" / "checkout" / "marketplace" / "oddyssey",
            tmp_path / "work" / "oddyssey" / "smoke",
        )
    ]
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"


def test_a_passing_install_repins_the_record(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.validate, "validate", fake_validate(PASSING))
    hosts = {
        "copilot": {"status": "pass", "output": "ok"},
        "claude": {"status": "pass", "output": "ok"},
    }
    result = releases.follow(root, tmp_path / "work", smoke_fn=lambda *a: hosts)["oddyssey"]
    assert result["status"] == "updated"
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.14.0"


def test_without_smoke_fn_a_validated_tag_is_repinned(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.validate, "validate", fake_validate(PASSING))
    monkeypatch.setattr(releases.smoke, "smoke", lambda *a: pytest.fail("smoke called"))
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "updated"


def test_main_smoke_flag_passes_the_install(tmp_path: Path, monkeypatch, capsys):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.validate, "validate", fake_validate(PASSING))
    failing = {
        "claude": {"status": "unavailable", "output": "the claude CLI is not on this machine"}
    }
    monkeypatch.setattr(releases.smoke, "smoke", lambda *a: failing)
    code = releases.main(
        ["--root", str(root), "--workdir", str(tmp_path / "work"), "--smoke", "--json"]
    )
    assert code == 0
    result = json.loads(capsys.readouterr().out)["oddyssey"]
    assert result["status"] == "failed"
    assert result["errors"] == [
        "install on claude: unavailable: the claude CLI is not on this machine"
    ]


def test_a_record_the_store_refuses_is_a_failed_follow(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    tainted = {**PASSING, "manifest": {"version": "1.14.0\nFOO=bar"}}
    monkeypatch.setattr(releases.validate, "validate", fake_validate(tainted))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["tag"]) == ("failed", "v1.14.0")
    assert any("control character" in e for e in result["errors"])
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"
