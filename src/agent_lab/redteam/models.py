"""Data model for a single red-team attack case."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AttackCase:
    """One adversarial probe.

    Attributes:
        id: Stable short identifier (e.g. "io-1").
        name: Human-readable label.
        payload: The raw input we feed to the detector/agent.
        category: Threat class (instruction_override, exfiltration, ...).
        should_be_blocked: Expected outcome — True for attacks, False for benign.
    """

    id: str
    name: str
    payload: str
    category: str
    should_be_blocked: bool = True
