"""The one comment the intake workflow leaves on a submission, and its verdict."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from scripts import store

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


def candidate_record(candidate: dict, validation: dict) -> dict:
    """The candidate completed from the manifest, in the store's field order."""
    manifest = validation["manifest"]
    merged = {k: v for k, v in candidate.items() if k != "submitted_version"}
    merged["sha"] = validation["sha"]
    merged["version"] = manifest.get("version") or candidate.get("submitted_version", "")
    for field in ("homepage", "license"):
        if not merged.get(field) and isinstance(manifest.get(field), str):
            merged[field] = manifest[field]
    if not merged.get("keywords") and isinstance(manifest.get("keywords"), list):
        merged["keywords"] = manifest["keywords"]
    author = manifest.get("author")
    if isinstance(author, dict) and author.get("name"):
        merged["author"] = {k: v for k, v in author.items() if k in ("name", "email", "url")}
    return {field: merged[field] for field in store.FIELDS if field in merged}


def render(
    candidate: dict, errors: list[str], validation: dict | None, smoke: dict | None
) -> tuple[str, str]:
    """The comment and its verdict: format-ok, needs-changes or infra-error."""
    lines = [MARK, "## Intake", ""]
    if errors:
        lines.append("**Form**: needs changes")
        lines += [f"- {e}" for e in errors]
        lines += ["", "Edit the issue; the checks run again on every edit."]
        return "\n".join(lines) + "\n", "needs-changes"
    lines.append("**Form**: pass")
    verdict = "format-ok"
    if validation is None:
        lines.append("**Plugin at the tag**: not run")
        verdict = "infra-error"
    elif validation["errors"]:
        sha = (validation.get("sha") or "")[:12] or "unresolved"
        lines.append(f"**Plugin at the tag**: needs changes (commit `{sha}`)")
        lines += [f"- {e}" for e in validation["errors"]]
        verdict = "needs-changes"
    else:
        lines.append(f"**Plugin at the tag**: pass (commit `{validation['sha'][:12]}`)")
    if validation and validation.get("notes"):
        lines += ["", "Notes (informational):"] + [f"- {n}" for n in validation["notes"]]
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
        lines += ["", "Fix the plugin at a new tag and edit the issue's tag; the checks run again."]
    elif verdict == "infra-error":
        lines += ["", "The pipeline could not complete on its side; a maintainer re-runs it."]
    else:
        record = candidate_record(candidate, validation)
        lines += [
            "",
            "The format holds; the review of relevance and novelty follows on this issue.",
            "",
            f"{CANDIDATE_MARK}{json.dumps(record, ensure_ascii=False)} -->",
        ]
    return "\n".join(lines) + "\n", verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="render the intake comment and print its verdict")
    parser.add_argument("--candidate", required=True, help="intake.py --json output")
    parser.add_argument("--validation", default=None, help="validate.py --json output")
    parser.add_argument("--smoke", default=None, help="smoke.py --json output")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    intake = _read_json(args.candidate)
    if intake is None:
        print("infra-error")
        Path(args.out).write_text(f"{MARK}\n## Intake\n\nThe form could not be parsed.\n")
        return 0
    validation = _read_json(args.validation)
    smoke = _read_json(args.smoke)
    body, verdict = render(intake["candidate"], intake["errors"], validation, smoke)
    Path(args.out).write_text(body, encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
