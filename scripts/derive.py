"""The record's fields, from the validated manifest first and the repository's metadata next.

The form gives the repository and the path only: the manifest at the validated commit is the
source of every other field, the repository's GitHub metadata fills what it leaves out, and
what neither gives is an error the contributor fixes in plugin.json. No text of the form
enters the record.
"""

from __future__ import annotations

import argparse
import http.client
import json
import sys
from pathlib import Path

from scripts import stats, store

# the store's field, the manifest's key, the repository metadata's key
FALLBACKS = (("description", "description", "description"), ("license", "license", "license"))
# what the store adds at the admission, so its rules can be run on the record here
PLACEHOLDERS = {
    "category": store.CATEGORIES[0],
    "admitted_at": "1970-01-01",
    "stats": {"stars": 0, "forks": 0, "watchers": 0, "refreshed_at": "1970-01-01T00:00:00Z"},
}


def metadata(raw: dict) -> dict:
    """What the repository's GitHub API object gives the record: description, license, homepage,
    topics, and its owner as an author."""
    license_ = raw.get("license") or {}
    spdx = license_.get("spdx_id") if isinstance(license_, dict) else None
    owner = raw.get("owner") or {}
    return {
        "description": raw.get("description") or "",
        "license": spdx if isinstance(spdx, str) and spdx != "NOASSERTION" else "",
        "homepage": raw.get("homepage") or "",
        "topics": [t for t in raw.get("topics") or [] if isinstance(t, str)],
        "owner": {
            "name": owner.get("login") or "",
            "url": owner.get("html_url") or "",
        },
    }


def fetch_metadata(repository: str, token: str | None) -> dict:
    return metadata(stats.fetch_raw(repository, token))


def _text(value: object) -> str:
    return " ".join(value.split()) if isinstance(value, str) else ""


def _url(value: object) -> str:
    text = _text(value)
    return text if store.URL_RE.match(text) else ""


def derive(candidate: dict, validation: dict, meta: dict) -> tuple[dict, list[str], list[str]]:
    """The record (without category, admitted_at, stats), its errors, and one line per field
    that the repository's metadata gave instead of the manifest."""
    manifest = validation["manifest"]
    errors: list[str] = []
    from_repository: list[str] = []
    record = {
        "name": manifest["name"],
        "repository": candidate["repository"],
        "path": candidate["path"],
        "ref": candidate["ref"],
        "sha": validation["sha"],
        "version": manifest["version"],
        "submitted_in": candidate["submitted_in"],
    }
    for field, key, meta_key in FALLBACKS:
        value = _text(manifest.get(key))
        if not value and _text(meta.get(meta_key)):
            value = _text(meta[meta_key])
            from_repository.append(field)
        record[field] = value
    # a homepage is an https url or nothing, from either source: GitHub's field is free text
    record["homepage"] = _url(manifest.get("homepage"))
    if not record["homepage"] and _url(meta.get("homepage")):
        record["homepage"] = _url(meta["homepage"])
        from_repository.append("homepage")
    author = manifest.get("author")
    if isinstance(author, dict) and _text(author.get("name")):
        record["author"] = {"name": _text(author["name"])}
        for key in ("email", "url"):
            if _text(author.get(key)):
                record["author"][key] = _text(author[key])
        if "url" in record["author"] and not store.URL_RE.match(record["author"]["url"]):
            del record["author"]["url"]
    else:
        owner = meta.get("owner") or {}
        record["author"] = {"name": _text(owner.get("name"))}
        if store.URL_RE.match(_text(owner.get("url"))):
            record["author"]["url"] = _text(owner["url"])
        if record["author"]["name"]:
            from_repository.append("author")
    keywords = manifest.get("keywords")
    if isinstance(keywords, list) and any(_text(k) for k in keywords):
        record["keywords"] = [_text(k).lower() for k in keywords if _text(k)]
    else:
        record["keywords"] = [t.lower() for t in meta.get("topics") or []]
        if record["keywords"]:
            from_repository.append("keywords")
    for field in ("description", "license"):
        if not record[field]:
            errors.append(
                f"plugin.json: no {field}, and the repository has none either: add a {field}"
            )
    if not record["author"]["name"]:
        errors.append("plugin.json: no author, and the repository's owner could not be read")
    ordered = {field: record[field] for field in store.FIELDS if field in record}
    # the store's own rules (a control character, a version, an email), so a record the
    # admission would refuse is a needs-changes here, not a failed admission after a ruling
    if not errors:
        errors += [
            f"plugin.json: {line}" for line in store.validate_record({**ordered, **PLACEHOLDERS})
        ]
    return ordered, errors, from_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="derive the record from the validated manifest")
    parser.add_argument("--candidate", required=True, help="intake.py --json output")
    parser.add_argument("--validation", required=True, help="validate.py --json output")
    parser.add_argument("--out", required=True, help="{record, errors, from_repository} JSON")
    args = parser.parse_args(argv)
    candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))["candidate"]
    validation = json.loads(Path(args.validation).read_text(encoding="utf-8"))
    if validation["errors"]:
        print("the plugin does not validate: nothing to derive", file=sys.stderr)
        return 2
    try:
        meta = fetch_metadata(candidate["repository"], stats.token_from_env())
    except (OSError, http.client.HTTPException, ValueError) as error:
        # URLError and timeouts are OSErrors; a dropped response is an HTTPException
        print(f"{candidate['repository']}: metadata unreadable ({error})", file=sys.stderr)
        return 2
    record, errors, from_repository = derive(candidate, validation, meta)
    Path(args.out).write_text(
        json.dumps(
            {"record": record, "errors": errors, "from_repository": from_repository}, indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
