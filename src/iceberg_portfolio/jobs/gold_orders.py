from __future__ import annotations

from pathlib import Path
import csv
from collections import defaultdict
from datetime import datetime


def main() -> None:
    """Create a simple daily revenue aggregation for the gold layer."""
    path = Path("data/raw/orders.csv")
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    revenue_by_day: dict[str, float] = defaultdict(float)

    for row in rows:
        order_day = datetime.fromisoformat(row["order_timestamp"]).date().isoformat()
        revenue_by_day[order_day] += float(row["amount"])

    for order_day, revenue in sorted(revenue_by_day.items()):
        print(f"{order_day}: revenue={revenue:.2f}")


if __name__ == "__main__":
    main()
