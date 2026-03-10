from __future__ import annotations

from pathlib import Path
import csv
from datetime import datetime


def main() -> None:
    """Apply simple cleaning and typing rules for the silver layer."""
    path = Path("data/raw/orders.csv")
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    cleaned = []
    for row in rows:
        cleaned.append(
            {
                "order_id": int(row["order_id"]),
                "customer_id": int(row["customer_id"]),
                "order_timestamp": datetime.fromisoformat(row["order_timestamp"]),
                "status": row["status"].strip().lower(),
                "amount": float(row["amount"]),
                "currency": row["currency"].strip().upper(),
            }
        )

    print(f"Silver transform complete. Prepared {len(cleaned)} typed rows.")


if __name__ == "__main__":
    main()
