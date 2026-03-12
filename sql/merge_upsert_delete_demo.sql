-- MERGE INTO demo for upsert and delete workflows with Apache Iceberg.

CREATE NAMESPACE IF NOT EXISTS local.demo;

CREATE TABLE IF NOT EXISTS local.demo.orders_merge_target (
    order_id BIGINT,
    customer_id BIGINT,
    status STRING,
    amount DECIMAL(12, 2),
    currency STRING
) USING iceberg;

INSERT OVERWRITE local.demo.orders_merge_target VALUES
    (100, 3001, 'created', 25.00, 'EUR'),
    (101, 3002, 'created', 79.99, 'EUR'),
    (102, 3003, 'created', 12.50, 'EUR');

CREATE OR REPLACE TEMP VIEW orders_merge_source AS
SELECT * FROM VALUES
    (100, 3001, 'updated', 35.00, 'EUR', 'UPSERT'),
    (101, 3002, 'cancelled', 79.99, 'EUR', 'DELETE'),
    (103, 3004, 'created', 49.90, 'EUR', 'UPSERT')
AS t(order_id, customer_id, status, amount, currency, op);

MERGE INTO local.demo.orders_merge_target AS target
USING orders_merge_source AS source
ON target.order_id = source.order_id
WHEN MATCHED AND source.op = 'DELETE' THEN DELETE
WHEN MATCHED AND source.op = 'UPSERT' THEN
  UPDATE SET
    target.customer_id = source.customer_id,
    target.status = source.status,
    target.amount = source.amount,
    target.currency = source.currency
WHEN NOT MATCHED AND source.op = 'UPSERT' THEN
  INSERT (order_id, customer_id, status, amount, currency)
  VALUES (source.order_id, source.customer_id, source.status, source.amount, source.currency);

SELECT *
FROM local.demo.orders_merge_target
ORDER BY order_id;

SELECT committed_at, snapshot_id, operation
FROM local.demo.orders_merge_target.snapshots
ORDER BY committed_at;
