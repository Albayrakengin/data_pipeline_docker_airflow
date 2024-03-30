CREATE TABLE IF NOT EXISTS my_table (
    product_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL,
    description TEXT,
    category VARCHAR(255),
    image TEXT,
    rating_rate NUMERIC,
    rating_count INTEGER
);
