PYTHON ?= python

.PHONY: install-dev format lint typecheck test check run-bronze run-silver run-gold

install-dev:
	$(PYTHON) -m pip install -e .[dev]

format:
	$(PYTHON) -m ruff format src tests

lint:
	$(PYTHON) -m ruff check src tests

typecheck:
	$(PYTHON) -m mypy src tests

test:
	$(PYTHON) -m pytest -q

check: lint typecheck test

run-bronze:
	$(PYTHON) -m iceberg_portfolio.jobs.bronze_orders

run-silver:
	$(PYTHON) -m iceberg_portfolio.jobs.silver_orders

run-gold:
	$(PYTHON) -m iceberg_portfolio.jobs.gold_orders
