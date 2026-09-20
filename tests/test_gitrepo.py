from pathlib import Path

import pytest

from scripts import gitrepo

FIXTURE = (Path(__file__).parent / "fixtures" / "ls" / "tags.txt").read_text()


def test_parse_tags_prefers_the_peeled_commit():
    tags = gitrepo.parse_tags(FIXTURE)
    assert tags["v1.0.0"] == "b" * 40
    assert tags["v1.2.0"] == "d" * 40
    assert tags["nightly"] == "e" * 40


def test_semver_key_reads_release_tags_only():
    assert gitrepo.semver_key("v1.10.0") == (1, 10, 0)
    assert gitrepo.semver_key("1.2.3") == (1, 2, 3)
    assert gitrepo.semver_key("nightly") is None
    assert gitrepo.semver_key("v1.2.0-rc1") is None


def test_latest_release_sorts_numerically():
    assert gitrepo.latest_release(gitrepo.parse_tags(FIXTURE)) == ("v1.10.0", "c" * 40)


def test_latest_release_none_without_release_tags():
    assert gitrepo.latest_release({"nightly": "e" * 40}) is None


def test_parse_head_reads_the_default_branch_and_its_commit():
    output = "ref: refs/heads/main\tHEAD\n" + "a" * 40 + "\tHEAD\n"
    assert gitrepo.parse_head(output) == ("main", "a" * 40)


def test_parse_head_without_a_symref_is_an_error():
    with pytest.raises(gitrepo.RepositoryError):
        gitrepo.parse_head("a" * 40 + "\tHEAD\n")


def test_resolve_takes_a_full_sha_as_itself(monkeypatch):
    monkeypatch.setattr(gitrepo, "list_tags", lambda *a: pytest.fail("looked up"))
    assert gitrepo.resolve("contoso/plugin", "b" * 40) == "b" * 40


def test_resolve_a_tag_by_name(monkeypatch):
    monkeypatch.setattr(gitrepo, "list_tags", lambda repository: {"v1.0.0": "c" * 40})
    assert gitrepo.resolve("contoso/plugin", "v1.0.0") == "c" * 40


def test_resolve_a_branch_by_name(monkeypatch):
    monkeypatch.setattr(gitrepo, "list_tags", lambda repository: {})
    heads = "e" * 40 + "\trefs/heads/feature/main\n" + "d" * 40 + "\trefs/heads/main\n"
    monkeypatch.setattr(gitrepo, "_git", lambda args, **kw: heads)
    assert gitrepo.resolve("contoso/plugin", "main") == "d" * 40
    with pytest.raises(LookupError):
        gitrepo.resolve("contoso/plugin", "develop")


def test_an_unreadable_repository_is_a_named_error(tmp_path: Path):
    with pytest.raises(gitrepo.RepositoryError):
        gitrepo.clone_at("contoso/does-not-exist", "1" * 40, tmp_path / "x")
