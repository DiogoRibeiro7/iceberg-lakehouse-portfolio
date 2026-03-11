from __future__ import annotations

import logging

from iceberg_portfolio.cli import build_common_parser, config_from_args, parse_args
from iceberg_portfolio.jobs.bronze_orders import run as run_bronze
from iceberg_portfolio.jobs.gold_orders import run as run_gold
from iceberg_portfolio.jobs.silver_orders import run as run_silver
from iceberg_portfolio.quality import run_quality_checks

LOGGER = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> None:
    parser = build_common_parser("Run bronze->silver->gold pipeline with quality checks.")
    args = parse_args(parser, argv)
    cfg = config_from_args(args)

    LOGGER.info("Starting pipeline run.")
    bronze_rows = run_bronze(cfg)
    silver_rows = run_silver(cfg)
    gold_rows = run_gold(cfg)
    quality_summary = run_quality_checks(cfg)
    LOGGER.info("Pipeline run complete.")
    print(
        "Pipeline complete. "
        f"bronze_rows={bronze_rows} "
        f"silver_rows={silver_rows} "
        f"gold_rows={len(gold_rows)} "
        f"reconciled_total={quality_summary.gold_total_revenue}"
    )


if __name__ == "__main__":
    main()
