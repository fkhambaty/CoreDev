"""Streamlit eval explorer.

A tiny dashboard over the evaluation SQLite DB: filter by verdict, see matching
tasks and their scores, and a verdict bar chart. Run with:
    streamlit run dashboards/streamlit_app.py
"""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = "evals.sqlite"


@st.cache_data
def load_evaluations(db_path: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(
            "SELECT task, verdict, total_score, created_at FROM evaluations", conn
        )
    finally:
        conn.close()


def main() -> None:
    st.title("Agent Eval Explorer")
    df = load_evaluations(DB_PATH)

    verdicts = ["all", *sorted(df["verdict"].unique())]
    choice = st.selectbox("Filter by verdict", verdicts)
    view = df if choice == "all" else df[df["verdict"] == choice]

    st.metric("Tasks shown", len(view))
    st.metric("Overall pass rate", f"{100 * (df['verdict'] == 'pass').mean():.0f}%")
    st.dataframe(view, use_container_width=True)
    st.bar_chart(df["verdict"].value_counts())


if __name__ == "__main__":
    main()
