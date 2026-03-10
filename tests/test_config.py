from iceberg_portfolio.config import LakehouseConfig


def test_default_catalog_name() -> None:
    cfg = LakehouseConfig()
    assert cfg.catalog_name == "local"
