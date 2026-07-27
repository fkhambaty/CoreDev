"""SQLite persistence + analytics for evaluation results.

Stores each evaluated trajectory (verdict, per-category scores, findings) in a
normalised schema so results can be aggregated with plain SQL. Named analytics
queries live in ``sql/analytics.sql`` and are loaded by name.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Dict, List

from agent_lab.evaluator import EvalReport

_SCHEMA = """
CREATE TABLE IF NOT EXISTS evaluations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    query       TEXT    NOT NULL,
    verdict     TEXT    NOT NULL,
    total       INTEGER NOT NULL,
    max_total   INTEGER NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS category_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    category      TEXT    NOT NULL,
    score         INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    severity      TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    note          TEXT    NOT NULL
);
"""

_QUERY_FILE = Path(__file__).resolve().parents[2] / "sql" / "analytics.sql"
_NAME_MARKER = re.compile(r"^--\s*name:\s*(\w+)\s*$", re.MULTILINE)


def load_named_queries(path: Path = _QUERY_FILE) -> Dict[str, str]:
    """Parse ``-- name: <id>`` blocks from a .sql file into a dict."""
    text = path.read_text(encoding="utf-8")
    queries: Dict[str, str] = {}
    matches = list(_NAME_MARKER.finditer(text))
    for index, match in enumerate(matches):
        name = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        queries[name] = text[start:end].strip()
    return queries


class EvalStore:
    """A thin SQLite wrapper for recording and analysing evaluations."""

    def __init__(self, database: str = ":memory:") -> None:
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(_SCHEMA)
        self._queries = load_named_queries()

    def record(self, query: str, report: EvalReport) -> int:
        """Persist one evaluation and return its row id."""
        cursor = self.connection.execute(
            "INSERT INTO evaluations (query, verdict, total, max_total) VALUES (?, ?, ?, ?)",
            (query, report.verdict, report.total, report.max_total),
        )
        evaluation_id = int(cursor.lastrowid)
        self.connection.executemany(
            "INSERT INTO category_scores (evaluation_id, category, score) VALUES (?, ?, ?)",
            [(evaluation_id, category, score) for category, score in report.scores.items()],
        )
        self.connection.executemany(
            "INSERT INTO findings (evaluation_id, severity, category, note) VALUES (?, ?, ?, ?)",
            [(evaluation_id, f.severity, f.category, f.note) for f in report.findings],
        )
        self.connection.commit()
        return evaluation_id

    def run_named(self, name: str) -> List[dict]:
        """Execute a named analytics query and return rows as dicts."""
        if name not in self._queries:
            raise KeyError(f"unknown query '{name}'")
        rows = self.connection.execute(self._queries[name]).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.connection.close()
