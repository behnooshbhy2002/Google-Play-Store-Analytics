-- Example 1
EXPLAIN ANALYZE
SELECT apps.id, apps.app_name, apps.category_id, apps.rating, apps.installs, apps.min_installs, apps.max_installs, apps.price, apps.content_rating, apps.privacy_policy, apps.ad_supported, apps.in_app_purchases, apps.editors_choice 
FROM apps 
WHERE apps.category_id IN (5) AND apps.rating BETWEEN 0.0 AND 5.0 AND apps.price BETWEEN 0.0 AND 1.0 ORDER BY apps.rating ASC


-- Example 2
EXPLAIN ANALYZE 
SELECT 
    apps.id, 
    apps.app_name, 
    apps.category_id, 
    apps.rating, 
    apps.installs, 
    apps.min_installs, 
    apps.max_installs, 
    apps.price, 
    apps.content_rating, 
    apps.privacy_policy, 
    apps.ad_supported, 
    apps.in_app_purchases, 
    apps.editors_choice 
FROM apps 
WHERE apps.category_id IN (5) 
    AND apps.rating < 3.0  
    AND apps.price BETWEEN 0.0 AND 1.0 
ORDER BY apps.rating ASC;



-- Create an index on category_id to speed up category-based lookups and other columns
CREATE INDEX idx_app_category ON apps (category_id);
CREATE INDEX IF NOT EXISTS idx_app_content_rating ON apps (content_rating);
CREATE INDEX IF NOT EXISTS idx_app_rating_range ON apps (rating);
CREATE INDEX IF NOT EXISTS idx_app_price ON apps (price);

-- Create one index from several columns
CREATE INDEX idx_apps_category_rating_price 
ON apps (category_id, rating, price);


DROP INDEX IF EXISTS idx_app_category;
DROP INDEX IF EXISTS idx_app_content_rating;
DROP INDEX IF EXISTS idx_app_rating_range;
DROP INDEX IF EXISTS idx_app_price;
DROP INDEX IF EXISTS idx_apps_category_rating_price;



-- Covering Index
CREATE INDEX idx_app_category ON apps(category_id) 
INCLUDE (app_name, rating, installs, min_installs, max_installs, price, content_rating);
