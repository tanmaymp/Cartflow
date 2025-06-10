from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

# DAG
with DAG(
    dag_id='cartflow_transform',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run DBT transformations for staging and marts',
) as dag:

    # Task 1 - dbt_run
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dbt/cartflow_dbt && dbt run',
    )

    # Task 2 - dbt_test
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dbt/cartflow_dbt && dbt test',
    )

    # task dependencies
    dbt_run >> dbt_test
