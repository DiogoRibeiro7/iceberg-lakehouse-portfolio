# Flink + Kafka + Iceberg Demo

This demo uses Kafka as a real streaming source for Flink SQL and writes
windowed aggregates into Iceberg tables in Nessie.

## Goal

- Consume order events from Kafka topic `orders-events`
- Aggregate revenue in 1-minute windows
- Persist results into `gold.orders_revenue_1m_kafka`

## Prerequisites

- Docker stack running from `docker/docker-compose.yml`
- Flink SQL client from this repo image (runtime jars preloaded)

## Run sequence

1. Start services:
   - `docker compose -f docker/docker-compose.yml up -d`
2. Create topic:
   - `docker compose -f docker/docker-compose.yml exec kafka rpk topic create orders-events`
3. Publish sample events:
   - `docker compose -f docker/docker-compose.yml exec kafka rpk topic produce orders-events`
   - Paste JSON lines and finish with Ctrl+D:

```json
{"order_id":"o-1001","customer_id":"c-1","order_ts":"2026-03-12T16:00:10","amount":75.50,"status":"PAID"}
{"order_id":"o-1002","customer_id":"c-2","order_ts":"2026-03-12T16:00:40","amount":22.00,"status":"PAID"}
{"order_id":"o-1003","customer_id":"c-1","order_ts":"2026-03-12T16:01:05","amount":100.00,"status":"PAID"}
```

4. Launch SQL client:
   - `python scripts/run_flink_sql_client.py`
5. Execute SQL in:
   - `sql/flink_kafka_iceberg_demo.sql`
6. Verify output:
   - `SELECT * FROM gold.orders_revenue_1m_kafka LIMIT 20;`

## Checkpoint and state configuration

Default SQL client config applies:
- `execution.checkpointing.interval: 30 s`
- `execution.checkpointing.mode: EXACTLY_ONCE`
- `parallelism.default: 1`

For demo tuning, run these before `INSERT INTO`:

```sql
SET 'execution.checkpointing.interval' = '10 s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'restart-strategy.type' = 'fixed-delay';
SET 'restart-strategy.fixed-delay.attempts' = '3';
SET 'restart-strategy.fixed-delay.delay' = '10 s';
```

## Failure-recovery proof steps

1. Keep producing events to Kafka topic `orders-events`.
2. Confirm Flink job is running:
   - `curl http://localhost:8081/jobs/overview`
3. Simulate worker failure:
   - `docker compose -f docker/docker-compose.yml stop flink-taskmanager`
4. Resume worker:
   - `docker compose -f docker/docker-compose.yml start flink-taskmanager`
5. Publish a few new events to Kafka.
6. Verify aggregate sink receives post-recovery data:
   - `SELECT * FROM gold.orders_revenue_1m_kafka LIMIT 20;`

Expected outcome:
- Flink job restarts and continues consuming from Kafka.
- Iceberg table keeps updating after taskmanager recovery.

## Notes

- Kafka bootstrap server inside Docker network is `kafka:9092`.
- SQL client image includes Kafka SQL connector jar for Flink 1.19.
