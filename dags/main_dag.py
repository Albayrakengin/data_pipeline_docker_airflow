import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

sys.path.append('/opt/airflow/python_scripts')


default_args = {
    'owner': 'Engin',
    'start_date': datetime(2024, 3, 15),
    'schedule_interval': '@daily',
}

with DAG(dag_id="my_dag",template_searchpath='/opt/airflow/sql_queries/' , default_args=default_args, catchup=False) as dag:

    transform_api_to_postgres = BashOperator (
        task_id = "api_to_postgres",
        bash_command=f'pwd && python /opt/airflow/python_scripts/api_to_postgres.py'
    ) 
    
    create_product_details_sql = PostgresOperator (
        task_id ="create_product_details",
        postgres_conn_id="postgres_default",
        sql= 'create_product_details.sql'
    )

    create_ratings_table_sql = PostgresOperator (
        task_id ="create_ratings_table",
        postgres_conn_id="postgres_default",
        sql= 'create_ratings_table.sql'
    )

    insert_product_details_sql = PostgresOperator (
        task_id ="insert_product_details",
        postgres_conn_id="postgres_default",
        sql= 'insert_product_details.sql'
    )

    insert_ratings_sql = PostgresOperator (
        task_id ="insert_ratings",
        postgres_conn_id="postgres_default",
        sql= 'insert_ratings.sql'
    )

    transform_api_to_postgres >> [create_ratings_table_sql, create_product_details_sql]
    create_product_details_sql >> insert_product_details_sql
    create_ratings_table_sql >> insert_ratings_sql