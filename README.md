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
rubrics/
  agent_eval_rubric.md   # 0–4 scoring, P0/P1/P2 findings
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

## Roadmap

See [`MEMORY.md`](./MEMORY.md) for the running log. Upcoming increments:
rubric-driven trajectory evaluator, red-team suites (prompt injection, PII leak,
authority escalation), a SQL analytics layer over evaluation results, and a
second-language CLI runner.
