from __future__ import annotations

from pathlib import Path

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns, write_csv_rows
from iceberg_portfolio.schemas import RAW_ORDERS_COLUMNS


def run(config: LakehouseConfig) -> int:
    """Load raw rows and persist the bronze table as an idempotent overwrite."""
    raw_path = Path(config.raw_orders_path)
    bronze_path = Path(config.bronze_orders_path)

    columns, rows = read_csv_rows(raw_path)
    validate_columns(columns, RAW_ORDERS_COLUMNS, label="raw orders")
    write_csv_rows(bronze_path, RAW_ORDERS_COLUMNS, rows)
    return len(rows)


def main() -> None:
    cfg = LakehouseConfig()
    row_count = run(cfg)
    print(
        f"Bronze ingest complete. table={cfg.bronze_orders_table} rows={row_count} "
        f"path={cfg.bronze_orders_path}"
    )


if __name__ == "__main__":
    main()
