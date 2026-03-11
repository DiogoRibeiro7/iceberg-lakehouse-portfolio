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

## 3) Show engineering guardrails (2-3 min)

```bash
make check
```

Call out:
- schema contracts in code
- quality checks and failure behavior
- CI + optional integration smoke workflow

## 4) Show Iceberg capabilities (3-4 min)

- Time travel demo: `sql/time_travel_demo.sql`
- Schema evolution demo: `sql/schema_evolution_demo.sql`
- Merge/upsert/delete demo: `sql/merge_upsert_delete_demo.sql`
- Nessie branching demo: `sql/nessie_branching_demo.sql`

## 5) Explain cloud path (1-2 min)

- Use `docs/aws_mapping.md` to map local components to S3, Glue, Athena, and EMR/Glue ETL.
- Mention what stays the same (Iceberg semantics) vs what changes (managed services and ops model).

## Suggested close

- "This repo focuses on correctness and operability first: deterministic outputs, quality gates, and reproducible demos."
- "Next technical increment is maintenance workflows (compaction and snapshot expiration)."
