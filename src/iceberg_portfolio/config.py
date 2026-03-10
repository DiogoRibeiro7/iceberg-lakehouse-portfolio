from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LakehouseConfig:
    """Application settings for the local Iceberg portfolio repository."""

    catalog_name: str = os.getenv("CATALOG_NAME", "local")
    warehouse: str = os.getenv("ICEBERG_WAREHOUSE", "s3://warehouse/")
    nessie_uri: str = os.getenv("NESSIE_URI", "http://localhost:19120/api/v1")
    s3_endpoint: str = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    s3_access_key: str = os.getenv("AWS_ACCESS_KEY_ID", "admin")
    s3_secret_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "password123")
