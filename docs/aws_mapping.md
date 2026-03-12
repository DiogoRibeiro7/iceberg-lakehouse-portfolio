# AWS Mapping

This repository runs locally with MinIO + Nessie + Spark + Iceberg.  
The table below maps those components and workflows to typical AWS equivalents.

## Component mapping

| Local component | Purpose | AWS equivalent |
|---|---|---|
| MinIO | S3-compatible object storage for table files | Amazon S3 |
| Nessie catalog | Table namespace/version management with branches | AWS Glue Data Catalog (metadata) + branch strategy via isolated environments/repos |
| Spark (tabulario image) | Batch transforms and SQL execution | Amazon EMR, AWS Glue ETL, or EMR Serverless |
| Iceberg tables | Open table format with snapshot semantics | Apache Iceberg on S3, queried via Athena/EMR/Glue |

## Query/processing mapping

| Local workflow | AWS option |
|---|---|
| Spark SQL against Iceberg | EMR Spark SQL or Glue Spark jobs |
| Analyst SQL against gold tables | Amazon Athena (Iceberg table support) |
| CI smoke/integration checks | GitHub Actions + ephemeral AWS test account resources |

## Metadata and governance notes

- Local Nessie branching demo approximates isolated development.  
  In AWS, common patterns include:
  - separate dev/stage/prod catalogs or databases
  - isolated prefixes/buckets per environment
  - promotion workflows through CI/CD and IaC

- Data quality checks in this repo can map to:
  - Glue job validations
  - Athena assertions
  - dedicated frameworks (Great Expectations/Deequ) in EMR/Glue pipelines

## Deployment sketch (AWS)

1. Store bronze/silver/gold data in S3 prefixes.
2. Register Iceberg tables in Glue Data Catalog.
3. Run transforms via Glue jobs or EMR Spark.
4. Query gold tables with Athena.
5. Orchestrate with Step Functions, MWAA, or external orchestrator.
6. Add CI/CD deployment and environment promotion gates.

## Tradeoffs to call out in interviews

- Why Iceberg over plain parquet directories (schema evolution, snapshot/time travel, atomic commits).
- Catalog strategy and environment isolation model.
- Cost/performance implications of Athena vs EMR/Glue for workload shape.
- Operational controls: quality gates, schema contracts, rollback strategy via snapshots.
