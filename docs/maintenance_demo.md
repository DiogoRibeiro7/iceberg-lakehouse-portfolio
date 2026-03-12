# Maintenance Demo

This walkthrough demonstrates Iceberg table maintenance operations: snapshot expiration, data file compaction, manifest rewriting, and orphan file removal.

## Script

- `sql/maintenance_demo.sql`

## Workflow

1. Create a table and apply several DML statements to accumulate snapshots.
2. Inspect snapshots, data files, and manifests before maintenance.
3. Expire old snapshots with `expire_snapshots`, keeping the most recent 2.
4. Compact small data files with `rewrite_data_files` using the `binpack` strategy.
5. Rewrite manifests with `rewrite_manifests` to reduce metadata overhead.
6. Remove orphaned files with `remove_orphan_files`.
7. Verify table contents are unchanged after all maintenance operations.

## What to verify

- After snapshot expiration:
  - Only the retained snapshots appear in the `.snapshots` system table.
  - Time travel to expired snapshots is no longer possible.
- After compaction:
  - The `.files` system table shows fewer, larger data files.
- After manifest rewriting:
  - The `.manifests` system table shows consolidated manifest entries.
- After all maintenance:
  - A final `SELECT` confirms data integrity is preserved.

## When to run maintenance

- **Snapshot expiration**: regularly, to reclaim storage from superseded snapshots.
- **Compaction**: after many small writes or streaming ingestion produce numerous small files.
- **Manifest rewriting**: when manifest list growth slows query planning.
- **Orphan file removal**: periodically, to clean up files left by failed or interrupted jobs.

## Notes

- Always run `expire_snapshots` before `remove_orphan_files` so expired data files become orphans eligible for removal.
- The `retain_last` parameter in `expire_snapshots` guarantees a minimum number of snapshots survive regardless of the timestamp cutoff.
- Compaction does not change table contents; it only reorganises the physical layout.
