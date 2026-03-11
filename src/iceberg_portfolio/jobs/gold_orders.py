from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns, write_csv_rows
from iceberg_portfolio.schemas import GOLD_DAILY_REVENUE_COLUMNS, SILVER_ORDERS_COLUMNS


def run(config: LakehouseConfig) -> list[dict[str, str]]:
    """Aggregate silver orders into deterministic daily revenue records."""
    silver_path = Path(config.silver_orders_path)
    gold_path = Path(config.gold_daily_revenue_path)

    columns, rows = read_csv_rows(silver_path)
    validate_columns(columns, SILVER_ORDERS_COLUMNS, label="silver orders")

    revenue_by_day: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))

    for row in rows:
        order_day = datetime.fromisoformat(row["order_timestamp"]).date().isoformat()
        revenue_by_day[order_day] += Decimal(row["amount"])

    aggregated: list[dict[str, str]] = []
    for order_day in sorted(revenue_by_day):
        revenue = revenue_by_day[order_day].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        aggregated.append({"order_date": order_day, "revenue": f"{revenue:.2f}"})

    write_csv_rows(gold_path, GOLD_DAILY_REVENUE_COLUMNS, aggregated)
    return aggregated


def main() -> None:
    cfg = LakehouseConfig()
    daily_revenue = run(cfg)
    row_count = len(daily_revenue)
    print(
        f"Gold aggregation complete. table={cfg.gold_daily_revenue_table} rows={row_count} "
        f"path={cfg.gold_daily_revenue_path}"
    )
    for row in daily_revenue:
        print(f"{row['order_date']}: revenue={row['revenue']}")


if __name__ == "__main__":
    main()
