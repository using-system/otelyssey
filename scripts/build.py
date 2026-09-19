"""Generate the listing artifacts from the store: manifest, plugin pages, README table."""

from __future__ import annotations

import json

MARKETPLACE_NAME = "otelyssey"
MARKETPLACE_REPO = "using-system/otelyssey"
OWNER = {"name": "using-system", "url": "https://github.com/using-system"}


def source_of(record: dict) -> dict:
    """The `github` source both hosts accept, `path` added when the plugin is in a subdirectory."""
    source = {"source": "github", "repo": record["repository"]}
    if record["path"]:
        source["path"] = record["path"]
    source["ref"] = record["ref"]
    source["sha"] = record["sha"]
    return source


def marketplace_json(records: dict[str, dict]) -> dict:
    plugins = []
    for name in sorted(records):
        record = records[name]
        entry = {
            "name": record["name"],
            "source": source_of(record),
            "description": record["description"],
            "version": record["version"],
            "category": record["category"],
            "keywords": record["keywords"],
            "license": record["license"],
            "author": record["author"],
        }
        if record["homepage"]:
            entry["homepage"] = record["homepage"]
        plugins.append(entry)
    return {
        "name": MARKETPLACE_NAME,
        "owner": OWNER,
        "description": "A self-run marketplace of OpenTelemetry agent plugins",
        "plugins": plugins,
    }


def render_json(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
