"""Obfuscation-resistant injection detection.

Attackers hide payloads with zero-width characters, homoglyphs, or base64.
This layer normalises and expands the text before applying the base rules.
"""

from __future__ import annotations

import base64
import re
import unicodedata

from agent_lab.redteam.detector import DetectionResult, InjectionDetector

# Zero-width and BOM characters attackers insert to split keywords.
_ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff"), None)

# A few common Cyrillic/lookalike homoglyphs mapped back to ASCII.
_HOMOGLYPHS = str.maketrans({
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0456": "i",
    "\u0455": "s", "\u0440": "p", "\u0441": "c",
})

_B64_TOKEN = re.compile(r"[A-Za-z0-9+/]{12,}={0,2}")


def normalize(text: str) -> str:
    """NFKC-normalise, strip zero-width chars, and fold common homoglyphs."""
    text = unicodedata.normalize("NFKC", text or "")
    return text.translate(_ZERO_WIDTH).translate(_HOMOGLYPHS)


def expand_base64(text: str) -> str:
    """Append decoded content of any base64-looking tokens so rules can match it."""
    decoded_parts: list[str] = []
    for token in _B64_TOKEN.findall(text or ""):
        try:
            decoded = base64.b64decode(token, validate=True).decode("utf-8", "ignore")
        except (ValueError, UnicodeDecodeError):
            continue
        if decoded and decoded.isprintable():
            decoded_parts.append(decoded)
    if not decoded_parts:
        return text
    return f"{text} {' '.join(decoded_parts)}"


class RobustInjectionDetector(InjectionDetector):
    """InjectionDetector that first de-obfuscates the input."""

    def detect(self, text: str) -> DetectionResult:
        prepared = expand_base64(normalize(text))
        return super().detect(prepared)
