"""Rule-based prompt-injection detector.

Deterministic regex rules, one per threat class, so results are reproducible and
each block reason is explainable (important for dense technical feedback).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List

_RULES: Dict[str, re.Pattern[str]] = {
    "instruction_override": re.compile(
        r"ignore\s+(all\s+|the\s+)?previous|disregard\s+(all\s+|your\s+)?instructions", re.I
    ),
    "system_prompt_leak": re.compile(
        r"(reveal|show|print|leak|dump)\s+(?:\w+\s+){0,3}(?:system\s+)?(prompt|instructions)", re.I
    ),
    "exfiltration": re.compile(
        r"(api[_-]?key|password|secret|token)\s*[:=]|send\s+.*(key|secret|token|password).*\bto\b", re.I
    ),
    "tool_abuse": re.compile(r"\beval\s*\(|__import__|os\.system|subprocess", re.I),
    "path_traversal": re.compile(r"\.\./|/etc/passwd", re.I),
}


@dataclass
class DetectionResult:
    blocked: bool
    reasons: List[str]


class InjectionDetector:
    """Flags a text as an injection attempt and explains why."""

    def detect(self, text: str) -> DetectionResult:
        reasons = [name for name, pattern in _RULES.items() if pattern.search(text or "")]
        return DetectionResult(blocked=bool(reasons), reasons=reasons)

    def evaluate_corpus(self, corpus: Iterable) -> dict:
        """Run the detector over a corpus and score against expected outcomes."""
        results: Dict[str, bool] = {}
        for case in corpus:
            got = self.detect(case.payload).blocked
            results[case.id] = got == case.should_be_blocked
        passed = sum(1 for ok in results.values() if ok)
        return {"passed": passed, "total": len(results), "results": results}
