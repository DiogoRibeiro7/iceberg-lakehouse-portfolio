FROM flink:1.19.2-scala_2.12-java11

ARG ICEBERG_VERSION=1.6.1
ARG FLINK_MINOR=1.19
ARG FLINK_KAFKA_CONNECTOR_VERSION=3.2.0-1.19
ARG MAVEN_REPO=https://repo1.maven.org/maven2

RUN set -eux; \
    curl -fSL "${MAVEN_REPO}/org/apache/iceberg/iceberg-flink-runtime-${FLINK_MINOR}/${ICEBERG_VERSION}/iceberg-flink-runtime-${FLINK_MINOR}-${ICEBERG_VERSION}.jar" \
      -o "/opt/flink/lib/iceberg-flink-runtime-${FLINK_MINOR}-${ICEBERG_VERSION}.jar"; \
    curl -fSL "${MAVEN_REPO}/org/apache/iceberg/iceberg-nessie/${ICEBERG_VERSION}/iceberg-nessie-${ICEBERG_VERSION}.jar" \
      -o "/opt/flink/lib/iceberg-nessie-${ICEBERG_VERSION}.jar"; \
    curl -fSL "${MAVEN_REPO}/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar" \
      -o "/opt/flink/lib/iceberg-aws-bundle-${ICEBERG_VERSION}.jar"; \
    curl -fSL "${MAVEN_REPO}/org/apache/flink/flink-sql-connector-kafka/${FLINK_KAFKA_CONNECTOR_VERSION}/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar" \
      -o "/opt/flink/lib/flink-sql-connector-kafka-${FLINK_KAFKA_CONNECTOR_VERSION}.jar"

COPY docker/flink/sql-client/conf/sql-client-defaults.yaml /opt/flink/conf/sql-client-defaults.yaml

ENV ENABLE_BUILT_IN_PLUGINS=flink-s3-fs-hadoop-1.19.2.jar
