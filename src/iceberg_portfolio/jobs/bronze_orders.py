from __future__ import annotations

import logging
from pathlib import Path

from iceberg_portfolio.cli import build_common_parser, config_from_args, parse_args
from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns, write_csv_rows
from iceberg_portfolio.schemas import RAW_ORDERS_COLUMNS

LOGGER = logging.getLogger(__name__)


def run(config: LakehouseConfig) -> int:
    """Load raw rows and persist the bronze table as an idempotent overwrite."""
    raw_path = Path(config.raw_orders_path)
    bronze_path = Path(config.bronze_orders_path)

    columns, rows = read_csv_rows(raw_path)
    validate_columns(columns, RAW_ORDERS_COLUMNS, label="raw orders")
    write_csv_rows(bronze_path, RAW_ORDERS_COLUMNS, rows)
    LOGGER.info(
        "Bronze table written: table=%s path=%s rows=%d",
        config.bronze_orders_table,
        bronze_path,
        len(rows),
    )
    return len(rows)


def main(argv: list[str] | None = None) -> None:
    parser = build_common_parser("Run bronze ingest job.")
    args = parse_args(parser, argv)
    cfg = config_from_args(args)
    row_count = run(cfg)
    print(
        f"Bronze ingest complete. table={cfg.bronze_orders_table} rows={row_count} "
        f"path={cfg.bronze_orders_path}"
    )


if __name__ == "__main__":
    main()
