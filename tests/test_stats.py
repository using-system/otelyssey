import json
from pathlib import Path

from scripts import stats

FIXTURES = Path(__file__).parent / "fixtures"
RAW = json.loads((FIXTURES / "api" / "repo.json").read_text())


def test_counts_use_subscribers_as_watchers():
    assert stats.counts(RAW) == {"stars": 12, "forks": 3, "watchers": 5}


def test_refresh_rewrites_only_when_a_count_moved(tmp_path: Path, monkeypatch):
    src = FIXTURES / "store-root" / ".store" / "oddyssey.json"
    (tmp_path / ".store").mkdir()
    (tmp_path / ".store" / "oddyssey.json").write_bytes(src.read_bytes())
    monkeypatch.setattr(stats, "fetch_raw", lambda repository, token: RAW)
    monkeypatch.setattr(stats, "now", lambda: "2026-09-19T01:00:00Z")
    assert stats.refresh(tmp_path, token=None) == (["oddyssey"], {})
    record = json.loads((tmp_path / ".store" / "oddyssey.json").read_text())
    assert record["stats"] == {
        "stars": 12,
        "forks": 3,
        "watchers": 5,
        "refreshed_at": "2026-09-19T01:00:00Z",
    }
    monkeypatch.setattr(stats, "now", lambda: "2026-09-20T01:00:00Z")
    assert stats.refresh(tmp_path, token=None) == ([], {})


def test_an_unreachable_repository_is_reported_not_raised(tmp_path: Path, monkeypatch):
    src = FIXTURES / "store-root" / ".store" / "oddyssey.json"
    (tmp_path / ".store").mkdir()
    (tmp_path / ".store" / "oddyssey.json").write_bytes(src.read_bytes())

    def failing(repository, token):
        raise stats.urllib.error.HTTPError(repository, 404, "Not Found", {}, None)

    monkeypatch.setattr(stats, "fetch_raw", failing)
    changed, failed = stats.refresh(tmp_path, token=None)
    assert changed == []
    assert "oddyssey" in failed and "404" in failed["oddyssey"]
    before = src.read_bytes()
    assert (tmp_path / ".store" / "oddyssey.json").read_bytes() == before


def test_token_comes_from_the_environment(monkeypatch):
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert stats.token_from_env() is None
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    assert stats.token_from_env() == "x"
