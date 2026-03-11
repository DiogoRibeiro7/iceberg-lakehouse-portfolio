from pathlib import Path

from pytest import MonkeyPatch

from iceberg_portfolio.config import LakehouseConfig, build_config


def test_default_catalog_name() -> None:
    cfg = LakehouseConfig()
    assert cfg.catalog_name == "local"


def test_default_pipeline_paths_and_tables() -> None:
    cfg = LakehouseConfig()
    assert cfg.raw_orders_path == "data/raw/orders.csv"
    assert cfg.bronze_orders_path == "data/bronze/orders_raw.csv"
    assert cfg.silver_orders_path == "data/silver/orders_clean.csv"
    assert cfg.gold_daily_revenue_path == "data/gold/daily_revenue.csv"
    assert cfg.bronze_orders_table == "bronze.orders_raw"
    assert cfg.silver_orders_table == "silver.orders_clean"
    assert cfg.gold_daily_revenue_table == "gold.daily_revenue"


def test_env_override_applied_at_instance_creation(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOG_NAME", "analytics")
    cfg = LakehouseConfig()
    assert cfg.catalog_name == "analytics"


def test_pipeline_paths_can_be_overridden(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BRONZE_ORDERS_PATH", "tmp/bronze.csv")
    monkeypatch.setenv("SILVER_ORDERS_PATH", "tmp/silver.csv")
    cfg = LakehouseConfig()
    assert cfg.bronze_orders_path == "tmp/bronze.csv"
    assert cfg.silver_orders_path == "tmp/silver.csv"


def test_env_change_reflected_in_new_instances(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOG_NAME", "first")
    first = LakehouseConfig()
    monkeypatch.setenv("CATALOG_NAME", "second")
    second = LakehouseConfig()

    assert first.catalog_name == "first"
    assert second.catalog_name == "second"


def test_build_config_loads_profile_file(tmp_path: Path) -> None:
    profile = tmp_path / "demo.env"
    profile.write_text(
        "\n".join(
            [
                "CATALOG_NAME=from_profile",
                "RAW_ORDERS_PATH=data/demo.csv",
                "GOLD_DAILY_REVENUE_TABLE=gold.demo",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    cfg = build_config(str(profile))
    assert cfg.catalog_name == "from_profile"
    assert cfg.raw_orders_path == "data/demo.csv"
    assert cfg.gold_daily_revenue_table == "gold.demo"


def test_environment_overrides_profile(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    profile = tmp_path / "demo.env"
    profile.write_text("CATALOG_NAME=from_profile\n", encoding="utf-8")
    monkeypatch.setenv("CATALOG_NAME", "from_env")

    cfg = build_config(str(profile))
    assert cfg.catalog_name == "from_env"
