from __future__ import annotations

import argparse

from iceberg_portfolio.config import LakehouseConfig, build_config
from iceberg_portfolio.logging_utils import configure_logging


def build_common_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--config-profile",
        default=None,
        help="Path to KEY=VALUE profile file. Environment variables still override profile values.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level for structured runtime logs.",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> LakehouseConfig:
    configure_logging(args.log_level)
    return build_config(profile_path=args.config_profile)


def parse_args(parser: argparse.ArgumentParser, argv: list[str] | None) -> argparse.Namespace:
    return parser.parse_args([] if argv is None else argv)
