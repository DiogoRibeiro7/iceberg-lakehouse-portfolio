from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from iceberg_portfolio.config import LakehouseConfig
from iceberg_portfolio.jobs import bronze_orders, gold_orders, silver_orders
from iceberg_portfolio.quality import DataQualityError, run_quality_checks


def _set_pipeline_paths(monkeypatch: MonkeyPatch, tmp_path: Path) -> dict[str, Path]:
    raw_path = tmp_path / "raw" / "orders.csv"
    bronze_path = tmp_path / "bronze" / "orders_raw.csv"
    silver_path = tmp_path / "silver" / "orders_clean.csv"
    gold_path = tmp_path / "gold" / "daily_revenue.csv"

    source = Path("data/raw/orders.csv")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, raw_path)

    monkeypatch.setenv("RAW_ORDERS_PATH", str(raw_path))
    monkeypatch.setenv("BRONZE_ORDERS_PATH", str(bronze_path))
    monkeypatch.setenv("SILVER_ORDERS_PATH", str(silver_path))
    monkeypatch.setenv("GOLD_DAILY_REVENUE_PATH", str(gold_path))

    return {"raw": raw_path, "bronze": bronze_path, "silver": silver_path, "gold": gold_path}


def test_quality_checks_pass_for_pipeline_output(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    _set_pipeline_paths(monkeypatch, tmp_path)
    cfg = LakehouseConfig()

    bronze_orders.run(cfg)
    silver_orders.run(cfg)
    gold_orders.run(cfg)
    summary = run_quality_checks(cfg)

    assert summary.silver_rows == 5
    assert summary.gold_rows == 3
    assert str(summary.silver_total_amount) == "189.48"
    assert str(summary.gold_total_revenue) == "189.48"


def test_quality_checks_fail_on_cross_layer_reconciliation(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    paths = _set_pipeline_paths(monkeypatch, tmp_path)
    cfg = LakehouseConfig()

    bronze_orders.run(cfg)
    silver_orders.run(cfg)
    gold_orders.run(cfg)

    lines = paths["gold"].read_text(encoding="utf-8").splitlines()
    lines[1] = "2026-01-01,70.49"
    paths["gold"].write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(DataQualityError, match="Cross-layer quality check failed"):
        run_quality_checks(cfg)
