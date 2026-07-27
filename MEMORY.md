# MEMORY.md — persistent project state

> A running log of decisions and progress so any contributor (human or agent)
> can pick up the project without re-reading every file. Newest entries on top.

## Project north star

Build a small, dependency-light **Agent Evaluation & Red-Team Lab**: a
deterministic tool-calling agent plus the harness to score its trajectories
against an objective rubric and stress-test it for security failures
(prompt injection, PII leakage, authority escalation).

## Conventions

- Python ≥ 3.10, standard library only for the core (tests may use `pytest`).
- Every tool validates its own input and raises `ToolError` — no crashes.
- The agent core is deterministic: no network, no LLM, no randomness.
- Each day ships one self-contained, tested increment.

## Log

### Day 1
- Scaffolded package `src/agent_lab` with `tools`, `trajectory`, `agent`.
- Deterministic `ToolCallingAgent` routes queries to one of four safe tools.
- Structured `Trajectory`/`Step` logging, JSON-serialisable.
- Authored evaluation rubric v1 (0–4 scale, P0/P1/P2 findings).
- Added pytest suite (agent + tools) and multi-version CI.
