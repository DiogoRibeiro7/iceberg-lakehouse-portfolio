from __future__ import annotations

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.quality import run_quality_checks


def main() -> None:
    cfg = LakehouseConfig()
    summary = run_quality_checks(cfg)
    print(
        "Quality checks passed. "
        f"silver_rows={summary.silver_rows} "
        f"gold_rows={summary.gold_rows} "
        f"silver_total={summary.silver_total_amount} "
        f"gold_total={summary.gold_total_revenue}"
    )


if __name__ == "__main__":
    main()
