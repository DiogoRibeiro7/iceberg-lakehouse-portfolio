from pytest import MonkeyPatch

from iceberg_portfolio.config import LakehouseConfig


def test_default_catalog_name() -> None:
    cfg = LakehouseConfig()
    assert cfg.catalog_name == "local"


def test_env_override_applied_at_instance_creation(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOG_NAME", "analytics")
    cfg = LakehouseConfig()
    assert cfg.catalog_name == "analytics"


def test_env_change_reflected_in_new_instances(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOG_NAME", "first")
    first = LakehouseConfig()
    monkeypatch.setenv("CATALOG_NAME", "second")
    second = LakehouseConfig()

    assert first.catalog_name == "first"
    assert second.catalog_name == "second"
