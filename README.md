# Iceberg Lakehouse Portfolio

Portfolio repository showcasing practical Apache Iceberg lakehouse engineering skills with Spark, MinIO, and Nessie.

## What this repo demonstrates

- Local lakehouse stack with **Spark + Iceberg + MinIO + Nessie**
- Simple **bronze / silver / gold** medallion pipeline
- Sample analyst-friendly SQL queries
- Project structure ready for:
  - time travel demos
  - schema evolution demos
  - merge/upsert workflows
  - data quality checks
  - Nessie branching workflows

## Architecture

- **MinIO**: local S3-compatible object storage
- **Nessie**: catalog and branching layer
- **Spark**: processing engine
- **Iceberg**: table format

## Repository layout

```text
.
├── data/
│   └── raw/orders.csv
├── docker/
│   └── docker-compose.yml
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── nessie_branching_demo.md
│   ├── phase2_demos.md
│   └── roadmap.md
├── sql/
│   ├── gold_metrics.sql
│   ├── inspect_tables.sql
│   ├── merge_upsert_delete_demo.sql
│   ├── nessie_branching_demo.sql
│   ├── schema_evolution_demo.sql
│   └── time_travel_demo.sql
├── src/iceberg_portfolio/
│   ├── __init__.py
│   ├── csv_utils.py
│   ├── config.py
│   ├── schemas.py
│   ├── spark_session.py
│   └── jobs/
│       ├── bronze_orders.py
│       ├── silver_orders.py
│       └── gold_orders.py
└── tests/
    ├── test_config.py
    └── test_jobs.py
```

## Quick start

### 1. Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### 2. Start the local stack

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 3. Run the medallion pipeline

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

## Development workflow

Run local quality checks with:

```bash
make check
```

Run the full deterministic local pipeline (including data quality):

```bash
make run-pipeline
```

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

## Current status

The project now includes reproducible bronze/silver/gold jobs with schema validation and CI checks.
It is still intentionally small and remains a portfolio base, not a full production lakehouse.

## Next recommended steps

1. Add maintenance workflows (compaction/snapshot expiration examples).
2. Add an AWS mapping document for S3 + Glue + Athena.
