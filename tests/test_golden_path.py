from agent_lab.golden_path import Step, refactor, score

IDEAL = ["lookup", "calculate", "answer"]


def test_perfect_trajectory_scores_full_adherence():
    traj = [Step("lookup"), Step("calculate"), Step("answer")]
    report = score(traj, IDEAL)
    assert report.adherence == 1.0
    assert report.wasted_steps == 0


def test_failed_and_duplicate_steps_are_refactored_out():
    traj = [
        Step("lookup"),
        Step("lookup"),                 # duplicate
        Step("calculate", ok=False),    # failed
        Step("calculate"),
        Step("answer"),
    ]
    cleaned = refactor(traj)
    assert [s.tool for s in cleaned] == ["lookup", "calculate", "answer"]


def test_wasted_steps_are_counted():
    traj = [Step("lookup"), Step("lookup"), Step("answer")]
    report = score(traj, IDEAL)
    assert report.wasted_steps == 1
    assert report.adherence < 1.0
