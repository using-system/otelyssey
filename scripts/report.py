"""The one comment the intake workflow leaves on a submission, and its verdict."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MARK = "<!-- otelyssey-intake -->"
CANDIDATE_MARK = "<!-- otelyssey-candidate "


def _read_json(path: str | None) -> dict | None:
    """The file's JSON, or None when it is absent, empty or not JSON (the step did not run)."""
    if not path or not Path(path).is_file():
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except ValueError:
        return None


def candidate_block(record: dict) -> str:
    """The record as JSON whose `>` is escaped: no manifest value can close the HTML comment."""
    return json.dumps(record, ensure_ascii=False).replace(">", "\\u003e")


def render(
    candidate: dict,
    errors: list[str],
    validation: dict | None,
    derived: dict | None,
    smoke: dict | None,
) -> tuple[str, str]:
    """The comment and its verdict: format-ok, needs-changes or infra-error.

    The derivation (derive.py) gives the record, its errors and the fields the repository's
    metadata filled; it runs after a validation that passed.
    """
    lines = [MARK, "## Intake", ""]
    if errors:
        lines.append("**Form**: needs changes")
        lines += [f"- {e}" for e in errors]
        lines += ["", "Edit the issue; the checks run again on every edit."]
        return "\n".join(lines) + "\n", "needs-changes"
    lines.append("**Form**: pass")
    ref = candidate.get("ref", "")
    # the review reads through a sanitizer that drops HTML comments and escapes quotes: the
    # facts it rules on stand here in backticks, the full sha below, never in the block only
    where = f"at `{candidate['path']}`" if candidate.get("path") else "at its root"
    if validation and not validation["errors"]:
        manifest = validation["manifest"]
        lines.append(
            f"**Plugin**: `{manifest['name']}` `{manifest['version']}` "
            f"in `{candidate['repository']}` {where}"
        )
    verdict = "format-ok"
    if validation is None:
        lines.append("**Plugin at the ref**: not run")
        verdict = "infra-error"
    elif validation["errors"]:
        sha = (validation.get("sha") or "")[:12] or "unresolved"
        lines.append(f"**Plugin at `{ref}`**: needs changes (commit `{sha}`)")
        lines += [f"- {e}" for e in validation["errors"]]
        verdict = "needs-changes"
    else:
        lines.append(f"**Plugin at `{ref}`**: pass (commit `{validation['sha']}`)")
    if validation and validation.get("notes"):
        lines += ["", "Notes (informational):"] + [f"- {n}" for n in validation["notes"]]
    if verdict == "format-ok":
        if lines[-1].startswith("- "):
            lines.append("")  # closes the notes list: the next line is a paragraph, not a bullet
        if derived is None:
            lines.append("**Record**: not derived")
            verdict = "infra-error"
        elif derived["errors"]:
            lines.append("**Record**: needs changes")
            lines += [f"- {e}" for e in derived["errors"]]
            verdict = "needs-changes"
        else:
            filled = derived.get("from_repository") or []
            source = "every field from plugin.json"
            if filled:
                source = (
                    f"{', '.join(filled)} from the repository (plugin.json has none), "
                    "the rest from plugin.json"
                )
            lines.append(f"**Record**: {source}")
    if verdict == "format-ok":
        if smoke is None:
            lines.append("**Install**: not run")
            verdict = "infra-error"
        else:
            for host, r in smoke.items():
                lines.append(f"**Install on {host}**: {r['status']}")
                if r["status"] != "pass":
                    lines += ["", "```text", r["output"].strip(), "```", ""]
            statuses = {r["status"] for r in smoke.values()}
            if "fail" in statuses:
                verdict = "needs-changes"
            elif "unavailable" in statuses:
                verdict = "infra-error"
    if verdict == "needs-changes":
        lines += [
            "",
            "Fix the plugin (a new tag, or a new commit on the default branch) and edit the "
            "issue; the checks run again.",
        ]
    elif verdict == "infra-error":
        lines += ["", "The pipeline could not complete on its side; a maintainer re-runs it."]
    else:
        record = derived["record"]
        lines += [
            "",
            "The format holds; the review of relevance, and that it is not a listed plugin "
            "resubmitted, follows on this issue.",
            "",
            f"{CANDIDATE_MARK}{candidate_block(record)} -->",
        ]
    return "\n".join(lines) + "\n", verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="render the intake comment and print its verdict")
    parser.add_argument("--candidate", required=True, help="intake.py --json output")
    parser.add_argument("--validation", default=None, help="validate.py --json output")
    parser.add_argument("--derived", default=None, help="derive.py --out file")
    parser.add_argument("--smoke", default=None, help="smoke.py --json output")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    intake = _read_json(args.candidate)
    if intake is None:
        print("infra-error")
        Path(args.out).write_text(
            f"{MARK}\n## Intake\n\nThe form could not be parsed.\n", encoding="utf-8"
        )
        return 0
    validation = _read_json(args.validation)
    derived = _read_json(args.derived)
    smoke = _read_json(args.smoke)
    body, verdict = render(intake["candidate"], intake["errors"], validation, derived, smoke)
    Path(args.out).write_text(body, encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
