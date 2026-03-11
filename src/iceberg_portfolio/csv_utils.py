from __future__ import annotations

import csv
from pathlib import Path


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header: {path}")
        rows: list[dict[str, str]] = []
        for row in reader:
            clean_row: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                clean_row[key] = "" if value is None else value
            rows.append(clean_row)
    return list(reader.fieldnames), rows


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validate_columns(actual: list[str], expected: list[str], *, label: str) -> None:
    if actual != expected:
        raise ValueError(f"{label} schema mismatch. Expected columns {expected}, got {actual}.")
