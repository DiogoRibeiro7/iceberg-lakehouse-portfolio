from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from iceberg_portfolio.jobs import bronze_orders, gold_orders, silver_orders


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    monkeypatch.setenv("BRONZE_ORDERS_TABLE", "bronze.orders_raw_test")
    monkeypatch.setenv("SILVER_ORDERS_TABLE", "silver.orders_clean_test")
    monkeypatch.setenv("GOLD_DAILY_REVENUE_TABLE", "gold.daily_revenue_test")

    return {
        "raw": raw_path,
        "bronze": bronze_path,
        "silver": silver_path,
        "gold": gold_path,
    }


def test_bronze_job_reports_rows_and_target_table(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    paths = _set_pipeline_paths(monkeypatch, tmp_path)
    bronze_orders.main()
    output = capsys.readouterr().out
    assert "Bronze ingest complete. table=bronze.orders_raw_test rows=5" in output
    assert f"path={paths['bronze']}" in output


def test_silver_job_reports_rows_and_target_table(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    paths = _set_pipeline_paths(monkeypatch, tmp_path)
    bronze_orders.main()
    silver_orders.main()
    output = capsys.readouterr().out
    assert "Silver transform complete. table=silver.orders_clean_test rows=5" in output
    assert f"path={paths['silver']}" in output


def test_gold_job_reports_daily_revenue(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    _set_pipeline_paths(monkeypatch, tmp_path)
    bronze_orders.main()
    silver_orders.main()
    gold_orders.main()
    output = capsys.readouterr().out.strip().splitlines()
    assert any(
        "Gold aggregation complete. table=gold.daily_revenue_test rows=3" in line for line in output
    )
    assert output[-3:] == [
        "2026-01-01: revenue=69.49",
        "2026-01-02: revenue=111.00",
        "2026-01-03: revenue=8.99",
    ]


def test_pipeline_writes_expected_schemas_and_is_idempotent(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    paths = _set_pipeline_paths(monkeypatch, tmp_path)

    bronze_orders.main()
    silver_orders.main()
    gold_orders.main()

    bronze_content_before = paths["bronze"].read_text(encoding="utf-8")
    silver_content_before = paths["silver"].read_text(encoding="utf-8")
    gold_content_before = paths["gold"].read_text(encoding="utf-8")
    hashes_before = {
        layer: _file_sha256(path)
        for layer, path in paths.items()
        if layer in {"bronze", "silver", "gold"}
    }

    bronze_orders.main()
    silver_orders.main()
    gold_orders.main()

    assert paths["bronze"].read_text(encoding="utf-8") == bronze_content_before
    assert paths["silver"].read_text(encoding="utf-8") == silver_content_before
    assert paths["gold"].read_text(encoding="utf-8") == gold_content_before
    assert _file_sha256(paths["bronze"]) == hashes_before["bronze"]
    assert _file_sha256(paths["silver"]) == hashes_before["silver"]
    assert _file_sha256(paths["gold"]) == hashes_before["gold"]

    assert bronze_content_before.splitlines()[0] == (
        "order_id,customer_id,order_timestamp,status,amount,currency"
    )
    assert silver_content_before.splitlines()[0] == (
        "order_id,customer_id,order_timestamp,status,amount,currency"
    )
    assert gold_content_before.splitlines()[0] == "order_date,revenue"
    assert gold_content_before.splitlines()[1:] == [
        "2026-01-01,69.49",
        "2026-01-02,111.00",
        "2026-01-03,8.99",
    ]
