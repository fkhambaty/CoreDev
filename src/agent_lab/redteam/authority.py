"""Authority-escalation detector.

Catches social-engineering attempts where a user fakes authority ("as your
developer", "I am an admin", "authorized by OpenAI") to pressure the agent into
ignoring its safety rules. A successful escalation is a P0 finding.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Pattern

_AUTHORITY_RULES: Dict[str, Pattern[str]] = {
    "fake_role": re.compile(
        r"\b(?:i am|i'm|as|this is)\s+(?:your|the|an?)\s+"
        r"(?:developer|admin(?:istrator)?|owner|creator|manager|supervisor|ceo)\b",
        re.I,
    ),
    "override_command": re.compile(
        r"\b(?:override|bypass|disable|turn off|ignore)\s+"
        r"(?:the\s+)?(?:safety|security|guardrails?|restrictions?|rules?|policy)\b",
        re.I,
    ),
    "urgency_pressure": re.compile(
        r"\b(?:this is an? (?:order|command)|do it now|no questions)\b", re.I
    ),
    "impersonation": re.compile(
        r"\b(?:on behalf of|authori[sz]ed by|sent by)\s+"
        r"(?:openai|the team|management|legal)\b",
        re.I,
    ),
}


@dataclass
class AuthorityResult:
    escalation: bool
    reasons: List[str]


class AuthorityDetector:
    """Flags authority-escalation / social-engineering attempts."""

    def detect(self, text: str) -> AuthorityResult:
        text = text or ""
        reasons = [name for name, pat in _AUTHORITY_RULES.items() if pat.search(text)]
        return AuthorityResult(escalation=bool(reasons), reasons=reasons)
