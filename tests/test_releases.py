import json
from pathlib import Path

import pytest

from scripts import releases

TAGS = {"v1.13.0": "1" * 40, "v1.14.0": "2" * 40}


@pytest.fixture(autouse=True)
def the_tag_carries_the_manifest(monkeypatch):
    """No network: a tag carries plugin.json unless a test says otherwise, and the repository's
    metadata is empty unless a test gives some."""
    monkeypatch.setattr(releases.gitrepo, "has_file", lambda repository, sha, path: True)
    monkeypatch.setattr(
        releases.derive, "fetch_metadata", lambda repository, token: releases.derive.metadata({})
    )


def store_with(tmp_path: Path) -> Path:
    src = Path(__file__).parent / "fixtures" / "store-root" / ".store" / "oddyssey.json"
    (tmp_path / ".store").mkdir()
    (tmp_path / ".store" / "oddyssey.json").write_bytes(src.read_bytes())
    return tmp_path


def fake_validate(result: dict, at: str = "2" * 40):
    def validate(repository, ref, path, name, version, workdir):
        assert (ref, version) == (at, "")
        return result

    return validate


def untagged(monkeypatch, head: str) -> None:
    """A repository without a release tag, its default branch main at `head`."""
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: {"nightly": "9" * 40})
    monkeypatch.setattr(releases.gitrepo, "default_branch", lambda repository: ("main", head))


def branch_record(root: Path) -> None:
    """The fixture record re-pinned on main at 3*40, as the intake pins an untagged repository."""
    path = root / ".store" / "oddyssey.json"
    record = json.loads(path.read_text())
    path.write_text(json.dumps({**record, "ref": "main", "sha": "3" * 40}))


def test_unchanged_when_the_latest_tag_is_the_admitted_one(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: {"v1.13.0": "1" * 40})
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "unchanged"


