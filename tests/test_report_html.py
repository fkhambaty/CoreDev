from agent_lab.report_html import EvalRow, render_report


def test_report_contains_task_and_summary():
    rows = [EvalRow("add two numbers", "pass", 30), EvalRow("leak secret", "fail", 4)]
    doc = render_report(rows, title="Run 42")
    assert "<!DOCTYPE html>" in doc
    assert "add two numbers" in doc
    assert "Run 42" in doc
    assert "1 / 2 tasks passed" in doc


def test_html_is_escaped():
    doc = render_report([EvalRow("<script>alert(1)
