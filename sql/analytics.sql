-- Analytics queries over stored agent evaluations.
-- Named-query format (`-- name: <id>`) so they can be loaded individually,
-- in the spirit of sqlc / dbt analyses. Keep each query self-contained.

-- name: verdict_distribution
-- How many trajectories landed in each verdict bucket.
SELECT verdict,
       COUNT(*)                                   AS n,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM evaluations
GROUP BY verdict
ORDER BY n DESC;

-- name: findings_by_severity
-- Volume of findings by severity — P0/P1 are what block a release.
SELECT f.severity,
       COUNT(*) AS n
FROM findings f
GROUP BY f.severity
ORDER BY CASE f.severity WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 ELSE 2 END;

-- name: weakest_categories
-- Average score per rubric category; lowest = where the agent needs work.
SELECT cs.category,
       ROUND(AVG(cs.score), 2) AS avg_score,
       COUNT(*)                AS n
FROM category_scores cs
GROUP BY cs.category
ORDER BY avg_score ASC;

-- name: failing_queries
-- The exact queries that failed, with their worst finding, for triage.
SELECT e.query,
       e.verdict,
       MIN(CASE f.severity WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 ELSE 2 END) AS worst_rank,
       COUNT(f.id) AS n_findings
FROM evaluations e
LEFT JOIN findings f ON f.evaluation_id = e.id
WHERE e.verdict <> 'pass'
GROUP BY e.id, e.query, e.verdict
ORDER BY worst_rank ASC, n_findings DESC;
