PYTHON ?= python
PROFILE ?= config/profiles/local.env

.PHONY: install-dev format lint typecheck test check run-bronze run-silver run-gold run-quality run-pipeline run-pipeline-profile smoke

install-dev:
	$(PYTHON) -m pip install -e .[dev]

format:
	$(PYTHON) -m ruff format src tests scripts

lint:
	$(PYTHON) -m ruff check src tests scripts

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

run-quality:
	$(PYTHON) -m iceberg_portfolio.jobs.quality_checks

run-pipeline:
	$(PYTHON) -m iceberg_portfolio.jobs.run_pipeline

run-pipeline-profile:
	$(PYTHON) -m iceberg_portfolio.jobs.run_pipeline --config-profile $(PROFILE)

smoke:
	$(PYTHON) scripts/smoke_test.py --config-profile $(PROFILE)
