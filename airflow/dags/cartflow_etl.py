from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine
import os
import time

# Define the Postgres connection details from environment or Airflow variables
PG_CONNECTION_STRING = os.getenv(
    "PG_CONNECTION_STRING", "postgresql://cartflow:cartflow@postgres:5432/cartflow")

# Function to load CSV files into PostgreSQL


def load_csv_to_postgres(csv_file, table_name, chunksize=500000):
    """
    Load a CSV file into a PostgreSQL table.
    :param csv_file: The path to the CSV file
    :param table_name: The name of the PostgreSQL table
    """
    # Read CSV file
    # df = pd.read_csv(csv_file)

    # Create connection to PostgreSQL
    time.sleep(5)
    engine = create_engine(PG_CONNECTION_STRING)

    chunk_iter = pd.read_csv(csv_file, chunksize=chunksize)
    for i, chunk in enumerate(chunk_iter):
        mode = 'replace' if i == 0 else 'append'
        chunk.to_sql(table_name, engine, if_exists=mode, index=False)
        print(f"Chunk {i+1} loaded for {table_name}")


# Define the default arguments
default_args = {
    'owner': 'airflow',
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

# Create the DAG
with DAG(
    'instacart_etl_dag',
    default_args=default_args,
    description='ETL DAG for loading Instacart data into PostgreSQL',
    schedule_interval=None,  # Set this to None for manual execution or a cron schedule
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task 1: Load CSV data into Postgres
    load_orders_task = PythonOperator(
        task_id='load_orders_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/orders.csv', 'orders'],
    )

    load_order_products_prior_task = PythonOperator(
        task_id='load_order_products_prior_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/order_products_prior.csv',
                 'order_products_prior'],
        execution_timeout=timedelta(hours=1)
    )

    load_order_products_train_task = PythonOperator(
        task_id='load_order_products_train_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/order_products__train.csv',
                 'order_products_train'],
    )

    load_aisles_task = PythonOperator(
        task_id='load_aisles_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/aisles.csv', 'aisles'],
    )

    load_departments_task = PythonOperator(
        task_id='load_departments_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/departments.csv', 'departments'],
    )

    load_products_task = PythonOperator(
        task_id='load_products_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/products.csv', 'products'],
    )

    # Define task dependencies
    load_orders_task >> load_aisles_task >> load_departments_task >> load_products_task >> load_order_products_train_task >> load_order_products_prior_task  

    # This ensures all CSV loading tasks run before any DBT transformations
