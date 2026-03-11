# Data Dictionary

This repository stores deterministic CSV outputs for silver and gold layers.

## Silver: `data/silver/orders_clean.csv`

| Column | Type | Description |
|---|---|---|
| `order_id` | integer (string-encoded) | Unique order identifier. |
| `customer_id` | integer (string-encoded) | Unique customer identifier. |
| `order_timestamp` | ISO-8601 timestamp | Event timestamp in local demo timezone context. |
| `status` | lowercase string | Order lifecycle status (`created`, `cancelled`, `refunded`, `updated`). |
| `amount` | decimal(12,2) (string-encoded) | Monetary amount with two decimal places. |
| `currency` | uppercase ISO-like code | Currency code (example: `EUR`). |

## Gold: `data/gold/daily_revenue.csv`

| Column | Type | Description |
|---|---|---|
| `order_date` | date (`YYYY-MM-DD`) | Day-level aggregation key derived from `order_timestamp`. |
| `revenue` | decimal(12,2) (string-encoded) | Sum of daily order amounts. |

## Enforced quality rules

- Required columns must match expected schemas exactly.
- Silver and gold outputs must be non-empty.
- Silver IDs must be positive integers.
- Silver amounts and gold revenues must be non-negative decimals.
- Gold `order_date` values must be unique.
- Cross-layer reconciliation must hold:
  - `sum(silver.amount) == sum(gold.revenue)` (rounded to two decimals).
