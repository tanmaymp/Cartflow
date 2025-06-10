from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='cartflow_master',
    default_args=default_args,
    description='Master DAG to orchestrate ingestion → dbt → export',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    trigger_ingestion = TriggerDagRunOperator(
        task_id='trigger_cartlfow_ingest',
        trigger_dag_id='cartflow_ingest',
        wait_for_completion=True,
        poke_interval=60,
        reset_dag_run=True,
    )

    trigger_transformation = TriggerDagRunOperator(
        task_id='trigger_cartlfow_transform',
        trigger_dag_id='cartflow_transform',
        wait_for_completion=True,
        poke_interval=60,
        reset_dag_run=True,
    )

    trigger_export = TriggerDagRunOperator(
        task_id='trigger_cartlfow_export',
        trigger_dag_id='cartflow_export',
        wait_for_completion=True,
        poke_interval=60,
        reset_dag_run=True,
    )

    trigger_ingestion >> trigger_transformation >> trigger_export
