from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_flink_demo_assets_exist() -> None:
    required_paths = [
        "sql/flink_iceberg_streaming_demo.sql",
        "sql/flink_kafka_iceberg_demo.sql",
        "docs/flink_demo.md",
        "docs/flink_kafka_demo.md",
        "docker/flink/sql-client/Dockerfile",
        "docker/flink/sql-client/conf/sql-client-defaults.yaml",
        "scripts/run_flink_sql_client.py",
        "scripts/validate_flink_sink_rows.py",
    ]
    for path in required_paths:
        assert Path(path).exists(), f"Missing required Flink asset: {path}"


def test_readme_references_flink_assets() -> None:
    readme = _read("README.md").lower()
    assert "flink streaming demo" in readme
    assert "sql/flink_iceberg_streaming_demo.sql" in readme
    assert "sql/flink_kafka_iceberg_demo.sql" in readme
    assert "docs/flink_demo.md" in readme
    assert "docs/flink_kafka_demo.md" in readme


def test_flink_docs_reference_execution_helpers() -> None:
    flink_demo = _read("docs/flink_demo.md").lower()
    kafka_demo = _read("docs/flink_kafka_demo.md").lower()

    assert "python scripts/run_flink_sql_client.py" in flink_demo
    assert "python scripts/validate_flink_sink_rows.py --table gold.orders_revenue_1m" in flink_demo

    assert "python scripts/run_flink_sql_client.py" in kafka_demo
    assert (
        "python scripts/validate_flink_sink_rows.py --table gold.orders_revenue_1m_kafka"
        in kafka_demo
    )
