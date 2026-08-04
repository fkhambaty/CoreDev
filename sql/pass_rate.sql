-- Pass-rate over time using window functions.
-- Shows the daily pass rate plus a 3-day moving average, so trends are visible
-- even when daily volume is small, and a running total of evaluations.

WITH daily AS (
    SELECT
        DATE(created_at)                                   AS day,
        COUNT(*)                                           AS total,
        SUM(CASE WHEN verdict = 'pass' THEN 1 ELSE 0 END)  AS passed
    FROM evaluations
    GROUP BY DATE(created_at)
)
SELECT
    day,
    total,
    passed,
    ROUND(100.0 * passed / total, 1) AS pass_rate_pct,
    ROUND(
        AVG(100.0 * passed / total) OVER (
            ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 1
    ) AS pass_rate_3day_avg,
    SUM(total) OVER (ORDER BY day) AS cumulative_evals
FROM daily
ORDER BY day;
