from __future__ import annotations

from pathlib import Path

import pytest

from iceberg_portfolio.csv_utils import read_csv_rows, validate_columns, write_csv_rows


def test_write_and_read_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    fieldnames = ["id", "name"]
    rows = [{"id": "1", "name": "alice"}, {"id": "2", "name": "bob"}]
    write_csv_rows(path, fieldnames, rows)

    actual_fields, actual_rows = read_csv_rows(path)
    assert actual_fields == fieldnames
    assert actual_rows == rows


def test_write_creates_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "dir" / "file.csv"
    write_csv_rows(path, ["a"], [{"a": "1"}])
    assert path.exists()


def test_read_csv_empty_file_raises(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="no header"):
        read_csv_rows(path)


def test_read_csv_header_only(tmp_path: Path) -> None:
    path = tmp_path / "header.csv"
    path.write_text("x,y\n", encoding="utf-8")
    fields, rows = read_csv_rows(path)
    assert fields == ["x", "y"]
    assert rows == []


def test_read_csv_none_values_become_empty_strings(tmp_path: Path) -> None:
    path = tmp_path / "nulls.csv"
    path.write_text("a,b\n1,\n", encoding="utf-8")
    _, rows = read_csv_rows(path)
    assert rows[0]["b"] == ""


def test_validate_columns_passes_on_match() -> None:
    validate_columns(["a", "b"], ["a", "b"], label="test")


def test_validate_columns_raises_on_mismatch() -> None:
    with pytest.raises(ValueError, match="schema mismatch"):
        validate_columns(["a", "c"], ["a", "b"], label="test")
