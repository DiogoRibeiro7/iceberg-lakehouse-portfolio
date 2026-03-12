from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _read_profile(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid config profile line: '{raw_line}'")
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


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

    @classmethod
    def from_mapping(cls, values: dict[str, str]) -> LakehouseConfig:
        return cls(
            catalog_name=values.get("CATALOG_NAME", "local"),
            warehouse=values.get("ICEBERG_WAREHOUSE", "s3://warehouse/"),
            nessie_uri=values.get("NESSIE_URI", "http://localhost:19120/api/v1"),
            s3_endpoint=values.get("S3_ENDPOINT", "http://localhost:9000"),
            s3_access_key=values.get("AWS_ACCESS_KEY_ID", "admin"),
            s3_secret_key=values.get("AWS_SECRET_ACCESS_KEY", "password123"),
            raw_orders_path=values.get("RAW_ORDERS_PATH", "data/raw/orders.csv"),
            bronze_orders_path=values.get("BRONZE_ORDERS_PATH", "data/bronze/orders_raw.csv"),
            silver_orders_path=values.get("SILVER_ORDERS_PATH", "data/silver/orders_clean.csv"),
            gold_daily_revenue_path=values.get(
                "GOLD_DAILY_REVENUE_PATH", "data/gold/daily_revenue.csv"
            ),
            bronze_orders_table=values.get("BRONZE_ORDERS_TABLE", "bronze.orders_raw"),
            silver_orders_table=values.get("SILVER_ORDERS_TABLE", "silver.orders_clean"),
            gold_daily_revenue_table=values.get("GOLD_DAILY_REVENUE_TABLE", "gold.daily_revenue"),
        )


def build_config(profile_path: str | None = None) -> LakehouseConfig:
    merged: dict[str, str] = {}
    if profile_path:
        merged.update(_read_profile(Path(profile_path)))
    merged.update({k: v for k, v in os.environ.items() if isinstance(v, str)})
    return LakehouseConfig.from_mapping(merged)
