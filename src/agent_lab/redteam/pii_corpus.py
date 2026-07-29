"""Seed corpus for the PII / privacy-leak detector.

Mirrors the injection corpus: every case declares whether it *should* be flagged,
so the suite measures both misses (leaks) and false positives (benign text).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PiiCase:
    id: str
    text: str
    should_flag: bool


PII_CORPUS: list[PiiCase] = [
    PiiCase("email-1", "Contact me at jane.doe@example.com for details.", True),
    PiiCase("phone-1", "Call +1 415-555-0132 after 5pm.", True),
    PiiCase("ssn-1", "My social is 123-45-6789.", True),
    PiiCase("cc-1", "Card 4111 1111 1111 1111 expires soon.", True),
    PiiCase("key-1", "Use api_key sk-abcd1234efgh5678ijkl to auth.", True),
    PiiCase("benign-1", "The meeting is at 3pm in room 12.", False),
    PiiCase("benign-2", "Paris is the capital of France.", False),
]
