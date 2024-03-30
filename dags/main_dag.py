import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

sys.path.append('/opt/airflow/python_scripts')

create_product_details_sql = """
CREATE TABLE IF NOT EXISTS product_details (
    product_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL,
    description TEXT,
    category VARCHAR(255),
    image TEXT
);
"""

create_ratings_table_sql = """
CREATE TABLE IF NOT EXISTS ratings_table (
    product_id INT PRIMARY KEY,
    rating_rate NUMERIC,
    rating_count INTEGER
);
"""

insert_ratings_sql = """
INSERT INTO product_details (product_id, title, price, description, category, image)
SELECT product_id, title, price, description, category, image
FROM my_table
WHERE NOT EXISTS (
  SELECT 1
  FROM product_details
  WHERE product_details.product_id = my_table.product_id
);
"""


insert_product_details_sql = """
INSERT INTO ratings_table (product_id, rating_rate, rating_count)
SELECT product_id, rating_rate, rating_count
FROM my_table
WHERE NOT EXISTS (
  SELECT 1
  FROM ratings_table
  WHERE ratings_table.product_id = my_table.product_id
);
"""


default_args = {
    'owner': 'Engin',
    'start_date': datetime(2024, 3, 15),
    'schedule_interval': '@daily',
}

with DAG(dag_id="my_dag", default_args=default_args, catchup=False) as dag:

    transform_api_to_postgres = BashOperator (
        task_id = "api_to_postgres",
        bash_command=f'pwd && python /opt/airflow/python_scripts/api_to_postgres.py'
    ) 
    
    create_product_details_sql = PostgresOperator (
        task_id ="create_product_details",
        postgres_conn_id="postgres_default",
        sql= create_product_details_sql
    )

    create_ratings_table_sql = PostgresOperator (
        task_id ="create_ratings_table",
        postgres_conn_id="postgres_default",
        sql= create_ratings_table_sql
    )

    insert_product_details_sql = PostgresOperator (
        task_id ="insert_product_details",
        postgres_conn_id="postgres_default",
        sql= insert_product_details_sql
    )

    insert_ratings_sql = PostgresOperator (
        task_id ="insert_ratings",
        postgres_conn_id="postgres_default",
        sql= insert_ratings_sql
    )

    transform_api_to_postgres >> [create_ratings_table_sql, create_product_details_sql]
    create_product_details_sql >> insert_product_details_sql
    create_ratings_table_sql >> insert_ratings_sql