# CoreDev — Agent Evaluation & Red-Team Lab

A small, dependency-light toolkit for **evaluating and red-teaming tool-calling
agents**. It pairs a deterministic tool-calling agent with the harness needed to
review its behaviour the way a human reviewer would: capture the full
**trajectory**, score it against an **objective rubric**, and stress-test it for
security failures.

The agent core is intentionally deterministic (no LLM, no network, no
randomness) so that every run is reproducible and every trajectory can be
replayed and scored identically. The interesting engineering lives in the
*evaluation and safety* layer, not in the agent's raw intelligence.

## Why this exists

Reviewing agent runs, writing verifiable scoring rubrics, and red-teaming for
vulnerabilities (data exposure, authority escalation, prompt injection) is a
distinct discipline from building the agent itself. This repo is a hands-on
sandbox for that discipline.

## Layout

```
src/agent_lab/
  tools.py        # safe, self-validating tools + registry
  trajectory.py   # structured, JSON-serialisable run logs
  agent.py        # deterministic tool-calling agent
  evaluator.py    # rubric-driven scorer -> scores + P0/P1/P2 findings + verdict
  store.py        # SQLite persistence + named-query analytics
rubrics/
  agent_eval_rubric.md   # 0–4 scoring, P0/P1/P2 findings
sql/
  analytics.sql   # named analytics queries over evaluation results
ts/               # TypeScript CLI: cross-language port of the scorer
tests/            # pytest suite
```

## Quick start

```bash
python -m pip install -r requirements.txt
pytest -q
```

```python
from agent_lab import ToolCallingAgent

agent = ToolCallingAgent()
traj = agent.run("12 + 30")
print(traj.final_answer)   # -> "42"
print(traj.to_json())      # full auditable trajectory
```

## Evaluate & analyse

```python
from agent_lab import ToolCallingAgent
from agent_lab.evaluator import evaluate
from agent_lab.store import EvalStore

agent, store = ToolCallingAgent(), EvalStore(":memory:")
for q in ["12 + 30", "reverse hi", "write me a poem"]:
    store.record(q, evaluate(agent.run(q)))

print(store.run_named("verdict_distribution"))
print(store.run_named("weakest_categories"))
```

## Roadmap

See [`MEMORY.md`](./MEMORY.md) for the running log. Upcoming increments:
red-team suites (prompt injection, PII leak, authority escalation), a
"Golden Path" refactor demo, and a dbt-style transform of evaluation metrics.
