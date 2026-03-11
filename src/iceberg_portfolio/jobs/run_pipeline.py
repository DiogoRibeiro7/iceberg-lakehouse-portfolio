from __future__ import annotations

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.jobs.bronze_orders import run as run_bronze
from iceberg_portfolio.jobs.gold_orders import run as run_gold
from iceberg_portfolio.jobs.silver_orders import run as run_silver
from iceberg_portfolio.quality import run_quality_checks


def main() -> None:
    cfg = LakehouseConfig()
    bronze_rows = run_bronze(cfg)
    silver_rows = run_silver(cfg)
    gold_rows = run_gold(cfg)
    quality_summary = run_quality_checks(cfg)
    print(
        "Pipeline complete. "
        f"bronze_rows={bronze_rows} "
        f"silver_rows={silver_rows} "
        f"gold_rows={len(gold_rows)} "
        f"reconciled_total={quality_summary.gold_total_revenue}"
    )


if __name__ == "__main__":
    main()
