from __future__ import annotations

from pathlib import Path


def _read_sql(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").lower()


def test_time_travel_demo_contains_history_queries() -> None:
    sql = _read_sql("sql/time_travel_demo.sql")
    assert "version as of" in sql
    assert "timestamp as of" in sql
    assert ".snapshots" in sql


def test_schema_evolution_demo_contains_evolution_operations() -> None:
    sql = _read_sql("sql/schema_evolution_demo.sql")
    assert "alter table" in sql
    assert "add column" in sql
    assert "alter column amount type decimal(14, 2)" in sql


def test_merge_demo_contains_delete_update_insert_branches() -> None:
    sql = _read_sql("sql/merge_upsert_delete_demo.sql")
    assert "merge into" in sql
    assert "then delete" in sql
    assert "then\n  update set" in sql
    assert "then\n  insert" in sql


def test_nessie_branching_demo_contains_branch_workflow() -> None:
    sql = _read_sql("sql/nessie_branching_demo.sql")
    assert "show references in local" in sql
    assert "create branch if not exists dev in local from main" in sql
    assert "use reference dev in local" in sql
    assert "merge branch dev into main in local" in sql
    assert "drop branch if exists dev in local" in sql
