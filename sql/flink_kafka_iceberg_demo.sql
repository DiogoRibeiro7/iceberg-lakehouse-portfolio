-- Flink + Kafka + Iceberg + Nessie demo SQL
-- Use this after starting the local stack with the kafka service.

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

CREATE TABLE IF NOT EXISTS bronze.orders_kafka (
  order_id STRING,
  customer_id STRING,
  order_ts TIMESTAMP(3),
  amount DECIMAL(12, 2),
  status STRING,
  WATERMARK FOR order_ts AS order_ts - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'orders-events',
  'properties.bootstrap.servers' = 'kafka:9092',
  'properties.group.id' = 'flink-orders-consumer',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'json.ignore-parse-errors' = 'true'
);

CREATE TABLE IF NOT EXISTS gold.orders_revenue_1m_kafka (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  order_count BIGINT,
  revenue DECIMAL(18, 2)
)
PARTITIONED BY (days(window_start));

INSERT INTO gold.orders_revenue_1m_kafka
SELECT
  window_start,
  window_end,
  COUNT(*) AS order_count,
  CAST(SUM(amount) AS DECIMAL(18, 2)) AS revenue
FROM TABLE(
  TUMBLE(TABLE bronze.orders_kafka, DESCRIPTOR(order_ts), INTERVAL '1' MINUTE)
)
GROUP BY window_start, window_end;
