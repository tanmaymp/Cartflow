from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

with DAG(
    dag_id='dbt_transform_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run DBT transformations for staging and marts',
) as dag:

    # Run dbt build (includes run + test)
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt/cartflow_dbt && dbt run',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt/cartflow_dbt && dbt test',
    )

    dbt_run >> dbt_test
