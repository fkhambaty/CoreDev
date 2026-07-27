import pytest

from agent_lab.tools import MAX_INPUT_CHARS, ToolError, default_registry


@pytest.fixture()
def tools():
    return default_registry()


def test_calculator_basic_arithmetic(tools):
    assert tools["calculator"]("3 * 4") == "12"
    assert tools["calculator"]("10 / 4") == "2.5"
    assert tools["calculator"]("7 - 9") == "-2"


def test_calculator_rejects_division_by_zero(tools):
    with pytest.raises(ToolError):
        tools["calculator"]("1 / 0")


def test_calculator_rejects_bad_operator(tools):
    with pytest.raises(ToolError):
        tools["calculator"]("2 ** 8")


def test_calculator_rejects_non_numeric(tools):
    with pytest.raises(ToolError):
        tools["calculator"]("two + three")


def test_word_count(tools):
    assert tools["word_count"]("the quick brown fox") == "4"
    assert tools["word_count"]("") == "0"


def test_reverse(tools):
    assert tools["reverse"]("abc") == "cba"


def test_lookup_hit_and_miss(tools):
    assert tools["lookup"]("Capital of France") == "Paris"
    with pytest.raises(ToolError):
        tools["lookup"]("meaning of life")


def test_oversized_input_is_rejected(tools):
    with pytest.raises(ToolError):
        tools["word_count"]("x " * (MAX_INPUT_CHARS))
