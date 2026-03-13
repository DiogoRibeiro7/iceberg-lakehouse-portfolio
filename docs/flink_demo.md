# Flink + Iceberg Streaming Demo

This demo showcases Flink SQL writing streaming aggregates into Iceberg tables
registered in the Nessie catalog.

## Goal

- Ingest generated order events in Flink
- Compute 1-minute tumbling window revenue metrics
- Persist results into partitioned Iceberg table in the `gold` namespace

## Prerequisites

- Docker stack running from `docker/docker-compose.yml`
- Flink SQL client image in this repo (preloads Iceberg/Nessie runtime jars)

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
2. Start Flink SQL client:
   - `docker compose -f docker/docker-compose.yml run --rm flink-sql-client`
   - or shortcut: `python scripts/run_flink_sql_client.py`
3. Execute the SQL script sections from `sql/flink_iceberg_streaming_demo.sql` in order.
4. Verify output table:
   - `SELECT * FROM gold.orders_revenue_1m LIMIT 20;`
   - quick validator:
     - `python scripts/validate_flink_sink_rows.py --table gold.orders_revenue_1m`

## Checkpoint and state configuration

Default SQL client config (`docker/flink/sql-client/conf/sql-client-defaults.yaml`):
- `execution.checkpointing.interval: 30 s`
- `execution.checkpointing.mode: EXACTLY_ONCE`
- `parallelism.default: 1`

Optional runtime overrides in SQL client:

```sql
SET 'execution.checkpointing.interval' = '10 s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'restart-strategy.type' = 'fixed-delay';
SET 'restart-strategy.fixed-delay.attempts' = '3';
SET 'restart-strategy.fixed-delay.delay' = '10 s';
```

## Failure-recovery proof steps

1. Start the continuous `INSERT INTO` job from `sql/flink_iceberg_streaming_demo.sql`.
2. Confirm a running job:
   - `curl http://localhost:8081/jobs/overview`
3. Simulate a worker failure:
   - `docker compose -f docker/docker-compose.yml stop flink-taskmanager`
4. Wait 20-30 seconds, then recover worker:
   - `docker compose -f docker/docker-compose.yml start flink-taskmanager`
5. Re-check running jobs:
   - `curl http://localhost:8081/jobs/overview`
6. Validate sink table still receives results:
   - `SELECT * FROM gold.orders_revenue_1m LIMIT 20;`

Expected outcome:
- Job transitions through restart and returns to `RUNNING`.
- New rows continue to appear in the Iceberg sink table after recovery.

## Runtime jars bundled in SQL client image

The SQL client image preloads:
- `iceberg-flink-runtime-1.19-1.6.1.jar`
- `iceberg-nessie-1.6.1.jar`
- `iceberg-aws-bundle-1.6.1.jar`

S3 plugin is enabled via:
- `ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-1.19.2.jar`

Also included for real event sources:
- `flink-sql-connector-kafka-3.2.0-1.19.jar`

## Kafka-based variant

For a real source (Kafka instead of `datagen`), use:
- SQL: `sql/flink_kafka_iceberg_demo.sql`
- Runbook: `docs/flink_kafka_demo.md`

## What to explain in interviews

- Why Iceberg is used as a sink for streaming aggregates
- Watermarking and event-time windows in Flink
- Exactly-once guarantees with checkpoints (in a production deployment)
- Partition design and downstream query pruning
