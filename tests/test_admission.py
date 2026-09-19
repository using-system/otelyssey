import json
from pathlib import Path

import pytest

from scripts import admission, report, store
from tests.test_report import CANDIDATE, SMOKE, VALIDATION


def intake_comment() -> str:
    body, verdict = report.render(CANDIDATE, [], VALIDATION, SMOKE)
    assert verdict == "format-ok"
    return body


def test_the_candidate_is_read_back_from_the_intake_comment():
    candidate = admission.candidate_from_comment(intake_comment())
    assert candidate["name"] == "my-otel-plugin"
    assert candidate["sha"] == "1" * 40
    assert candidate["submitted_in"] == 7


def test_a_comment_without_the_block_is_refused():
    with pytest.raises(ValueError, match="candidate block"):
        admission.candidate_from_comment("## Intake\n\n**Form**: needs changes\n")


def test_the_last_block_wins_when_the_comment_carries_two():
    first = intake_comment()
    second = first.replace('"version": "1.2.0"', '"version": "1.3.0"')
    assert admission.candidate_from_comment(first + second)["version"] == "1.3.0"


def test_the_record_adds_the_admission_date_and_zero_stats():
    candidate = admission.candidate_from_comment(intake_comment())
    record = admission.admitted(candidate, 7, "2026-09-19", "2026-09-19T17:00:00Z")
    assert list(record) == list(store.FIELDS)
    assert record["admitted_at"] == "2026-09-19"
    assert record["stats"] == {
        "stars": 0,
        "forks": 0,
        "watchers": 0,
        "refreshed_at": "2026-09-19T17:00:00Z",
    }
    assert store.validate_record(record) == []


def test_a_block_from_another_issue_is_refused():
    candidate = admission.candidate_from_comment(intake_comment())
    with pytest.raises(ValueError, match="submitted_in"):
        admission.admitted(candidate, 8, "2026-09-19", "2026-09-19T17:00:00Z")


def test_main_writes_the_canonical_record_and_prints_its_path(tmp_path: Path, capsys):
    (tmp_path / "comment.md").write_text(intake_comment(), encoding="utf-8")
    code = admission.main(
        ["--comment-file", str(tmp_path / "comment.md"), "--issue", "7", "--root", str(tmp_path)]
    )
    assert code == 0
    path = tmp_path / ".store" / "my-otel-plugin.json"
    assert capsys.readouterr().out.strip() == str(path)
    record = json.loads(path.read_text(encoding="utf-8"))
    assert path.read_text(encoding="utf-8") == store.canonical(record)
    assert store.DATE_RE.match(record["admitted_at"])
    assert store.STAMP_RE.match(record["stats"]["refreshed_at"])


def test_main_fails_the_check_on_a_wrong_issue(tmp_path: Path, capsys):
    (tmp_path / "comment.md").write_text(intake_comment(), encoding="utf-8")
    code = admission.main(
        ["--comment-file", str(tmp_path / "comment.md"), "--issue", "8", "--root", str(tmp_path)]
    )
    assert code == 1
    assert "submitted_in" in capsys.readouterr().out
    assert not (tmp_path / ".store").exists()


def test_a_value_that_would_close_the_block_is_read_back_intact():
    candidate = {**CANDIDATE, "description": "closes --> the block"}
    body, _ = report.render(candidate, [], VALIDATION, SMOKE)
    assert admission.candidate_from_comment(body)["description"] == "closes --> the block"


def test_a_block_that_is_not_a_json_object_is_refused():
    with pytest.raises(ValueError, match="not JSON"):
        admission.candidate_from_comment(f"{report.CANDIDATE_MARK}{{oops -->")
    with pytest.raises(ValueError, match="not an object"):
        admission.candidate_from_comment(f"{report.CANDIDATE_MARK}[1] -->")


def test_main_fails_the_check_on_a_candidate_the_store_refuses(tmp_path: Path, capsys):
    body = intake_comment().replace('"category": "backend"', '"category": "other"')
    (tmp_path / "comment.md").write_text(body, encoding="utf-8")
    code = admission.main(
        ["--comment-file", str(tmp_path / "comment.md"), "--issue", "7", "--root", str(tmp_path)]
    )
    assert code == 1
    assert "category" in capsys.readouterr().out
    assert not (tmp_path / ".store").exists()


def test_main_exits_2_when_the_comment_file_is_missing(tmp_path: Path, capsys):
    code = admission.main(["--comment-file", str(tmp_path / "none.md"), "--issue", "7"])
    assert code == 2
    assert capsys.readouterr().out == ""
