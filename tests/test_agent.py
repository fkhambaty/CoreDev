from agent_lab.agent import ToolCallingAgent


def test_agent_routes_arithmetic_to_calculator():
    agent = ToolCallingAgent()
    trajectory = agent.run("12 + 30")
    assert trajectory.final_answer == "42"
    assert trajectory.steps[0].tool == "calculator"
    assert trajectory.had_error is False


def test_agent_routes_reverse():
    agent = ToolCallingAgent()
    trajectory = agent.run("reverse hello")
    assert trajectory.final_answer == "olleh"
    assert trajectory.steps[0].tool == "reverse"


def test_agent_routes_lookup():
    agent = ToolCallingAgent()
    trajectory = agent.run("what is the capital of france?")
    assert trajectory.final_answer == "Paris"


def test_agent_declines_unsupported_query():
    agent = ToolCallingAgent()
    trajectory = agent.run("write me a poem about the sea")
    assert trajectory.had_error is True
    assert trajectory.steps[0].tool is None


def test_trajectory_serialises_to_json():
    agent = ToolCallingAgent()
    trajectory = agent.run("3 * 3")
    payload = trajectory.to_json()
    assert '"final_answer": "9"' in payload
    assert '"tool": "calculator"' in payload
