"""Tool definitions and a small registry for the tool-calling agent.

Each tool validates its own input and raises ``ToolError`` on bad input so the
agent can record a clean failure in the trajectory instead of crashing. Keeping
validation inside the tool boundary is what makes later red-teaming (e.g. path
traversal, oversized input) tractable and auditable.
"""

from __future__ import annotations

import math
import operator
from dataclasses import dataclass
from typing import Callable, Dict

# Maximum characters we accept for any single tool input. Guards against
# denial-of-service style inputs during red-team runs.
MAX_INPUT_CHARS = 2_000


class ToolError(Exception):
    """Raised when a tool receives invalid input or cannot complete safely."""


@dataclass(frozen=True)
class Tool:
    """A single capability the agent can call.

    Attributes:
        name: Stable identifier used by the agent to select the tool.
        description: Human-readable summary used in rubrics and docs.
        run: Callable that takes a single string argument and returns a string.
    """

    name: str
    description: str
    run: Callable[[str], str]

    def __call__(self, argument: str) -> str:
        if not isinstance(argument, str):
            raise ToolError(f"{self.name}: argument must be a string")
        if len(argument) > MAX_INPUT_CHARS:
            raise ToolError(
                f"{self.name}: input exceeds {MAX_INPUT_CHARS} chars"
            )
        return self.run(argument)


_ALLOWED_OPERATORS: Dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def _calculator(argument: str) -> str:
    """Evaluate a simple two-operand arithmetic expression, e.g. ``"3 * 4"``.

    Deliberately does NOT use ``eval`` — arbitrary expression evaluation is a
    classic injection vector. We parse exactly one binary operation instead.
    """
    tokens = argument.split()
    if len(tokens) != 3:
        raise ToolError("calculator: expected '<number> <op> <number>'")
    left_raw, op, right_raw = tokens
    if op not in _ALLOWED_OPERATORS:
        raise ToolError(f"calculator: unsupported operator '{op}'")
    try:
        left, right = float(left_raw), float(right_raw)
    except ValueError as exc:
        raise ToolError("calculator: operands must be numbers") from exc
    if op == "/" and right == 0:
        raise ToolError("calculator: division by zero")
    result = _ALLOWED_OPERATORS[op](left, right)
    # Present integers without a trailing ".0" for readability.
    if math.isclose(result, round(result)):
        return str(int(round(result)))
    return str(result)


def _word_count(argument: str) -> str:
    return str(len(argument.split()))


def _reverse(argument: str) -> str:
    return argument[::-1]


# A tiny mock knowledge base so the "lookup" tool is deterministic and offline.
_KNOWLEDGE_BASE: Dict[str, str] = {
    "capital of france": "Paris",
    "speed of light": "299,792,458 m/s",
    "python creator": "Guido van Rossum",
}


def _lookup(argument: str) -> str:
    key = argument.strip().lower()
    if key not in _KNOWLEDGE_BASE:
        raise ToolError(f"lookup: no entry for '{argument}'")
    return _KNOWLEDGE_BASE[key]


def default_registry() -> Dict[str, Tool]:
    """Return a fresh registry of the built-in tools keyed by name."""
    tools = [
        Tool("calculator", "Evaluate '<number> <op> <number>' arithmetic.", _calculator),
        Tool("word_count", "Count whitespace-separated words in the input.", _word_count),
        Tool("reverse", "Reverse the characters of the input string.", _reverse),
        Tool("lookup", "Look up a fact in a small offline knowledge base.", _lookup),
    ]
    return {tool.name: tool for tool in tools}
