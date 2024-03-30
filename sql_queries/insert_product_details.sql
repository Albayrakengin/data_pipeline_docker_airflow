INSERT INTO ratings_table (product_id, rating_rate, rating_count)
SELECT product_id, rating_rate, rating_count
FROM my_table
WHERE NOT EXISTS (
  SELECT 1
  FROM ratings_table
  WHERE ratings_table.product_id = my_table.product_id
);