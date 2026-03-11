from __future__ import annotations

from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns, write_csv_rows
from iceberg_portfolio.schemas import RAW_ORDERS_COLUMNS, SILVER_ORDERS_COLUMNS


def run(config: LakehouseConfig) -> int:
    """Apply deterministic cleaning rules and write the silver table."""
    bronze_path = Path(config.bronze_orders_path)
    silver_path = Path(config.silver_orders_path)

    columns, rows = read_csv_rows(bronze_path)
    validate_columns(columns, RAW_ORDERS_COLUMNS, label="bronze orders")

    cleaned: list[dict[str, str]] = []
    for row in rows:
        amount = Decimal(row["amount"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        timestamp = datetime.fromisoformat(row["order_timestamp"]).replace(microsecond=0)
        cleaned.append(
            {
                "order_id": str(int(row["order_id"])),
                "customer_id": str(int(row["customer_id"])),
                "order_timestamp": timestamp.isoformat(),
                "status": row["status"].strip().lower(),
                "amount": f"{amount:.2f}",
                "currency": row["currency"].strip().upper(),
            }
        )

    write_csv_rows(silver_path, SILVER_ORDERS_COLUMNS, cleaned)
    return len(cleaned)


def main() -> None:
    cfg = LakehouseConfig()
    row_count = run(cfg)
    print(
        f"Silver transform complete. table={cfg.silver_orders_table} rows={row_count} "
        f"path={cfg.silver_orders_path}"
    )


if __name__ == "__main__":
    main()
