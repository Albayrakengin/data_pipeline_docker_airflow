CREATE TABLE IF NOT EXISTS product_details (
    product_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL,
    description TEXT,
    category VARCHAR(255),
    image TEXT
);