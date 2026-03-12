# Flink + Iceberg Streaming Demo

This demo showcases Flink SQL writing streaming aggregates into Iceberg tables
registered in the Nessie catalog.

## Goal

- Ingest generated order events in Flink
- Compute 1-minute tumbling window revenue metrics
- Persist results into partitioned Iceberg table in the `gold` namespace

## Prerequisites

- Docker stack running from `docker/docker-compose.yml`
- Flink SQL client with Iceberg + Nessie runtime dependencies available

## Demo SQL

Use: `sql/flink_iceberg_streaming_demo.sql`

The script includes:
- `CREATE CATALOG ...` using Nessie + MinIO
- Source stream table via `datagen`
- Partitioned target Iceberg table
- Streaming `INSERT INTO ... SELECT` window aggregation

## Run sequence

1. Start stack:
   - `docker compose -f docker/docker-compose.yml up -d`
2. Open Flink SQL client connected to JobManager.
3. Execute the SQL script sections in order.
4. Verify output table:
   - `SELECT * FROM gold.orders_revenue_1m LIMIT 20;`

## What to explain in interviews

- Why Iceberg is used as a sink for streaming aggregates
- Watermarking and event-time windows in Flink
- Exactly-once guarantees with checkpoints (in a production deployment)
- Partition design and downstream query pruning
