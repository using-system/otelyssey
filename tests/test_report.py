import json
from pathlib import Path

from scripts import report, store

CANDIDATE = {
    "repository": "contoso/my-otel-plugin",
    "path": "",
    "submitted_in": 7,
    "ref": "v1.2.0",
    "sha": "1" * 40,
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
RECORD = {
    "name": "my-otel-plugin",
    "description": "d",
    "repository": "contoso/my-otel-plugin",
    "path": "",
    "ref": "v1.2.0",
    "sha": "1" * 40,
    "version": "1.2.0",
    "author": {"name": "Contoso"},
    "license": "Apache-2.0",
    "homepage": "https://contoso.example/plugin",
    "keywords": ["opentelemetry"],
    "submitted_in": 7,
}
DERIVED = {"record": RECORD, "errors": [], "from_repository": []}
SMOKE = {
    "copilot": {"status": "pass", "output": "ok"},
    "claude": {"status": "pass", "output": "ok"},
}


def test_green_report_carries_the_derived_record_in_store_order():
    body, verdict = report.render(CANDIDATE, [], VALIDATION, DERIVED, SMOKE)
    assert verdict == "format-ok"
    block = body.split(report.CANDIDATE_MARK, 1)[1].split(" -->", 1)[0]
    candidate = json.loads(block)
    assert list(candidate) == [
        f for f in store.FIELDS if f not in ("categories", "admitted_at", "stats")
    ]
    assert candidate == RECORD
    assert "**Plugin at `v1.2.0`**: pass (commit `" + "1" * 40 + "`)" in body
    assert "**Record**: every field from plugin.json" in body
    assert "Notes (informational)" in body and "commands:" in body


def test_green_report_states_the_facts_the_review_reads_in_backticks():
    # the review reads through a sanitizer that drops HTML comments and escapes quotes:
    # the facts it rules on stand in the text, in backticks, the full sha included
    body, _ = report.render(CANDIDATE, [], VALIDATION, DERIVED, SMOKE)
    assert "**Plugin**: `my-otel-plugin` `1.2.0` in `contoso/my-otel-plugin` at its root" in body
    candidate = {**CANDIDATE, "path": "plugins/my-otel-plugin"}
    body, _ = report.render(candidate, [], VALIDATION, DERIVED, SMOKE)
    assert "in `contoso/my-otel-plugin` at `plugins/my-otel-plugin`" in body


def test_the_report_says_which_fields_the_repository_filled():
    derived = {**DERIVED, "from_repository": ["description", "keywords"]}
    body, verdict = report.render(CANDIDATE, [], VALIDATION, derived, SMOKE)
    assert verdict == "format-ok"
    assert (
        "**Record**: description, keywords from the repository (plugin.json has none), "
        "the rest from plugin.json"
    ) in body


def test_derivation_errors_make_needs_changes_before_any_install():
    derived = {
        **DERIVED,
        "errors": ["plugin.json: no license, and the repository has none either: add a license"],
    }
    body, verdict = report.render(CANDIDATE, [], VALIDATION, derived, None)
    assert verdict == "needs-changes"
    assert "**Record**: needs changes\n- plugin.json: no license" in body
    assert "**Install" not in body
    assert report.CANDIDATE_MARK not in body


def test_a_missing_derivation_is_an_infra_error():
    body, verdict = report.render(CANDIDATE, [], VALIDATION, None, None)
    assert verdict == "infra-error"
    assert "**Record**: not derived" in body


def test_form_errors_make_needs_changes():
    body, verdict = report.render({}, ["plugin.json URL: the URL of plugin.json"], None, None, None)
    assert verdict == "needs-changes"
    assert "plugin.json URL" in body
    assert report.CANDIDATE_MARK not in body


def test_validation_errors_make_needs_changes():
    validation = {**VALIDATION, "sha": None, "errors": ["repository: not found"], "notes": []}
    body, verdict = report.render(CANDIDATE, [], validation, None, None)
    assert verdict == "needs-changes"
    assert "**Plugin at `v1.2.0`**: needs changes (commit `unresolved`)" in body


def test_unavailable_host_is_an_infra_error():
    smoke = {**SMOKE, "claude": {"status": "unavailable", "output": "no claude"}}
    _, verdict = report.render(CANDIDATE, [], VALIDATION, DERIVED, smoke)
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
    derived = {**DERIVED, "record": {**RECORD, "author": {"name": "x --> injected"}}}
    body, verdict = report.render(CANDIDATE, [], VALIDATION, derived, SMOKE)
    assert verdict == "format-ok"
    tail = body.split(report.CANDIDATE_MARK, 1)[1]
    assert tail.count("-->") == 1
    block = tail.split(" -->", 1)[0]
    assert json.loads(block)["author"]["name"] == "x --> injected"


def test_the_install_lines_start_a_paragraph_after_the_notes_list():
    body, _ = report.render(CANDIDATE, [], VALIDATION, DERIVED, SMOKE)
    # a line right after a bullet is that bullet's continuation in Markdown
    assert "format defines\n\n**Record**" in body
