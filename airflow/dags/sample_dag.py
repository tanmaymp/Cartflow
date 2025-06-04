from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 4),
    'retries': 1,
}

with DAG('simple_dag', default_args=default_args, schedule_interval='@once') as dag:
    start_task = DummyOperator(task_id='start')

    start_task
