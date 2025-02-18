CREATE MATERIALIZED VIEW avg_rating_per_category AS
SELECT 
    c.category_name,
    ROUND(CAST(AVG(a.rating) AS NUMERIC), 2) AS avg_rating,
    COUNT(a.id) AS total_apps
FROM apps a
JOIN categories c ON a.category_id = c.id
GROUP BY c.category_name
ORDER BY avg_rating DESC;

SELECT * FROM avg_rating_per_category;

SELECT category_name, avg_rating, total_apps
        FROM avg_rating_per_category
-- SELECT * FROM apps;
