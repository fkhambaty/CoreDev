import sqlite3

from projects.csv_loader.loader import load_csv


def test_load_csv_inserts_rows(tmp_path):
    csv_path = tmp_path / "people.csv"
    csv_path.write_text("name,age\nAda,36\nAlan,41\n", encoding="utf-8")
    db_path = tmp_path / "out.sqlite"

    n = load_csv(csv_path, db_path, "people")
    assert n == 2

    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT name, age FROM people ORDER BY name").fetchall()
    conn.close()
    assert rows == [("Ada", "36"), ("Alan", "41")]


def test_empty_csv_loads_nothing(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("", encoding="utf-8")
    n = load_csv(csv_path, tmp_path / "out.sqlite", "empty")
    assert n == 0
