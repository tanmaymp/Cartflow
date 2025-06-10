from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
from sqlalchemy import create_engine, inspect, text
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Postgres connection details from environment
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

# Function to load CSV files into PostgreSQL

def load_csv_to_postgres(csv_file, table_name, chunksize=500000):
    """
    Load a CSV file into PostgreSQL:
    - Creates the table if it does not exist.
    - If table exists, truncates and appends (preserves views).
    """
    time.sleep(5)
    engine = create_engine(PG_CONNECTION_STRING)
    inspector = inspect(engine)

    table_exists = inspector.has_table(table_name)

    if not table_exists:
        print(f"Table {table_name} does not exist. Creating and loading.")
        chunk_iter = pd.read_csv(csv_file, chunksize=chunksize)
        for i, chunk in enumerate(chunk_iter):
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Chunk {i+1} loaded for {table_name}")
    else:
        print(f"Table {table_name} exists. Truncating and reloading.")
        with engine.begin() as conn:
            conn.execute(text(f'TRUNCATE TABLE {table_name}'))
            # conn.commit()

        chunk_iter = pd.read_csv(csv_file, chunksize=chunksize)
        for i, chunk in enumerate(chunk_iter):
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Chunk {i+1} loaded for {table_name}")


# default arguments
default_args = {
    'owner': 'airflow',
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

# DAG
with DAG(
    dag_id='cartflow_ingest',
    default_args=default_args,
    description='ETL DAG for loading Instacart data into PostgreSQL',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task 1 - Ingest orders.csv
    load_orders_task = PythonOperator(
        task_id='load_orders_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/orders.csv', 'orders'],
    )

    # Task 2 - Ingest order_products_prior.csv
    load_order_products_prior_task = PythonOperator(
        task_id='load_order_products_prior_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/order_products_prior.csv',
                 'order_products_prior'],
        execution_timeout=timedelta(hours=1)
    )

    # Task 3 - Ingest order_products__train.csv
    load_order_products_train_task = PythonOperator(
        task_id='load_order_products_train_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/order_products__train.csv',
                 'order_products_train'],
    )

    # Task 4 - Ingest aisles.csv
    load_aisles_task = PythonOperator(
        task_id='load_aisles_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/aisles.csv', 'aisles'],
    )

    # Task 5 - Ingest departments.csv
    load_departments_task = PythonOperator(
        task_id='load_departments_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/departments.csv', 'departments'],
    )

    # Task 6 - Ingest products.csv
    load_products_task = PythonOperator(
        task_id='load_products_csv',
        python_callable=load_csv_to_postgres,
        op_args=['/opt/airflow/data/raw/products.csv', 'products'],
    )

    # task dependencies
    load_orders_task >> load_aisles_task >> load_departments_task >> load_products_task >> load_order_products_train_task >> load_order_products_prior_task  
