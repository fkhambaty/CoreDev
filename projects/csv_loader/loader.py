"""CSV -> SQLite loader CLI.

Reads a CSV file and loads it into a SQLite table, inferring column names from
the header. Standard-library only. Safe against SQL injection: identifiers are
quoted and every value goes through a parameterised insert.

Usage:
    python -m projects.csv_loader.loader data.csv --db out.sqlite --table people
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from typing import List, Optional


def _quote_ident(name: str) -> str:
    """Safely quote a SQL identifier (column/table name)."""
    return '"' + name.replace('"', '""') + '"'


def load_csv(csv_path: Path, db_path: Path, table: str) -> int:
    """Load a CSV into `table`, returning the number of rows inserted."""
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header: List[str] = next(reader, [])
        if not header:
            return 0
        rows = list(reader)

    cols = ", ".join(_quote_ident(h) for h in header)
    placeholders = ", ".join("?" for _ in header)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {_quote_ident(table)} ({cols})")
        conn.executemany(
            f"INSERT INTO {_quote_ident(table)} ({cols}) VALUES ({placeholders})",
            rows,
        )
        conn.commit()
    finally:
        conn.close()
    return len(rows)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Load a CSV file into SQLite.")
    parser.add_argument("csv", type=Path, help="path to the CSV file")
    parser.add_argument("--db", type=Path, default=Path("out.sqlite"), help="SQLite DB path")
    parser.add_argument("--table", default="data", help="destination table name")
    args = parser.parse_args(argv)
    n = load_csv(args.csv, args.db, args.table)
    print(f"Loaded {n} rows into {args.table}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
