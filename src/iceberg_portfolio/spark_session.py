from __future__ import annotations

from iceberg_portfolio.config import LakehouseConfig


def build_spark_session() -> dict[str, str]:
    """Return a minimal placeholder config structure for local Spark setup.

    In a full implementation, this function would create a SparkSession configured
    with Iceberg, Nessie, and MinIO integration.
    """
    cfg = LakehouseConfig()
    return {
        "catalog_name": cfg.catalog_name,
        "warehouse": cfg.warehouse,
        "nessie_uri": cfg.nessie_uri,
        "s3_endpoint": cfg.s3_endpoint,
    }
