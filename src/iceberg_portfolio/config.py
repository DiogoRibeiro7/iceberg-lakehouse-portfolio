from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class LakehouseConfig:
    """Application settings for the local Iceberg portfolio repository."""

    catalog_name: str = field(default_factory=lambda: os.getenv("CATALOG_NAME", "local"))
    warehouse: str = field(
        default_factory=lambda: os.getenv("ICEBERG_WAREHOUSE", "s3://warehouse/")
    )
    nessie_uri: str = field(
        default_factory=lambda: os.getenv("NESSIE_URI", "http://localhost:19120/api/v1")
    )
    s3_endpoint: str = field(
        default_factory=lambda: os.getenv("S3_ENDPOINT", "http://localhost:9000")
    )
    s3_access_key: str = field(default_factory=lambda: os.getenv("AWS_ACCESS_KEY_ID", "admin"))
    s3_secret_key: str = field(
        default_factory=lambda: os.getenv("AWS_SECRET_ACCESS_KEY", "password123")
    )
    raw_orders_path: str = field(
        default_factory=lambda: os.getenv("RAW_ORDERS_PATH", "data/raw/orders.csv")
    )
    bronze_orders_path: str = field(
        default_factory=lambda: os.getenv("BRONZE_ORDERS_PATH", "data/bronze/orders_raw.csv")
    )
    silver_orders_path: str = field(
        default_factory=lambda: os.getenv("SILVER_ORDERS_PATH", "data/silver/orders_clean.csv")
    )
    gold_daily_revenue_path: str = field(
        default_factory=lambda: os.getenv("GOLD_DAILY_REVENUE_PATH", "data/gold/daily_revenue.csv")
    )
    bronze_orders_table: str = field(
        default_factory=lambda: os.getenv("BRONZE_ORDERS_TABLE", "bronze.orders_raw")
    )
    silver_orders_table: str = field(
        default_factory=lambda: os.getenv("SILVER_ORDERS_TABLE", "silver.orders_clean")
    )
    gold_daily_revenue_table: str = field(
        default_factory=lambda: os.getenv("GOLD_DAILY_REVENUE_TABLE", "gold.daily_revenue")
    )
