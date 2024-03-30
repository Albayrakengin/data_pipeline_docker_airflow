INSERT INTO product_details (product_id, title, price, description, category, image)
SELECT product_id, title, price, description, category, image
FROM my_table
WHERE NOT EXISTS (
  SELECT 1
  FROM product_details
  WHERE product_details.product_id = my_table.product_id
);