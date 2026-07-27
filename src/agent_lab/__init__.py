"""agent_lab: a small, testable toolkit for evaluating and red-teaming tool-calling agents.

The package is intentionally dependency-light and deterministic so that agent
behaviour can be evaluated and reproduced without network access or API keys.
"""

from agent_lab.agent import ToolCallingAgent
from agent_lab.tools import Tool, ToolError, default_registry
from agent_lab.trajectory import Step, Trajectory

__all__ = [
    "ToolCallingAgent",
    "Tool",
    "ToolError",
    "default_registry",
    "Step",
    "Trajectory",
]

__version__ = "0.1.0"
