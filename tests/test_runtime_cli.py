from __future__ import annotations

import shutil
from pathlib import Path

from pytest import CaptureFixture

from iceberg_portfolio.jobs import run_pipeline


def test_run_pipeline_supports_profile_and_log_level(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    raw_path = tmp_path / "raw" / "orders.csv"
    bronze_path = tmp_path / "bronze" / "orders_raw.csv"
    silver_path = tmp_path / "silver" / "orders_clean.csv"
    gold_path = tmp_path / "gold" / "daily_revenue.csv"

    raw_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path("data/raw/orders.csv"), raw_path)

    profile = tmp_path / "profile.env"
    profile.write_text(
        "\n".join(
            [
                f"RAW_ORDERS_PATH={raw_path}",
                f"BRONZE_ORDERS_PATH={bronze_path}",
                f"SILVER_ORDERS_PATH={silver_path}",
                f"GOLD_DAILY_REVENUE_PATH={gold_path}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    run_pipeline.main(["--config-profile", str(profile), "--log-level", "DEBUG"])
    output = capsys.readouterr().out
    assert "Pipeline complete." in output
    assert "bronze_rows=5" in output
    assert "silver_rows=5" in output
    assert "gold_rows=3" in output
