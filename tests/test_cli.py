from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from iceberg_portfolio.cli import build_common_parser, config_from_args, parse_args


def test_build_common_parser_returns_parser_with_expected_flags() -> None:
    parser = build_common_parser("test description")
    assert isinstance(parser, argparse.ArgumentParser)
    args = parser.parse_args([])
    assert args.config_profile is None
    assert args.log_level == "INFO"


def test_parse_args_with_all_flags() -> None:
    parser = build_common_parser("test")
    args = parse_args(parser, ["--config-profile", "some.env", "--log-level", "DEBUG"])
    assert args.config_profile == "some.env"
    assert args.log_level == "DEBUG"


def test_parse_args_none_treated_as_empty() -> None:
    parser = build_common_parser("test")
    args = parse_args(parser, None)
    assert args.config_profile is None
    assert args.log_level == "INFO"


def test_invalid_log_level_rejected() -> None:
    parser = build_common_parser("test")
    with pytest.raises(SystemExit):
        parse_args(parser, ["--log-level", "VERBOSE"])


def test_config_from_args_returns_config_with_defaults() -> None:
    parser = build_common_parser("test")
    args = parse_args(parser, [])
    cfg = config_from_args(args)
    assert cfg.catalog_name == "local"


def test_config_from_args_loads_profile(tmp_path: Path) -> None:
    profile = tmp_path / "test.env"
    profile.write_text("CATALOG_NAME=test_catalog\n", encoding="utf-8")

    parser = build_common_parser("test")
    args = parse_args(parser, ["--config-profile", str(profile)])
    cfg = config_from_args(args)
    assert cfg.catalog_name == "test_catalog"
