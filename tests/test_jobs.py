from __future__ import annotations

from pytest import CaptureFixture

from iceberg_portfolio.jobs import bronze_orders, gold_orders, silver_orders


def test_bronze_job_reports_loaded_rows(capsys: CaptureFixture[str]) -> None:
    bronze_orders.main()
    output = capsys.readouterr().out
    assert "Bronze ingest complete. Loaded 5 rows" in output


def test_silver_job_reports_typed_rows(capsys: CaptureFixture[str]) -> None:
    silver_orders.main()
    output = capsys.readouterr().out
    assert "Silver transform complete. Prepared 5 typed rows." in output


def test_gold_job_reports_daily_revenue(capsys: CaptureFixture[str]) -> None:
    gold_orders.main()
    output = capsys.readouterr().out.strip().splitlines()
    assert output == [
        "2026-01-01: revenue=69.49",
        "2026-01-02: revenue=111.00",
        "2026-01-03: revenue=8.99",
    ]
