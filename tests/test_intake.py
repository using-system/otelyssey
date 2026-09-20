import json
from pathlib import Path

import pytest

from scripts import intake

FIXTURES = Path(__file__).parent / "fixtures" / "issues"
TAGS = {"v1.0.0": "a" * 40, "v1.2.0": "b" * 40}


@pytest.fixture(autouse=True)
def the_tag_carries_the_manifest(monkeypatch):
    """No network: a tag carries plugin.json unless a test says otherwise."""
    monkeypatch.setattr(intake.gitrepo, "has_file", lambda repository, sha, path: True)


def test_parse_form_maps_labels_to_values():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    assert fields == {
        "plugin.json URL": "https://github.com/contoso/my-otel-plugin/blob/main/plugin.json"
    }
    assert intake.parse_form("### plugin.json URL\n\n_No response_\n") == {"plugin.json URL": ""}


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://github.com/contoso/my-otel-plugin/blob/main/plugin.json",
            ("contoso/my-otel-plugin", ""),
        ),
        (
            "https://github.com/Contoso/skills/blob/v1.2.0/plugins/otel/plugin.json",
            ("Contoso/skills", "plugins/otel"),
        ),
        (
            "https://github.com/contoso/skills/raw/main/plugins/otel/plugin.json",
            ("contoso/skills", "plugins/otel"),
        ),
        (
            "https://raw.githubusercontent.com/contoso/skills/main/plugins/otel/plugin.json",
            ("contoso/skills", "plugins/otel"),
        ),
        ("https://www.github.com/contoso/skills.git/blob/main/plugin.json", ("contoso/skills", "")),
        # a percent-encoded path is decoded; the store accepts a space, the pages quote it
        (
            "https://github.com/contoso/skills/blob/main/my%20plugins/otel/plugin.json",
            ("contoso/skills", "my plugins/otel"),
        ),
        (
            "  https://github.com/contoso/my-otel-plugin/blob/main/plugin.json  ",
            ("contoso/my-otel-plugin", ""),
        ),
    ],
)
def test_parse_url_gives_the_repository_and_the_path(url, expected):
    assert intake.parse_url(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/contoso",
        "https://github.com/contoso/my-otel-plugin",
        "https://github.com/contoso/my-otel-plugin/tree/main/plugins/otel",
        "https://github.com/contoso/my-otel-plugin/blob/main/plugins/otel",
        "https://github.com/contoso/my-otel-plugin/blob/plugin.json",
        "http://github.com/contoso/my-otel-plugin/blob/main/plugin.json",
        "https://gitlab.com/contoso/my-otel-plugin/-/blob/main/plugin.json",
        "https://github.com/contoso/my-otel-plugin/blob/main/../plugin.json",
        "https://github.com/contoso/my-otel-plugin/blob/main/./plugin.json",
        "https://github.com/contoso/my-otel-plugin/blob/main/plugin.json?plain=1",
        "https://github.com/contoso/my-otel-plugin/blob/main/PLUGIN.JSON",
        "https://github.com/-contoso/my-otel-plugin/blob/main/plugin.json",
        "https://github.com/contoso/my-otel-plugin/blob/main/a%0ab/plugin.json",
        "",
    ],
)
def test_parse_url_refuses_what_is_not_a_manifest_url(url):
    with pytest.raises(ValueError, match="plugin.json URL"):
        intake.parse_url(url)


def test_candidate_from_a_valid_form():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    record, errors = intake.candidate(fields, issue_number=7)
    assert errors == []
    assert record == {"repository": "contoso/my-otel-plugin", "path": "", "submitted_in": 7}


def test_candidate_names_a_bad_url():
    fields = intake.parse_form((FIXTURES / "bad-repository.md").read_text())
    _, errors = intake.candidate(fields, issue_number=7)
    assert len(errors) == 1 and errors[0].startswith("plugin.json URL: the URL of plugin.json")


def test_candidate_names_a_missing_section():
    _, errors = intake.candidate({"Plugin name": "x"}, issue_number=7)
    assert errors == ["plugin.json URL: section missing from the form"]


def test_resolve_ref_picks_the_latest_release(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    assert intake.resolve_ref("contoso/my-otel-plugin", "") == ("v1.2.0", "b" * 40, [])


def test_resolve_ref_without_a_release_tag_takes_the_default_branch(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: {"nightly": "c" * 40})
    monkeypatch.setattr(intake.gitrepo, "default_branch", lambda repository: ("main", "d" * 40))
    assert intake.resolve_ref("contoso/my-otel-plugin", "") == ("main", "d" * 40, [])


def test_resolve_ref_prefers_a_release_tag_over_the_default_branch(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(intake.gitrepo, "default_branch", lambda *a: pytest.fail("asked"))
    assert intake.resolve_ref("contoso/my-otel-plugin", "") == ("v1.2.0", "b" * 40, [])


def test_resolve_ref_skips_a_tag_without_the_manifest(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    monkeypatch.setattr(intake.gitrepo, "default_branch", lambda repository: ("main", "d" * 40))
    asked = []
    monkeypatch.setattr(
        intake.gitrepo, "has_file", lambda repository, sha, path: asked.append((sha, path))
    )
    assert intake.resolve_ref("contoso/my-otel-plugin", "plugins/x") == ("main", "d" * 40, [])
    assert asked == [("b" * 40, "plugins/x/plugin.json")]


def test_resolve_ref_unreadable(monkeypatch):
    def failing(repository):
        raise intake.gitrepo.RepositoryError("repository not found")

    monkeypatch.setattr(intake.gitrepo, "list_tags", failing)
    tag, sha, errors = intake.resolve_ref("contoso/gone", "")
    assert (tag, sha) == ("", "")
    assert errors == ["GitHub repository: cannot be read (repository not found)"]


def test_main_resolves_the_latest_release_and_ignores_the_urls_ref(
    tmp_path: Path, capsys, monkeypatch
):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text().replace("/main/", "/some-branch/"))
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["errors"] == []
    assert data["candidate"] == {
        "repository": "contoso/my-otel-plugin",
        "path": "",
        "submitted_in": 7,
        "ref": "v1.2.0",
        "sha": "b" * 40,
    }


def test_main_reports_the_resolution_errors(tmp_path: Path, capsys, monkeypatch):
    def gone(repository):
        raise intake.gitrepo.RepositoryError("repository not found")

    monkeypatch.setattr(intake.gitrepo, "list_tags", gone)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["errors"] == ["GitHub repository: cannot be read (repository not found)"]
    assert "ref" not in data["candidate"]


def test_main_does_not_resolve_a_form_with_errors(tmp_path: Path, capsys, monkeypatch):
    def must_not_be_called(repository):
        raise AssertionError("must not be called")

    monkeypatch.setattr(intake.gitrepo, "list_tags", must_not_be_called)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "bad-repository.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 1
    [error] = json.loads(capsys.readouterr().out)["errors"]
    assert error.startswith("plugin.json URL")


def test_main_no_resolve_keeps_the_form_only(tmp_path: Path, capsys, monkeypatch):
    def must_not_be_called(repository):
        raise AssertionError("must not be called")

    monkeypatch.setattr(intake.gitrepo, "list_tags", must_not_be_called)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--no-resolve"]) == 0
    assert capsys.readouterr().out == "candidate at contoso/my-otel-plugin '' \n"
