"""Static HTML eval-report generator.

Turns a list of evaluation results into a single self-contained HTML file — no
web server, no JS framework. Handy for sharing a run summary or attaching to a PR.
User-supplied text is HTML-escaped so a task name can never inject markup.
"""

from __future__ import annotations

import html
from dataclasses import dataclass
from typing import List


@dataclass
class EvalRow:
    task: str
    verdict: str
    score: int
    max_score: int = 32


_VERDICT_COLOR = {"pass": "#12a150", "revise": "#b7791f", "fail": "#d64545"}


def _row_html(row: EvalRow) -> str:
    color = _VERDICT_COLOR.get(row.verdict.lower(), "#55607a")
    pct = round(100 * row.score / row.max_score) if row.max_score else 0
    return (
        f"<tr><td>{html.escape(row.task)}</td>"
        f'<td style="color:{color};font-weight:700">{html.escape(row.verdict)}</td>'
        f"<td>{row.score}/{row.max_score} ({pct}%)</td></tr>"
    )


def render_report(rows: List[EvalRow], title: str = "Eval Report") -> str:
    """Return a complete, standalone HTML document as a string."""
    body = "\n".join(_row_html(r) for r in rows)
    passed = sum(1 for r in rows if r.verdict.lower() == "pass")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:40px;color:#1c2333}}
table{{border-collapse:collapse;width:100%}}
th,td{{padding:8px 12px;border-bottom:1px solid #e7eaf0;text-align:left}}
th{{background:#f2f5fa}}
</style></head>
<body>
<h1>{html.escape(title)}</h1>
<p>{passed} / {len(rows)} tasks passed.</p>
<table><thead><tr><th>Task</th><th>Verdict</th><th>Score</th></tr></thead>
<tbody>
{body}
</tbody></table>
</body></html>
"""
