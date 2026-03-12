# Roadmap

## Completed

### Phase 1
- Validate the local stack
- Make bronze, silver, and gold jobs runnable
- Improve README

### Phase 2
- Add time travel demo
- Add schema evolution demo
- Add merge/upsert/delete demo

### Phase 3
- Add data quality checks
- Add Nessie branching demo
- Add maintenance workflows (snapshot expiration, compaction, manifest rewriting, orphan removal)

### Phase 4
- Add CI and test coverage
- Add logging, CLI flags, and profile-based config
- Add smoke test workflow for local stack validation
- Add AWS mapping for S3, Glue, Athena, and EMR/Glue ETL
- Add unit tests for CLI, logging, and CSV utilities
- Add coverage enforcement (80% minimum) and Python version matrix to CI
- Add format check and separate CI jobs for lint, typecheck, and test
- Add output validation to smoke test and health-check wait to integration workflow

### Phase 5
- Add sample output artifacts (pipeline run, quality checks, test suite, data preview)
- Update demo walkthrough with data flow section and sample output references

## Next

### Phase 6 — Partitioning and performance
- Add partitioned table demo (partition by day, hidden partitioning)
- Add partition evolution demo (migrate partition scheme without rewriting data)
- Add sort order demo (write-time clustering for scan efficiency)
- Document query planning benefits with partition pruning examples

### Phase 7 — Streaming ingestion
- Add Kafka + Spark Structured Streaming ingestion into bronze Iceberg tables
- Demonstrate near-real-time append and compaction cycle
- Add streaming-specific quality checks (late data, out-of-order events)
- Extend docker-compose with Kafka and Schema Registry services

### Phase 8 — Orchestration
- Add Airflow (MWAA-compatible) DAG for bronze/silver/gold pipeline
- Add retry, alerting, and SLA monitoring patterns
- Add dependency-aware scheduling between layers
- Document orchestrator comparison (Step Functions vs MWAA vs Dagster)

### Phase 9 — AWS deployment
- Add Terraform module for S3 + Glue Catalog + Athena workgroup
- Add Glue ETL job wrappers for bronze/silver/gold transforms
- Add example IAM policies and least-privilege roles
- Add environment promotion workflow (dev/staging/prod)
- Add cost estimation notes for Athena vs EMR vs Glue

### Phase 10 — Observability and governance
- Add data lineage tracking (OpenLineage integration)
- Add metrics collection (row counts, freshness, schema drift alerts)
- Add access control demo (column-level and row-level filtering)
- Add audit logging for table mutations
- Document monitoring mapping (local logs to CloudWatch/Datadog)

## Ideas (unprioritised)
- Record terminal sessions with asciinema for animated demos
- Add multi-table joins and slowly changing dimensions (SCD Type 2) demo
- Add cross-catalog federation example (Nessie + Glue side by side)
- Add dbt-iceberg integration for transform layer
- Add Great Expectations or Soda integration for data quality
- Benchmark compaction strategies (binpack vs sort) with larger datasets
