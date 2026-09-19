import json
from pathlib import Path

from scripts import intake

FIXTURES = Path(__file__).parent / "fixtures" / "issues"
TAGS = {"v1.0.0": "a" * 40, "v1.2.0": "b" * 40}


def test_parse_form_maps_labels_to_values():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    assert fields["Plugin name"] == "my-otel-plugin"
    assert fields["Path inside the repository"] == ""
    assert fields["Keywords"] == "opentelemetry, tempo, traces"


def test_candidate_from_a_valid_form():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    record, errors = intake.candidate(fields, issue_number=7)
    assert errors == []
    assert record["name"] == "my-otel-plugin"
    assert record["repository"] == "contoso/my-otel-plugin"
    assert record["path"] == ""
    assert record["keywords"] == ["opentelemetry", "tempo", "traces"]
    assert record["author"] == {"name": "Contoso", "url": "https://github.com/contoso"}
    assert record["homepage"] == ""
    assert record["submitted_in"] == 7
    assert list(record) == [
        "name",
        "description",
        "category",
        "repository",
        "path",
        "author",
        "license",
        "homepage",
        "keywords",
        "submitted_in",
    ]


def test_candidate_names_a_bad_repository():
    fields = intake.parse_form((FIXTURES / "bad-repository.md").read_text())
    _, errors = intake.candidate(fields, issue_number=7)
    assert errors == ["GitHub repository: owner/repo"]


def test_resolve_ref_picks_the_latest_release(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    assert intake.resolve_ref("contoso/my-otel-plugin") == ("v1.2.0", "b" * 40, [])


def test_resolve_ref_no_release_tag(monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: {"nightly": "c" * 40})
    tag, sha, errors = intake.resolve_ref("contoso/my-otel-plugin")
    assert (tag, sha) == ("", "")
    assert errors == [
        "GitHub repository: no release tag (the pipeline follows X.Y.Z or vX.Y.Z tags)"
    ]


def test_resolve_ref_unreadable(monkeypatch):
    def failing(repository):
        raise intake.gitrepo.RepositoryError("repository not found")

    monkeypatch.setattr(intake.gitrepo, "list_tags", failing)
    tag, sha, errors = intake.resolve_ref("contoso/gone")
    assert (tag, sha) == ("", "")
    assert errors == ["GitHub repository: cannot be read (repository not found)"]


def test_candidate_refuses_a_comment_terminator():
    fields = intake.parse_form((FIXTURES / "comment-close.md").read_text())
    _, errors = intake.candidate(fields, issue_number=7)
    assert errors == ["Description: must not contain -->"]


def test_main_resolves_the_latest_release(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: TAGS)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["errors"] == []
    assert data["candidate"]["name"] == "my-otel-plugin"
    assert data["candidate"]["ref"] == "v1.2.0"
    assert data["candidate"]["sha"] == "b" * 40


def test_main_reports_the_resolution_errors(tmp_path: Path, capsys, monkeypatch):
    monkeypatch.setattr(intake.gitrepo, "list_tags", lambda repository: {})
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["errors"] == [
        "GitHub repository: no release tag (the pipeline follows X.Y.Z or vX.Y.Z tags)"
    ]
    assert "ref" not in data["candidate"]


def test_main_does_not_resolve_a_form_with_errors(tmp_path: Path, capsys, monkeypatch):
    def must_not_be_called(repository):
        raise AssertionError("must not be called")

    monkeypatch.setattr(intake.gitrepo, "list_tags", must_not_be_called)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "bad-repository.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["errors"] == ["GitHub repository: owner/repo"]


def test_main_no_resolve_keeps_the_form_only(tmp_path: Path, capsys, monkeypatch):
    def must_not_be_called(repository):
        raise AssertionError("must not be called")

    monkeypatch.setattr(intake.gitrepo, "list_tags", must_not_be_called)
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    args = ["--body-file", str(body), "--issue", "7", "--json", "--no-resolve"]
    assert intake.main(args) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["errors"] == []
    assert "ref" not in data["candidate"] and "sha" not in data["candidate"]


def test_path_is_refused_by_segment_not_by_substring():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    record, errors = intake.candidate({**fields, "Path inside the repository": "a..b"}, 7)
    assert errors == [] and record["path"] == "a..b"
    _, errors = intake.candidate({**fields, "Path inside the repository": "a/../b"}, 7)
    assert errors == ["Path inside the repository: a relative directory"]
