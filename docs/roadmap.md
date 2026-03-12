# Roadmap

## Completed

### Phase 1
- Validate the local stack
- Make bronze, silver, and gold jobs runnable
- Improve README

### Phase 2
- Add time travel demo
- Add schema evolution demo
- Add merge/upsert/delete demo

### Phase 3
- Add data quality checks
- Add Nessie branching demo
- Add maintenance workflows (snapshot expiration, compaction, manifest rewriting, orphan removal)

### Phase 4
- Add CI and test coverage
- Add logging, CLI flags, and profile-based config
- Add smoke test workflow for local stack validation
- Add AWS mapping for S3, Glue, Athena, and EMR/Glue ETL
- Add unit tests for CLI, logging, and CSV utilities
- Add coverage enforcement (80% minimum) and Python version matrix to CI
- Add format check and separate CI jobs for lint, typecheck, and test
- Add output validation to smoke test and health-check wait to integration workflow

### Phase 5
- Add sample output artifacts (pipeline run, quality checks, test suite, data preview)
- Update demo walkthrough with data flow section and sample output references

## Next

Roadmap complete. Potential future extensions:
- Record terminal sessions with asciinema for animated demos
- Add Terraform/CDK examples for AWS deployment
- Add streaming ingestion demo with Kafka/Flink
