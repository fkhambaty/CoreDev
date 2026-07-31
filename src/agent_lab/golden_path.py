"""Golden Path analysis for agent trajectories.

A "Golden Path" is the ideal, minimal, reliable sequence of steps for a task.
Reviewing a real (often messy) trajectory and refactoring it toward the Golden
Path is core to the agent-builder role. This module scores how far a trajectory
drifts from the Golden Path and produces a cleaned-up version.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Step:
    """One step an agent took."""

    tool: str
    ok: bool = True
    note: str = ""


@dataclass
class GoldenPathReport:
    adherence: float          # 0.0 - 1.0: fraction of the ideal tools reached successfully
    ideal: List[str]          # the golden tool sequence
    actual: List[str]         # what the agent actually did
    wasted_steps: int         # redundant / failed steps that add no value


def _dedupe_preserving_order(tools: List[str]) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for tool in tools:
        if tool not in seen:
            seen.add(tool)
            out.append(tool)
    return out


def refactor(trajectory: List[Step]) -> List[Step]:
    """Drop failed and duplicate steps, keeping only what advances the task."""
    cleaned: List[Step] = []
    seen: set[str] = set()
    for step in trajectory:
        if not step.ok:
            continue                      # a failed step never belongs on the Golden Path
        if step.tool in seen:
            continue                      # redundant repeat of an already-successful tool
        seen.add(step.tool)
        cleaned.append(step)
    return cleaned


def score(trajectory: List[Step], ideal: List[str]) -> GoldenPathReport:
    """Compare an actual trajectory against the ideal tool sequence."""
    actual_tools = [s.tool for s in trajectory]
    successful = _dedupe_preserving_order([s.tool for s in trajectory if s.ok])
    matched = sum(1 for tool in ideal if tool in successful)
    adherence = matched / len(ideal) if ideal else 1.0
    wasted = len(actual_tools) - len(refactor(trajectory))
    return GoldenPathReport(
        adherence=round(adherence, 3),
        ideal=ideal,
        actual=actual_tools,
        wasted_steps=wasted,
    )
