"""A small, deterministic tool-calling agent.

The agent uses simple intent routing (no LLM, no network) so its behaviour is
fully reproducible and unit-testable. The point of this lab is the *evaluation
and red-teaming harness* around agents, not the agent's raw intelligence — a
deterministic core lets every trajectory be replayed and scored identically.
"""

from __future__ import annotations

import re
from typing import Dict, Optional

from agent_lab.tools import Tool, ToolError, default_registry
from agent_lab.trajectory import Step, Trajectory

_CALC_PATTERN = re.compile(r"^\s*-?\d+(\.\d+)?\s*[+\-*/]\s*-?\d+(\.\d+)?\s*$")


class ToolCallingAgent:
    """Routes a natural-language query to exactly one built-in tool."""

    def __init__(self, tools: Optional[Dict[str, Tool]] = None) -> None:
        self.tools: Dict[str, Tool] = tools if tools is not None else default_registry()

    def _select_tool(self, query: str) -> tuple[Optional[str], str]:
        """Return the chosen tool name and the argument to pass to it.

        Returns ``(None, "")`` when no tool matches, so the caller can record a
        graceful "no tool" step rather than guessing.
        """
        normalized = query.strip()
        lowered = normalized.lower()

        if _CALC_PATTERN.match(normalized):
            return "calculator", normalized
        if lowered.startswith("reverse "):
            return "reverse", normalized[len("reverse "):]
        if lowered.startswith("count words in ") or lowered.startswith("word count "):
            argument = normalized.split(" in ", 1)[-1] if " in " in lowered else normalized
            return "word_count", argument
        if lowered.startswith("lookup ") or lowered.startswith("what is the "):
            argument = re.sub(r"^(lookup|what is the)\s+", "", normalized, flags=re.IGNORECASE)
            return "lookup", argument.rstrip("?")
        return None, ""

    def run(self, query: str) -> Trajectory:
        """Execute the query and return a complete trajectory."""
        trajectory = Trajectory(query=query)
        tool_name, argument = self._select_tool(query)

        if tool_name is None:
            trajectory.add_step(
                Step(
                    thought="No matching tool for this query.",
                    tool=None,
                    tool_input=None,
                    observation="declined: unsupported request",
                    ok=False,
                )
            )
            trajectory.final_answer = "I don't have a tool that can handle that request."
            return trajectory

        tool = self.tools[tool_name]
        try:
            observation = tool(argument)
            trajectory.add_step(
                Step(
                    thought=f"Query matches the '{tool_name}' tool.",
                    tool=tool_name,
                    tool_input=argument,
                    observation=observation,
                    ok=True,
                )
            )
            trajectory.final_answer = observation
        except ToolError as exc:
            trajectory.add_step(
                Step(
                    thought=f"Selected '{tool_name}' but input was rejected.",
                    tool=tool_name,
                    tool_input=argument,
                    observation=f"error: {exc}",
                    ok=False,
                )
            )
            trajectory.final_answer = f"The '{tool_name}' tool could not process that input."

        return trajectory
