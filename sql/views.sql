-- Analytics views over the evaluation store.
-- Assumes the Day 6 schema:
--   evaluations(id, task, verdict, total_score, created_at)
--   category_scores(evaluation_id, category, score)
--   findings(evaluation_id, severity, message)

-- 1. Verdict distribution with running percentage (window function).
CREATE VIEW IF NOT EXISTS v_verdict_distribution AS
SELECT
    verdict,
    COUNT(*)                                            AS n,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)  AS pct
FROM evaluations
GROUP BY verdict
ORDER BY n DESC;

-- 2. Weakest categories (lowest average score first).
CREATE VIEW IF NOT EXISTS v_weakest_categories AS
SELECT
    category,
    ROUND(AVG(score), 2) AS avg_score,
    COUNT(*)             AS samples
FROM category_scores
GROUP BY category
ORDER BY avg_score ASC;

-- 3. Findings by severity, ordered P0 -> P1 -> P2 with a CASE sort key.
CREATE VIEW IF NOT EXISTS v_findings_by_severity AS
SELECT
    severity,
    COUNT(*) AS n
FROM findings
GROUP BY severity
ORDER BY CASE severity
    WHEN 'P0' THEN 0
    WHEN 'P1' THEN 1
    WHEN 'P2' THEN 2
    ELSE 3
END;
