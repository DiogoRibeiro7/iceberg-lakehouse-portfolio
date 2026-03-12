-- Flink + Iceberg + Nessie demo SQL
-- Run in Flink SQL Client after configuring Iceberg/Nessie catalog jars.

CREATE CATALOG local WITH (
  'type' = 'iceberg',
  'catalog-type' = 'nessie',
  'uri' = 'http://nessie:19120/api/v1',
  'ref' = 'main',
  'warehouse' = 's3://warehouse/',
  's3.endpoint' = 'http://minio:9000',
  's3.path-style-access' = 'true',
  's3.access-key' = 'admin',
  's3.secret-key' = 'password123'
);

USE CATALOG local;
CREATE DATABASE IF NOT EXISTS bronze;
CREATE DATABASE IF NOT EXISTS gold;

-- Source event stream table.
CREATE TABLE IF NOT EXISTS bronze.orders_events (
  order_id STRING,
  customer_id STRING,
  order_ts TIMESTAMP(3),
  amount DECIMAL(12, 2),
  status STRING,
  WATERMARK FOR order_ts AS order_ts - INTERVAL '5' SECOND
) WITH (
  'connector' = 'datagen',
  'rows-per-second' = '10',
  'fields.order_id.length' = '12',
  'fields.customer_id.length' = '10',
  'fields.amount.min' = '10',
  'fields.amount.max' = '500',
  'fields.status.length' = '6'
);

-- Target Iceberg table with partitioning.
CREATE TABLE IF NOT EXISTS gold.orders_revenue_1m (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  order_count BIGINT,
  revenue DECIMAL(18, 2)
)
PARTITIONED BY (days(window_start));

-- Streaming aggregation into Iceberg.
INSERT INTO gold.orders_revenue_1m
SELECT
  window_start,
  window_end,
  COUNT(*) AS order_count,
  CAST(SUM(amount) AS DECIMAL(18, 2)) AS revenue
FROM TABLE(
  TUMBLE(TABLE bronze.orders_events, DESCRIPTOR(order_ts), INTERVAL '1' MINUTE)
)
GROUP BY window_start, window_end;
