# Architecture

This repository uses a local lakehouse stack:

- Spark for processing
- Apache Iceberg for table format
- MinIO as S3-compatible object storage
- Nessie as the catalog and data branching layer

This setup is useful for learning and portfolio demonstration because it makes Iceberg workflows visible without needing AWS.
