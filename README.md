# Iceberg Lakehouse Portfolio

[![CI](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/actions/workflows/ci.yml/badge.svg)](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/actions/workflows/ci.yml)
[![Integration Smoke](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/actions/workflows/integration-smoke.yml/badge.svg)](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/actions/workflows/integration-smoke.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A580%25-brightgreen)](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/actions/workflows/ci.yml)
[![Dependabot](https://img.shields.io/badge/dependabot-enabled-025E8C)](https://github.com/DiogoRibeiro7/iceberg-lakehouse-portfolio/security/dependabot)
[![Zenodo](https://img.shields.io/badge/Zenodo-ready-blue)](https://zenodo.org/)

Portfolio repository showcasing practical Apache Iceberg lakehouse engineering skills with Spark, MinIO, and Nessie.

## What this repo demonstrates

- Local lakehouse stack with **Spark + Iceberg + MinIO + Nessie**
- Simple **bronze / silver / gold** medallion pipeline
- Sample analyst-friendly SQL queries
- Iceberg demo assets for:
  - time travel
  - schema evolution
  - merge/upsert/delete
  - Nessie branching
  - maintenance operations

## Architecture

- **MinIO**: local S3-compatible object storage
- **Nessie**: catalog and branching layer
- **Spark**: processing engine
- **Iceberg**: table format

## Prerequisites

- Python 3.10+
- Docker Desktop (or Docker Engine + Compose v2)
- Git
- Optional for `make` targets: GNU Make

## Repository layout

```text
.
├── data/
│   └── raw/orders.csv
├── config/
│   └── profiles/local.env
├── docker/
│   └── docker-compose.yml
├── docs/
│   ├── architecture.md
│   ├── aws_mapping.md
│   ├── data_dictionary.md
│   ├── demo_walkthrough.md
│   ├── maintenance_demo.md
│   ├── nessie_branching_demo.md
│   ├── phase2_demos.md
│   ├── roadmap.md
│   └── sample_output/
│       ├── pipeline_run.txt
│       ├── quality_checks.txt
│       ├── test_suite.txt
│       └── data_preview.txt
├── sql/
│   ├── gold_metrics.sql
│   ├── inspect_tables.sql
│   ├── maintenance_demo.sql
│   ├── merge_upsert_delete_demo.sql
│   ├── nessie_branching_demo.sql
│   ├── schema_evolution_demo.sql
│   └── time_travel_demo.sql
├── scripts/
│   └── smoke_test.py
├── src/iceberg_portfolio/
│   ├── __init__.py
│   ├── cli.py
│   ├── csv_utils.py
│   ├── config.py
│   ├── logging_utils.py
│   ├── quality.py
│   ├── schemas.py
│   ├── spark_session.py
│   └── jobs/
│       ├── bronze_orders.py
│       ├── quality_checks.py
│       ├── run_pipeline.py
│       ├── silver_orders.py
│       └── gold_orders.py
└── tests/
    ├── test_cli.py
    ├── test_config.py
    ├── test_csv_utils.py
    ├── test_demo_sql.py
    ├── test_jobs.py
    ├── test_logging_utils.py
    ├── test_quality.py
    └── test_runtime_cli.py
```

## Quick start

### 1. Create and activate virtual environment

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
pip install -e .[dev]
```

### 2. Start the local stack

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 3. Run the medallion pipeline

```bash
python -m iceberg_portfolio.jobs.run_pipeline
```

Or run step-by-step:

```bash
python -m iceberg_portfolio.jobs.bronze_orders
python -m iceberg_portfolio.jobs.silver_orders
python -m iceberg_portfolio.jobs.gold_orders
python -m iceberg_portfolio.jobs.quality_checks
```

Pipeline outputs are written as deterministic CSV tables:
- `data/bronze/orders_raw.csv`
- `data/silver/orders_clean.csv`
- `data/gold/daily_revenue.csv`

Each run overwrites target files, so reruns are idempotent for the same input.
Quality checks fail fast on broken schemas, invalid values, or reconciliation mismatches.
Jobs support runtime flags:
- `--config-profile <path>` to load KEY=VALUE settings files
- `--log-level DEBUG|INFO|WARNING|ERROR`

Run with profile explicitly:

```bash
python -m iceberg_portfolio.jobs.run_pipeline --config-profile config/profiles/local.env
```

## What runs where

- Python jobs in `src/iceberg_portfolio/jobs` generate deterministic local CSV outputs for reproducible portfolio execution.
- Spark/Iceberg/Nessie/MinIO services are used for SQL demos and lakehouse architecture walkthroughs under `sql/` and `docs/`.
- This split keeps the core pipeline fast and deterministic while still demonstrating Iceberg platform concepts.

## Development workflow

Run local quality checks with:

```bash
make check
```

Run the full deterministic local pipeline (including data quality):

```bash
make run-pipeline
```

Run the full pipeline with profile file explicitly:

```bash
make run-pipeline-profile
```

Run local smoke validation (Docker services + pipeline run):

```bash
make smoke
```

If `make` is unavailable on your OS, use direct Python commands:

```bash
python -m pytest -q
python scripts/smoke_test.py --config-profile config/profiles/local.env
```

Optional integration CI workflow:
- `.github/workflows/integration-smoke.yml` (manual trigger, plus relevant PR path changes)

Install and run pre-commit hooks:

```bash
pre-commit install
pre-commit run --all-files
```

## Iceberg demos (Phase 2)

- Time travel: `sql/time_travel_demo.sql`
- Schema evolution: `sql/schema_evolution_demo.sql`
- Merge/upsert/delete: `sql/merge_upsert_delete_demo.sql`

Demo details and run order are documented in `docs/phase2_demos.md`.

## Nessie branching demo (Phase 3)

- SQL walkthrough: `sql/nessie_branching_demo.sql`
- Runbook and validation checklist: `docs/nessie_branching_demo.md`

## Maintenance workflows (Phase 3)

- SQL walkthrough: `sql/maintenance_demo.sql`
- Runbook and verification checklist: `docs/maintenance_demo.md`

## Portfolio demo path

- Architecture and design rationale: `docs/architecture.md`
- Interview-friendly runbook: `docs/demo_walkthrough.md`
- AWS service mapping: `docs/aws_mapping.md`
- Community and contribution docs: `CONTRIBUTING.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`

## Current status

The project includes reproducible bronze/silver/gold jobs with schema validation,
profile-driven config, structured logging/CLI flags, CI checks with coverage enforcement,
and Iceberg/Nessie demo workflows.
It is still intentionally small and remains a portfolio base, not a full production lakehouse.

## Sample output

Pre-captured terminal output for quick review without running the stack:
- Pipeline run: `docs/sample_output/pipeline_run.txt`
- Quality checks: `docs/sample_output/quality_checks.txt`
- Test suite: `docs/sample_output/test_suite.txt`
- Data preview (all layers): `docs/sample_output/data_preview.txt`
