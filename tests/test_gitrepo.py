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


def test_an_unreadable_repository_is_a_named_error(tmp_path: Path):
    with pytest.raises(gitrepo.RepositoryError):
        gitrepo.clone_at("contoso/does-not-exist", "1" * 40, tmp_path / "x")
