"""Structured trajectory logging for agent runs.

A "trajectory" is the ordered record of what an agent did: which tool it chose,
what input it passed, and what came back. This is the raw material an Agent
Builder reviews and scores, so it must be complete, ordered, and serialisable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class Step:
    """A single decision-and-action taken by the agent."""

    thought: str
    tool: Optional[str]
    tool_input: Optional[str]
    observation: str
    ok: bool


@dataclass
class Trajectory:
    """The full ordered record of a single agent run."""

    query: str
    steps: List[Step] = field(default_factory=list)
    final_answer: Optional[str] = None

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    @property
    def had_error(self) -> bool:
        return any(not step.ok for step in self.steps)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
