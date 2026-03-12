from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True, capture_output=True)


def _assert_services_running(compose_file: Path) -> None:
    expected = {"minio", "nessie", "spark-iceberg"}
    result = _run(
        [
            "docker",
            "compose",
            "-f",
            str(compose_file),
            "ps",
            "--services",
            "--filter",
            "status=running",
        ]
    )
    running = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    missing = sorted(expected - running)
    if missing:
        raise RuntimeError(
            "Smoke test failed: required services are not running: "
            + ", ".join(missing)
            + ". Start stack with 'docker compose -f docker/docker-compose.yml up -d'."
        )


def _run_pipeline(profile_path: str | None) -> None:
    cmd = [sys.executable, "-m", "iceberg_portfolio.jobs.run_pipeline", "--log-level", "INFO"]
    if profile_path:
        cmd.extend(["--config-profile", profile_path])
    _run(cmd)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run local stack smoke validation.")
    parser.add_argument(
        "--compose-file",
        default="docker/docker-compose.yml",
        help="Path to docker compose file used by the local stack.",
    )
    parser.add_argument(
        "--config-profile",
        default=None,
        help="Optional KEY=VALUE profile path passed into pipeline run.",
    )
    args = parser.parse_args(argv)

    compose_file = Path(args.compose_file)
    if not compose_file.exists():
        raise FileNotFoundError(f"Compose file not found: {compose_file}")

    _assert_services_running(compose_file)
    _run_pipeline(args.config_profile)
    _assert_pipeline_outputs()
    print("Smoke test passed. Docker services healthy, pipeline run succeeded, outputs valid.")


def _assert_pipeline_outputs() -> None:
    expected_files = {
        Path("data/bronze/orders_raw.csv"): ["order_id", "customer_id"],
        Path("data/silver/orders_clean.csv"): ["order_id", "customer_id"],
        Path("data/gold/daily_revenue.csv"): ["order_date", "order_count"],
    }
    for path, required_columns in expected_files.items():
        if not path.exists():
            raise RuntimeError(f"Smoke test failed: expected output file missing: {path}")
        header = path.read_text(encoding="utf-8").splitlines()[0]
        for col in required_columns:
            if col not in header:
                raise RuntimeError(
                    f"Smoke test failed: {path} missing expected column '{col}'"
                )


if __name__ == "__main__":
    main()
