-- Rank categories worst-first using RANK() so ties share a position.
-- Handy for "show me the top 3 weakest areas to focus on".

WITH cat AS (
    SELECT
        category,
        AVG(score) AS avg_score,
        COUNT(*)   AS samples
    FROM category_scores
    GROUP BY category
)
SELECT
    category,
    ROUND(avg_score, 2)                   AS avg_score,
    samples,
    RANK() OVER (ORDER BY avg_score ASC)  AS weakness_rank
FROM cat
ORDER BY weakness_rank;
