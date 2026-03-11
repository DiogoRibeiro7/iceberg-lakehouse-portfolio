-- Schema evolution demo for Apache Iceberg.
-- Run this script after creating local.demo.orders_history, or standalone with setup below.

CREATE NAMESPACE IF NOT EXISTS local.demo;

CREATE TABLE IF NOT EXISTS local.demo.orders_evolution (
    order_id BIGINT,
    customer_id BIGINT,
    order_timestamp TIMESTAMP,
    status STRING,
    amount DECIMAL(12, 2),
    currency STRING
) USING iceberg;

INSERT OVERWRITE local.demo.orders_evolution VALUES
    (10, 2001, TIMESTAMP '2026-02-01 09:00:00', 'created', 80.00, 'EUR'),
    (11, 2002, TIMESTAMP '2026-02-01 11:30:00', 'created', 15.49, 'EUR');

-- Additive change: add nullable column.
ALTER TABLE local.demo.orders_evolution
ADD COLUMN sales_channel STRING;

-- Type widening: amount can now hold larger values.
ALTER TABLE local.demo.orders_evolution
ALTER COLUMN amount TYPE DECIMAL(14, 2);

-- Populate newly added column for existing rows.
UPDATE local.demo.orders_evolution
SET sales_channel = 'web'
WHERE sales_channel IS NULL;

INSERT INTO local.demo.orders_evolution VALUES
    (12, 2003, TIMESTAMP '2026-02-02 12:05:00', 'created', 1500.99, 'EUR', 'mobile');

SELECT order_id, amount, sales_channel
FROM local.demo.orders_evolution
ORDER BY order_id;

SELECT committed_at, snapshot_id, operation
FROM local.demo.orders_evolution.snapshots
ORDER BY committed_at;
