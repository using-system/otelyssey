from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_store_directory_exists():
    assert (ROOT / ".store").is_dir()


def test_scripts_package_importable():
    import scripts  # noqa: F401
