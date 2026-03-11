from __future__ import annotations

import csv
from pathlib import Path


def main() -> None:
    """Load raw order rows from the sample CSV.

    This placeholder job keeps the bronze layer concept explicit: ingest raw data
    with minimal interpretation.
    """
    path = Path("data/raw/orders.csv")
    with path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    print(f"Bronze ingest complete. Loaded {len(rows)} rows from {path}.")


if __name__ == "__main__":
    main()
