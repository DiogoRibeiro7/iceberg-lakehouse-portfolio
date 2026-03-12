from __future__ import annotations

import argparse
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Launch Flink SQL client container for the local demo stack."
    )
    parser.add_argument(
        "--compose-file",
        default="docker/docker-compose.yml",
        help="Path to docker compose file.",
    )
    args = parser.parse_args()

    subprocess.run(
        ["docker", "compose", "-f", args.compose_file, "run", "--rm", "flink-sql-client"],
        check=True,
    )


if __name__ == "__main__":
    main()
