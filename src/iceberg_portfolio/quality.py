from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns
from iceberg_portfolio.schemas import GOLD_DAILY_REVENUE_COLUMNS, SILVER_ORDERS_COLUMNS


class DataQualityError(ValueError):
    """Raised when one or more data quality rules fail."""


@dataclass(frozen=True)
class QualitySummary:
    silver_rows: int
    gold_rows: int
    silver_total_amount: Decimal
    gold_total_revenue: Decimal


def _parse_decimal(value: str, *, field: str, row_number: int) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as exc:
        raise DataQualityError(
            f"Invalid decimal in {field} at row {row_number}: '{value}'."
        ) from exc


def _validate_silver_rows(rows: list[dict[str, str]]) -> Decimal:
    if not rows:
        raise DataQualityError("Silver quality check failed: table is empty.")

    allowed_statuses = {"created", "cancelled", "refunded", "updated"}
    total_amount = Decimal("0.00")

    for idx, row in enumerate(rows, start=1):
        for key in SILVER_ORDERS_COLUMNS:
            if row.get(key, "").strip() == "":
                raise DataQualityError(
                    f"Silver quality check failed: '{key}' is empty at row {idx}."
                )

        order_id = int(row["order_id"])
        customer_id = int(row["customer_id"])
        if order_id <= 0 or customer_id <= 0:
            raise DataQualityError(
                f"Silver quality check failed: IDs must be positive at row {idx}."
            )

        datetime.fromisoformat(row["order_timestamp"])

        status = row["status"]
        if status not in allowed_statuses:
            raise DataQualityError(
                f"Silver quality check failed: invalid status '{status}' at row {idx}."
            )

        currency = row["currency"]
        if len(currency) != 3 or currency != currency.upper():
            raise DataQualityError(
                f"Silver quality check failed: invalid currency '{currency}' at row {idx}."
            )

        amount = _parse_decimal(row["amount"], field="amount", row_number=idx)
        if amount < 0:
            raise DataQualityError(
                f"Silver quality check failed: negative amount '{amount}' at row {idx}."
            )
        total_amount += amount

    return total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _validate_gold_rows(rows: list[dict[str, str]]) -> Decimal:
    if not rows:
        raise DataQualityError("Gold quality check failed: table is empty.")

    seen_dates: set[str] = set()
    total_revenue = Decimal("0.00")

    for idx, row in enumerate(rows, start=1):
        for key in GOLD_DAILY_REVENUE_COLUMNS:
            if row.get(key, "").strip() == "":
                raise DataQualityError(f"Gold quality check failed: '{key}' is empty at row {idx}.")

        order_date = row["order_date"]
        datetime.strptime(order_date, "%Y-%m-%d")
        if order_date in seen_dates:
            raise DataQualityError(
                f"Gold quality check failed: duplicate order_date '{order_date}'."
            )
        seen_dates.add(order_date)

        revenue = _parse_decimal(row["revenue"], field="revenue", row_number=idx)
        if revenue < 0:
            raise DataQualityError(
                f"Gold quality check failed: negative revenue '{revenue}' at row {idx}."
            )
        total_revenue += revenue

    return total_revenue.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def run_quality_checks(config: LakehouseConfig) -> QualitySummary:
    silver_path = Path(config.silver_orders_path)
    gold_path = Path(config.gold_daily_revenue_path)

    silver_columns, silver_rows = read_csv_rows(silver_path)
    validate_columns(silver_columns, SILVER_ORDERS_COLUMNS, label="silver orders")

    gold_columns, gold_rows = read_csv_rows(gold_path)
    validate_columns(gold_columns, GOLD_DAILY_REVENUE_COLUMNS, label="gold daily revenue")

    silver_total = _validate_silver_rows(silver_rows)
    gold_total = _validate_gold_rows(gold_rows)

    if silver_total != gold_total:
        raise DataQualityError(
            "Cross-layer quality check failed: "
            f"silver total amount {silver_total} != gold total revenue {gold_total}."
        )

    return QualitySummary(
        silver_rows=len(silver_rows),
        gold_rows=len(gold_rows),
        silver_total_amount=silver_total,
        gold_total_revenue=gold_total,
    )
