-- Time travel demo for Apache Iceberg (Spark SQL + Nessie catalog).
-- Run this script in order.

CREATE NAMESPACE IF NOT EXISTS local.demo;

CREATE TABLE IF NOT EXISTS local.demo.orders_history (
    order_id BIGINT,
    customer_id BIGINT,
    order_timestamp TIMESTAMP,
    status STRING,
    amount DECIMAL(12, 2),
    currency STRING
) USING iceberg;

INSERT OVERWRITE local.demo.orders_history VALUES
    (1, 1001, TIMESTAMP '2026-01-01 10:15:00', 'created', 49.99, 'EUR'),
    (2, 1002, TIMESTAMP '2026-01-01 10:45:00', 'created', 19.50, 'EUR'),
    (3, 1001, TIMESTAMP '2026-01-02 09:10:00', 'cancelled', 12.00, 'EUR');

-- Snapshot A: baseline contents.
SELECT committed_at, snapshot_id, operation
FROM local.demo.orders_history.snapshots
ORDER BY committed_at;

-- Create Snapshot B with an update.
UPDATE local.demo.orders_history
SET status = 'refunded'
WHERE order_id = 3;

SELECT committed_at, snapshot_id, operation
FROM local.demo.orders_history.snapshots
ORDER BY committed_at;

-- Replace <snapshot_id_from_baseline> with Snapshot A id from the query above.
SELECT order_id, status, amount
FROM local.demo.orders_history VERSION AS OF <snapshot_id_from_baseline>
ORDER BY order_id;

-- Replace <timestamp_before_update> with a timestamp between Snapshot A and B.
SELECT order_id, status, amount
FROM local.demo.orders_history TIMESTAMP AS OF '<timestamp_before_update>'
ORDER BY order_id;

-- Current view (latest snapshot).
SELECT order_id, status, amount
FROM local.demo.orders_history
ORDER BY order_id;