def test_updated_when_a_newer_tag_validates(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    passing = {
        "sha": "2" * 40,
        "manifest": {"version": "1.14.0"},
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(passing))
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "updated"
    record = json.loads((root / ".store" / "oddyssey.json").read_text())
    assert (record["ref"], record["sha"], record["version"]) == ("v1.14.0", "2" * 40, "1.14.0")


def test_a_repin_reads_the_derived_fields_from_the_new_manifest(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    before = json.loads((root / ".store" / "oddyssey.json").read_text())
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    manifest = {
        "name": "oddyssey",
        "version": "1.14.0",
        "description": "A new description",
        "keywords": ["otel", "odd"],
        "author": {"name": "New Author", "url": "https://new.example"},
        "license": "Apache-2.0",
    }
    passing = {
        "sha": "2" * 40,
        "manifest": manifest,
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(passing))
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "updated"
    record = json.loads((root / ".store" / "oddyssey.json").read_text())
    assert record["description"] == "A new description"
    assert record["keywords"] == ["otel", "odd"]
    assert record["author"] == {"name": "New Author", "url": "https://new.example"}
    assert record["license"] == "Apache-2.0"
    # the manifest has no homepage and the repository none either: an empty derived value
    assert record["homepage"] == ""
    for field in ("name", "categories", "submitted_in", "admitted_at", "stats"):
        assert record[field] == before[field]


def test_a_repin_keeps_a_field_the_new_manifest_and_the_repository_lack(
    tmp_path: Path, monkeypatch
):
    root = store_with(tmp_path)
    before = json.loads((root / ".store" / "oddyssey.json").read_text())
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    bare = {"name": "oddyssey", "version": "1.14.0"}
    passing = {
        "sha": "2" * 40,
        "manifest": bare,
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(passing))

    def unreachable(repository, token):
        raise TimeoutError("slow")

    monkeypatch.setattr(releases.derive, "fetch_metadata", unreachable)
    assert releases.follow(root, tmp_path / "work")["oddyssey"]["status"] == "updated"
    record = json.loads((root / ".store" / "oddyssey.json").read_text())
    assert (record["ref"], record["sha"], record["version"]) == ("v1.14.0", "2" * 40, "1.14.0")
    # the record's values stood in for the repository's: nothing the repository had given is
    # emptied by an API that could not be read
    for field in ("description", "license", "author", "homepage", "keywords"):
        assert record[field] == before[field]


def test_failed_keeps_the_record(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    failing = {
        "sha": "2" * 40,
        "manifest": {},
        "skills": False,
        "mcp": {},
        "errors": ["plugin.json: missing"],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(failing))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("failed", "v1.14.0")
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"


def test_untagged_unchanged_when_the_head_is_the_admitted_commit(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    untagged(monkeypatch, "3" * 40)
    monkeypatch.setattr(releases.validate, "validate", lambda *a: pytest.fail("validated"))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("unchanged", "main")


def test_untagged_unchanged_when_the_head_moved_without_a_version_bump(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    untagged(monkeypatch, "4" * 40)
    same = {
        "sha": "4" * 40,
        "manifest": {"version": "1.13.0"},
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(same, at="4" * 40))
    monkeypatch.setattr(releases.smoke, "smoke", lambda *a: pytest.fail("smoke called"))
    result = releases.follow(root, tmp_path / "work", smoke_fn=releases.smoke.smoke)["oddyssey"]
    assert (result["status"], result["ref"]) == ("unchanged", "main")
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["sha"] == "3" * 40


def test_untagged_broken_head_without_a_version_bump_is_not_a_failure(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    untagged(monkeypatch, "4" * 40)
    broken = {
        "sha": "4" * 40,
        "manifest": {},
        "skills": False,
        "mcp": {},
        "errors": ["plugin.json: not JSON"],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(broken, at="4" * 40))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["errors"]) == ("unchanged", [])
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["sha"] == "3" * 40


def test_untagged_broken_head_with_a_version_bump_is_a_failure(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    untagged(monkeypatch, "4" * 40)
    broken = {
        "sha": "4" * 40,
        "manifest": {"version": "1.14.0"},
        "skills": False,
        "mcp": {},
        "errors": ["plugin.json: not JSON"],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(broken, at="4" * 40))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"], result["errors"]) == (
        "failed",
        "main",
        ["plugin.json: not JSON"],
    )


def test_untagged_updated_when_the_manifest_version_changed(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    untagged(monkeypatch, "4" * 40)
    bumped = {
        "sha": "4" * 40,
        "manifest": {"version": "1.14.0"},
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(bumped, at="4" * 40))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("updated", "main")
    record = json.loads((root / ".store" / "oddyssey.json").read_text())
    assert (record["ref"], record["sha"], record["version"]) == ("main", "4" * 40, "1.14.0")


def test_a_tag_without_the_manifest_is_followed_on_the_branch(tmp_path: Path, monkeypatch):
    # the repository's tags predate the plugin: the record stays on main, by version
    root = store_with(tmp_path)
    branch_record(root)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.gitrepo, "default_branch", lambda repository: ("main", "3" * 40))
    asked = []
    monkeypatch.setattr(
        releases.gitrepo, "has_file", lambda repository, sha, path: asked.append((sha, path))
    )
    monkeypatch.setattr(releases.validate, "validate", lambda *a: pytest.fail("validated"))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("unchanged", "main")
    assert asked == [("2" * 40, "marketplace/oddyssey/plugin.json")]


def test_a_plugin_that_vanished_from_a_tagged_record_is_a_failure(tmp_path: Path, monkeypatch):
    # the record is on v1.13.0; the latest tag and the head both lack plugin.json
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(releases.gitrepo, "has_file", lambda repository, sha, path: False)
    monkeypatch.setattr(releases.gitrepo, "default_branch", lambda repository: ("main", "4" * 40))
    gone = {
        "sha": "4" * 40,
        "manifest": {},
        "skills": False,
        "mcp": {},
        "errors": ["plugin.json: missing"],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(gone, at="4" * 40))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("failed", "main")
    assert result["errors"][0].startswith("plugin.json: at neither")
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"


def test_a_first_tag_takes_over_a_record_on_a_branch(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    branch_record(root)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: {"v1.13.0": "5" * 40})
    same = {
        "sha": "5" * 40,
        "manifest": {"version": "1.13.0"},
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(same, at="5" * 40))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("updated", "v1.13.0")
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["sha"] == "5" * 40


def test_unreadable_tags_are_a_failure_not_a_crash(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)

    def failing(repository):
        raise releases.gitrepo.RepositoryError("gone")

    monkeypatch.setattr(releases.gitrepo, "list_tags", failing)
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert result["status"] == "failed"
    assert "gone" in result["errors"][0]


PASSING = {
    "sha": "2" * 40,
    "manifest": {"version": "1.14.0"},
    "skills": False,
    "mcp": {},
    "errors": [],
    "notes": [],
}


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
    assert (result["status"], result["ref"]) == ("failed", "v1.14.0")
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


def test_a_new_manifest_the_store_refuses_is_named_as_the_manifests(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    bad = {"name": "oddyssey", "version": "1.14.0", "description": "red \x1b"}
    passing = {
        "sha": "2" * 40,
        "manifest": bad,
        "skills": False,
        "mcp": {},
        "errors": [],
        "notes": [],
    }
    monkeypatch.setattr(releases.validate, "validate", fake_validate(passing))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert result["status"] == "failed"
    assert result["errors"] == ["plugin.json: description: control character"]
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"


def test_a_record_the_store_refuses_is_a_failed_follow(tmp_path: Path, monkeypatch):
    root = store_with(tmp_path)
    monkeypatch.setattr(releases.gitrepo, "list_tags", lambda repository: TAGS)
    tainted = {**PASSING, "manifest": {"version": "1.14.0\nFOO=bar"}}
    monkeypatch.setattr(releases.validate, "validate", fake_validate(tainted))
    result = releases.follow(root, tmp_path / "work")["oddyssey"]
    assert (result["status"], result["ref"]) == ("failed", "v1.14.0")
    assert any("control character" in e for e in result["errors"])
    assert json.loads((root / ".store" / "oddyssey.json").read_text())["ref"] == "v1.13.0"
