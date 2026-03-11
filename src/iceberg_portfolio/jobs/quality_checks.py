from __future__ import annotations

import logging

from iceberg_portfolio.cli import build_common_parser, config_from_args, parse_args
from iceberg_portfolio.quality import run_quality_checks

LOGGER = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> None:
    parser = build_common_parser("Run quality checks on silver and gold outputs.")
    args = parse_args(parser, argv)
    cfg = config_from_args(args)
    summary = run_quality_checks(cfg)
    LOGGER.info(
        "Quality checks passed: silver_rows=%d gold_rows=%d silver_total=%s gold_total=%s",
        summary.silver_rows,
        summary.gold_rows,
        summary.silver_total_amount,
        summary.gold_total_revenue,
    )
    print(
        "Quality checks passed. "
        f"silver_rows={summary.silver_rows} "
        f"gold_rows={summary.gold_rows} "
        f"silver_total={summary.silver_total_amount} "
        f"gold_total={summary.gold_total_revenue}"
    )


if __name__ == "__main__":
    main()
