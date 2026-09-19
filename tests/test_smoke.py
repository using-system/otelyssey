import json
from pathlib import Path

from scripts import smoke

PLUGIN = Path(__file__).parent / "fixtures" / "plugins" / "valid"


def test_ephemeral_marketplace_points_at_a_copy(tmp_path: Path):
    market = smoke.ephemeral_marketplace(tmp_path, "my-otel-plugin", PLUGIN)
    manifest = json.loads((market / ".claude-plugin" / "marketplace.json").read_text())
    assert manifest["name"] == "otelyssey-intake"
    [entry] = manifest["plugins"]
    assert entry == {"name": "my-otel-plugin", "source": "./plugin"}
    assert (market / "plugin" / "plugin.json").is_file()


def test_unavailable_host_is_not_a_failure(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    market = smoke.ephemeral_marketplace(tmp_path, "my-otel-plugin", PLUGIN)
    status, output = smoke.install("copilot", market, "my-otel-plugin", tmp_path / "home")
    assert status == "unavailable"
    assert "copilot" in output


def test_smoke_runs_every_host(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    result = smoke.smoke("my-otel-plugin", PLUGIN, tmp_path)
    assert set(result) == {"copilot", "claude"}
    assert all(r["status"] == "unavailable" for r in result.values())


def test_smoke_twice_on_one_workdir_is_clean(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    first = smoke.smoke("my-otel-plugin", PLUGIN, tmp_path)
    second = smoke.smoke("my-otel-plugin", PLUGIN, tmp_path)
    assert second == first
    stale = tmp_path / "home-copilot" / "stale.txt"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("from a previous run\n")
    monkeypatch.setattr(smoke.shutil, "which", lambda host: "/bin/true")
    monkeypatch.setattr(smoke, "_run", lambda args, home: (0, "my-otel-plugin"))
    third = smoke.smoke("my-otel-plugin", PLUGIN, tmp_path)
    assert all(r["status"] == "pass" for r in third.values())
    assert not stale.exists()
