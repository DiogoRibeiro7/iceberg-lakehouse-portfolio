-- Maintenance demo for Apache Iceberg (Spark SQL + Nessie catalog).
-- Shows snapshot expiration, data compaction, manifest rewriting,
-- and orphan file removal.
-- Run statements in order.

CREATE NAMESPACE IF NOT EXISTS local.demo;

-- 1) Create a table and generate multiple snapshots to maintain.
CREATE TABLE IF NOT EXISTS local.demo.orders_maintenance (
    order_id BIGINT,
    customer_id BIGINT,
    order_timestamp TIMESTAMP,
    status STRING,
    amount DECIMAL(12, 2),
    currency STRING
) USING iceberg;

INSERT OVERWRITE local.demo.orders_maintenance VALUES
    (1, 1001, TIMESTAMP '2026-01-01 10:00:00', 'created', 25.00, 'EUR'),
    (2, 1002, TIMESTAMP '2026-01-01 11:00:00', 'created', 50.00, 'EUR');

UPDATE local.demo.orders_maintenance
SET status = 'cancelled'
WHERE order_id = 2;

INSERT INTO local.demo.orders_maintenance VALUES
    (3, 1003, TIMESTAMP '2026-01-02 09:30:00', 'created', 75.00, 'EUR');

UPDATE local.demo.orders_maintenance
SET amount = 30.00
WHERE order_id = 1;

-- 2) Inspect snapshots before maintenance.
SELECT committed_at, snapshot_id, operation, summary
FROM local.demo.orders_maintenance.snapshots
ORDER BY committed_at;

-- 3) Inspect data files before compaction.
SELECT file_path, file_format, record_count, file_size_in_bytes
FROM local.demo.orders_maintenance.files;

-- 4) Inspect manifests before rewriting.
SELECT path, length, partition_spec_id, added_data_files_count
FROM local.demo.orders_maintenance.manifests;

-- 5) Expire old snapshots, keeping only the most recent 2.
-- Replace <expiration_timestamp> with a timestamp between the 3rd and 4th snapshot.
CALL local.system.expire_snapshots(
    table => 'local.demo.orders_maintenance',
    older_than => TIMESTAMP '<expiration_timestamp>',
    retain_last => 2
);

-- 6) Verify snapshots after expiration.
SELECT committed_at, snapshot_id, operation
FROM local.demo.orders_maintenance.snapshots
ORDER BY committed_at;

-- 7) Compact small data files into fewer, larger files.
CALL local.system.rewrite_data_files(
    table => 'local.demo.orders_maintenance',
    strategy => 'binpack'
);

-- 8) Inspect data files after compaction.
SELECT file_path, file_format, record_count, file_size_in_bytes
FROM local.demo.orders_maintenance.files;

-- 9) Rewrite manifests to reduce metadata overhead.
CALL local.system.rewrite_manifests('local.demo.orders_maintenance');

-- 10) Inspect manifests after rewriting.
SELECT path, length, partition_spec_id, added_data_files_count
FROM local.demo.orders_maintenance.manifests;

-- 11) Remove orphaned files not referenced by any snapshot.
-- Replace <orphan_timestamp> with the current timestamp.
CALL local.system.remove_orphan_files(
    table => 'local.demo.orders_maintenance',
    older_than => TIMESTAMP '<orphan_timestamp>'
);

-- 12) Final state: confirm table contents are unchanged after maintenance.
SELECT order_id, customer_id, status, amount, currency
FROM local.demo.orders_maintenance
ORDER BY order_id;
