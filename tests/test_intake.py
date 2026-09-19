from pathlib import Path

from scripts import intake

FIXTURES = Path(__file__).parent / "fixtures" / "issues"


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
    assert record["ref"] == "v1.2.0"
    assert record["keywords"] == ["opentelemetry", "tempo", "traces"]
    assert record["author"] == {"name": "Contoso", "url": "https://github.com/contoso"}
    assert record["homepage"] == ""
    assert record["submitted_in"] == 7
    assert record["submitted_version"] == "1.2.0"
    assert "sha" not in record


def test_candidate_names_every_problem():
    fields = intake.parse_form((FIXTURES / "missing-tag.md").read_text())
    _, errors = intake.candidate(fields, issue_number=7)
    assert any("Release tag" in e for e in errors)
    assert any("GitHub repository" in e for e in errors)


def test_candidate_refuses_a_comment_terminator():
    fields = intake.parse_form((FIXTURES / "comment-close.md").read_text())
    _, errors = intake.candidate(fields, issue_number=7)
    assert errors == ["Description: must not contain -->"]


def test_main_prints_json(tmp_path: Path, capsys):
    body = tmp_path / "body.md"
    body.write_text((FIXTURES / "valid.md").read_text())
    assert intake.main(["--body-file", str(body), "--issue", "7", "--json"]) == 0
    assert '"name": "my-otel-plugin"' in capsys.readouterr().out


def test_path_is_refused_by_segment_not_by_substring():
    fields = intake.parse_form((FIXTURES / "valid.md").read_text())
    record, errors = intake.candidate({**fields, "Path inside the repository": "a..b"}, 7)
    assert errors == [] and record["path"] == "a..b"
    _, errors = intake.candidate({**fields, "Path inside the repository": "a/../b"}, 7)
    assert errors == ["Path inside the repository: a relative directory"]
