import pytest

from agent_lab.agent import ToolCallingAgent
from agent_lab.evaluator import evaluate
from agent_lab.store import EvalStore, load_named_queries


@pytest.fixture()
def store():
    db = EvalStore(":memory:")
    yield db
    db.close()


def _seed(store: EvalStore) -> None:
    agent = ToolCallingAgent()
    for query in ["12 + 30", "reverse hi", "write me a poem", "1 / 0"]:
        traj = agent.run(query)
        store.record(query, evaluate(traj))


def test_named_queries_load():
    queries = load_named_queries()
    assert {"verdict_distribution", "findings_by_severity", "weakest_categories"} <= set(queries)


def test_record_and_verdict_distribution(store):
    _seed(store)
    rows = store.run_named("verdict_distribution")
    total = sum(row["n"] for row in rows)
    assert total == 4
    verdicts = {row["verdict"] for row in rows}
    assert "pass" in verdicts


def test_weakest_categories_returns_eight(store):
    _seed(store)
    rows = store.run_named("weakest_categories")
    assert len(rows) == 8
    assert all(0 <= row["avg_score"] <= 4 for row in rows)


def test_unknown_query_raises(store):
    with pytest.raises(KeyError):
        store.run_named("does_not_exist")
