-- Severity SLA report: how long each finding has been outstanding.
-- SLA policy: P0 <= 1 day, P1 <= 3 days, P2 <= 7 days. Rows marked BREACHED
-- are past their SLA and need attention first.

SELECT
    f.severity,
    f.message,
    e.task,
    CAST(julianday('now') - julianday(e.created_at) AS INT) AS age_days,
    CASE f.severity WHEN 'P0' THEN 1 WHEN 'P1' THEN 3 WHEN 'P2' THEN 7 END AS sla_days,
    CASE
        WHEN CAST(julianday('now') - julianday(e.created_at) AS INT) >
             CASE f.severity WHEN 'P0' THEN 1 WHEN 'P1' THEN 3 WHEN 'P2' THEN 7 END
        THEN 'BREACHED'
        ELSE 'within SLA'
    END AS sla_status
FROM findings f
JOIN evaluations e ON e.id = f.evaluation_id
ORDER BY CASE f.severity WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 ELSE 2 END, age_days DESC;
