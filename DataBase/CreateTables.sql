-- Create the categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL
);

-- DROP TABLE apps CASCADE;

-- Create the developers table
CREATE TABLE developers (
    id SERIAL PRIMARY KEY,
    developer_id VARCHAR(255) ,
    website TEXT,
    email TEXT
);

-- Create the content_ratings table
CREATE TABLE content_ratings (
    id SERIAL PRIMARY KEY,
    content_rating VARCHAR(50) UNIQUE NOT NULL
);

-- Create the apps table
CREATE TABLE apps (
    id SERIAL PRIMARY KEY,
    app_name TEXT NOT NULL,
    app_id VARCHAR(255) UNIQUE NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    rating FLOAT,
    rating_count INT,
    installs BIGINT,
    min_installs BIGINT,
    max_installs BIGINT,
    is_free BOOLEAN,
    price FLOAT,
    currency VARCHAR(10),
    size_mb FLOAT,
    min_android VARCHAR(50),
    developer_id INT REFERENCES developers(id) ON DELETE SET NULL,
    released DATE,
    last_updated DATE,
    content_rating INT REFERENCES content_ratings(id) ON DELETE SET NULL,
    privacy_policy TEXT,
    ad_supported BOOLEAN,
    in_app_purchases BOOLEAN,
    editors_choice BOOLEAN
);

