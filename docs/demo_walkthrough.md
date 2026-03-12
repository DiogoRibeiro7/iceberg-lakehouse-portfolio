# Demo Walkthrough

Use this as a short portfolio/interview walkthrough (10-15 minutes).

## 1) Context and stack (1-2 min)

- Goal: demonstrate practical Iceberg lakehouse engineering patterns end to end.
- Stack: Spark + Iceberg + MinIO + Nessie, with deterministic bronze/silver/gold outputs.

## 2) Run the pipeline (2-3 min)

```bash
make run-pipeline-profile
```

Show:
- deterministic outputs in `data/bronze`, `data/silver`, `data/gold`
- quality reconciliation result in pipeline output

Sample output: `docs/sample_output/pipeline_run.txt`

## 3) Walk through data flow (1-2 min)

Show how data transforms across layers:
- Raw: source-shape CSV with 5 order records
- Bronze: schema-validated passthrough
- Silver: typed, normalised, analysis-ready
- Gold: daily revenue aggregation (5 rows to 3)

Sample data at each layer: `docs/sample_output/data_preview.txt`

## 4) Show engineering guardrails (2-3 min)

```bash
make check
```

Call out:
- schema contracts in code
- quality checks with cross-layer reconciliation
- CI with coverage enforcement (80% minimum, Python 3.10-3.12 matrix)
- integration smoke workflow with output validation

Sample output: `docs/sample_output/test_suite.txt`

## 5) Show Iceberg capabilities (3-4 min)

- Time travel demo: `sql/time_travel_demo.sql`
- Schema evolution demo: `sql/schema_evolution_demo.sql`
- Merge/upsert/delete demo: `sql/merge_upsert_delete_demo.sql`
- Nessie branching demo: `sql/nessie_branching_demo.sql`
- Maintenance demo: `sql/maintenance_demo.sql`

## 6) Explain cloud path (1-2 min)

- Use `docs/aws_mapping.md` to map local components to S3, Glue, Athena, and EMR/Glue ETL.
- Mention what stays the same (Iceberg semantics) vs what changes (managed services and ops model).

## Suggested close

- "This repo focuses on correctness and operability first: deterministic outputs, quality gates, and reproducible demos."
- "Every demo is backed by CI, coverage enforcement, and idempotent outputs you can verify yourself."
