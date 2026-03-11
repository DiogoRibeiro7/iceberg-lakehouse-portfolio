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
│   └── roadmap.md
├── sql/
│   ├── gold_metrics.sql
│   └── inspect_tables.sql
├── src/iceberg_portfolio/
│   ├── __init__.py
│   ├── config.py
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
```

## Development workflow

Run local quality checks with:

```bash
make check
```

Install and run pre-commit hooks:

```bash
pre-commit install
pre-commit run --all-files
```

## Current status

This scaffold is intentionally small. It is a portfolio base, not yet a full production lakehouse.

## Next recommended steps

1. Add a deterministic time travel demo.
2. Add schema evolution examples.
3. Add `MERGE INTO` workflows.
4. Add Nessie branch-based isolated development.
5. Add an AWS mapping document for S3 + Glue + Athena.
