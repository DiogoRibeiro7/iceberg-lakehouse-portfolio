from __future__ import annotations

import argparse
import re
import subprocess
import time


def _build_validation_sql(table_name: str) -> str:
    return f"""
CREATE CATALOG local WITH (
  'type' = 'iceberg',
  'catalog-type' = 'nessie',
  'uri' = 'http://nessie:19120/api/v1',
  'ref' = 'main',
  'warehouse' = 's3://warehouse/',
  's3.endpoint' = 'http://minio:9000',
  's3.path-style-access' = 'true',
  's3.access-key' = 'admin',
  's3.secret-key' = 'password123'
);
USE CATALOG local;
SELECT CONCAT('ROW_COUNT=', CAST(COUNT(*) AS STRING)) AS row_count_marker FROM {table_name};
QUIT;
"""


def _run_sql_client(compose_file: str, sql: str) -> str:
    result = subprocess.run(
        ["docker", "compose", "-f", compose_file, "run", "--rm", "-T", "flink-sql-client"],
        input=sql,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Flink SQL client command failed.")
    return result.stdout


def _extract_row_count(output: str) -> int | None:
    match = re.search(r"ROW_COUNT=(\d+)", output)
    if not match:
        return None
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate that a Flink Iceberg sink table has rows."
    )
    parser.add_argument(
        "--compose-file",
        default="docker/docker-compose.yml",
        help="Path to docker compose file.",
    )
    parser.add_argument(
        "--table",
        default="gold.orders_revenue_1m",
        help="Fully-qualified Iceberg table name to validate.",
    )
    parser.add_argument(
        "--min-rows",
        default=1,
        type=int,
        help="Minimum row count required for validation.",
    )
    parser.add_argument(
        "--timeout-sec",
        default=120,
        type=int,
        help="Max wait time for rows to appear.",
    )
    parser.add_argument(
        "--poll-sec",
        default=5,
        type=int,
        help="Polling interval in seconds.",
    )
    args = parser.parse_args()

    deadline = time.time() + args.timeout_sec
    sql = _build_validation_sql(args.table)

    while time.time() < deadline:
        try:
            output = _run_sql_client(args.compose_file, sql)
            row_count = _extract_row_count(output)
            if row_count is not None and row_count >= args.min_rows:
                print(
                    f"Validation passed: table '{args.table}' has {row_count} rows "
                    f"(required >= {args.min_rows})."
                )
                return
        except RuntimeError:
            pass
        time.sleep(args.poll_sec)

    raise RuntimeError(
        f"Validation failed: table '{args.table}' did not reach {args.min_rows} rows "
        f"within {args.timeout_sec} seconds."
    )


if __name__ == "__main__":
    main()
