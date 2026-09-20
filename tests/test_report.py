import json
from pathlib import Path

from scripts import report, store

CANDIDATE = {
    "name": "my-otel-plugin",
    "description": "d",
    "category": "backend",
    "repository": "contoso/my-otel-plugin",
    "path": "",
    "ref": "v1.2.0",
    "sha": "1" * 40,
    "author": {"name": "Contoso"},
    "license": "Apache-2.0",
    "homepage": "",
    "keywords": ["opentelemetry"],
    "submitted_in": 7,
}
VALIDATION = {
    "sha": "1" * 40,
    "manifest": {
        "name": "my-otel-plugin",
        "version": "1.2.0",
        "homepage": "https://contoso.example/plugin",
    },
    "errors": [],
    "notes": ["commands: not an entry the Agent Plugins format defines"],
}
SMOKE = {
    "copilot": {"status": "pass", "output": "ok"},
    "claude": {"status": "pass", "output": "ok"},
}


def test_green_report_carries_the_candidate_block_in_store_order():
    body, verdict = report.render(CANDIDATE, [], VALIDATION, SMOKE)
    assert verdict == "format-ok"
    block = body.split(report.CANDIDATE_MARK, 1)[1].split(" -->", 1)[0]
    candidate = json.loads(block)
    assert list(candidate) == [f for f in store.FIELDS if f not in ("admitted_at", "stats")]
    assert candidate["sha"] == "1" * 40
    assert candidate["version"] == "1.2.0"
    assert candidate["homepage"] == "https://contoso.example/plugin"
    assert "**Plugin at `v1.2.0`**: pass (commit `" + "1" * 40 + "`)" in body
    assert "Notes (informational)" in body and "commands:" in body


def test_green_report_states_the_facts_the_review_reads_in_backticks():
    # the review reads through a sanitizer that drops HTML comments and escapes quotes:
    # the facts it rules on stand in the text, in backticks, the full sha included
    body, _ = report.render(CANDIDATE, [], VALIDATION, SMOKE)
    assert "**Plugin**: `my-otel-plugin` `1.2.0` in `contoso/my-otel-plugin` at its root" in body
    candidate = {**CANDIDATE, "path": "plugins/my-otel-plugin"}
    body, _ = report.render(candidate, [], VALIDATION, SMOKE)
    assert "in `contoso/my-otel-plugin` at `plugins/my-otel-plugin`" in body


def test_the_record_takes_the_version_of_the_manifest_and_the_sha_of_the_validation():
    candidate = {k: v for k, v in CANDIDATE.items() if k != "sha"}
    record = report.candidate_record(candidate, VALIDATION)
    assert record["sha"] == "1" * 40
    assert record["version"] == "1.2.0"


def test_form_errors_make_needs_changes():
    body, verdict = report.render({}, ["GitHub repository: owner/repo"], None, None)
    assert verdict == "needs-changes"
    assert "GitHub repository" in body
    assert report.CANDIDATE_MARK not in body


def test_validation_errors_make_needs_changes():
    validation = {**VALIDATION, "sha": None, "errors": ["repository: not found"], "notes": []}
    body, verdict = report.render(CANDIDATE, [], validation, None)
    assert verdict == "needs-changes"
    assert "**Plugin at `v1.2.0`**: needs changes (commit `unresolved`)" in body


def test_unavailable_host_is_an_infra_error():
    smoke = {**SMOKE, "claude": {"status": "unavailable", "output": "no claude"}}
    _, verdict = report.render(CANDIDATE, [], VALIDATION, smoke)
    assert verdict == "infra-error"


def test_main_treats_an_empty_file_as_not_run(tmp_path: Path, capsys):
    (tmp_path / "candidate.json").write_text(json.dumps({"candidate": CANDIDATE, "errors": []}))
    (tmp_path / "validation.json").write_text("")
    code = report.main(
        [
            "--candidate",
            str(tmp_path / "candidate.json"),
            "--validation",
            str(tmp_path / "validation.json"),
            "--out",
            str(tmp_path / "comment.md"),
        ]
    )
    assert code == 0
    assert capsys.readouterr().out.strip() == "infra-error"
    assert "not run" in (tmp_path / "comment.md").read_text()


def test_manifest_content_cannot_close_the_candidate_block():
    manifest = {**VALIDATION["manifest"], "author": {"name": "x --> injected"}}
    body, verdict = report.render(CANDIDATE, [], {**VALIDATION, "manifest": manifest}, SMOKE)
    assert verdict == "format-ok"
    tail = body.split(report.CANDIDATE_MARK, 1)[1]
    assert tail.count("-->") == 1
    block = tail.split(" -->", 1)[0]
    assert json.loads(block)["author"]["name"] == "x --> injected"


def test_a_manifest_url_is_copied_only_when_it_is_https():
    manifest = {
        **VALIDATION["manifest"],
        "homepage": "javascript:alert(1)",
        "author": {"name": "x", "url": "http://insecure"},
    }
    record = report.candidate_record(CANDIDATE, {**VALIDATION, "manifest": manifest})
    assert record["homepage"] == ""
    assert record["author"] == {"name": "x"}


def test_the_install_lines_start_a_paragraph_after_the_notes_list():
    body, _ = report.render(CANDIDATE, [], VALIDATION, SMOKE)
    # a line right after a bullet is that bullet's continuation in Markdown
    assert "format defines\n\n**Install on copilot**" in body
