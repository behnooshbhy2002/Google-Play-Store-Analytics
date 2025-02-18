
COPY categories(category_name, id) 
FROM 'D:\University-Master\Term-1\Adv Data Base\PR01\Codes\ADB-PR01\categories.csv' 
DELIMITER ',' 
CSV HEADER;
SELECT * FROM categories LIMIT 5;

COPY developers(developer_id, website, email,id)
FROM 'D:\University-Master\Term-1\Adv Data Base\PR01\Codes\ADB-PR01\developers.csv'
DELIMITER ','
CSV HEADER;
SELECT * FROM developers LIMIT 5;

COPY content_ratings(content_rating, id) 
FROM 'D:\University-Master\Term-1\Adv Data Base\PR01\Codes\ADB-PR01\content_rating.csv' 
DELIMITER ',' 
CSV HEADER;
SELECT * FROM content_ratings LIMIT 5;

COPY apps(app_name, app_id, category_id, rating, rating_count, installs, min_installs, 
          max_installs, is_free, price, currency, size_mb, min_android, developer_id, 
          released, last_updated, content_rating, privacy_policy, ad_supported, 
          in_app_purchases, editors_choice) 
FROM 'D:\University-Master\Term-1\Adv Data Base\PR01\Codes\ADB-PR01\apps_with_content_rating_id.csv'
DELIMITER ','
CSV HEADER;
SELECT * FROM apps LIMIT 5;
