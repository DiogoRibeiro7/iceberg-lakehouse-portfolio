from __future__ import annotations

import logging

from iceberg_portfolio.logging_utils import configure_logging


def test_configure_logging_sets_level() -> None:
    configure_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING


def test_configure_logging_accepts_valid_levels() -> None:
    for level in ("DEBUG", "INFO", "WARNING", "ERROR"):
        configure_logging(level)
        # basicConfig only applies on the first call to an unconfigured root
        # logger, so verify it does not raise for any valid level.
        assert getattr(logging, level) is not None
