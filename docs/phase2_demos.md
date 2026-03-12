# Phase 2 Demos

This document summarizes the three core Iceberg demos now included in this repository.

## Time travel

- Script: `sql/time_travel_demo.sql`
- Shows:
  - snapshot inspection through `<table>.snapshots`
  - historical reads with `VERSION AS OF <snapshot_id>`
  - historical reads with `TIMESTAMP AS OF '<timestamp>'`

## Schema evolution

- Script: `sql/schema_evolution_demo.sql`
- Shows:
  - `ALTER TABLE ... ADD COLUMN`
  - `ALTER TABLE ... ALTER COLUMN ... TYPE` (widening)
  - backfill/update behavior after evolution

## Merge / upsert / delete

- Script: `sql/merge_upsert_delete_demo.sql`
- Shows:
  - source-change staging in a temp view
  - `MERGE INTO` with `DELETE`, `UPDATE`, and `INSERT` branches
  - post-merge table validation and snapshot inspection

## Suggested run order

1. `sql/time_travel_demo.sql`
2. `sql/schema_evolution_demo.sql`
3. `sql/merge_upsert_delete_demo.sql`
