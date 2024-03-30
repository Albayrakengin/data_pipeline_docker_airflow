INSERT INTO my_table (product_id, title, price, description, category, image, rating_rate, rating_count)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (product_id) DO NOTHING;
