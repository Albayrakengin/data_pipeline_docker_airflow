import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


sys.path.append('/opt/airflow/python_scripts')

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
    