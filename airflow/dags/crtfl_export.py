from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

# default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

EXPORT_PATH = "/opt/airflow/data_exports"
# Postgres connection details from environment
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

# Function to export PostgreSQL table to CSV file
def export_table_to_csv(table_name):
    engine = create_engine(PG_CONNECTION_STRING)
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, engine)
    filename = os.path.join(EXPORT_PATH, f"{table_name}.csv")
    df.to_csv(filename, index=False)
    print(f"Exported {table_name} to {filename}")

# DAG
with DAG(
    dag_id='cartflow_export',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description="Export DBT marts to CSV"
) as dag:

    # Task 1 - Export fact_user_orders.csv
    export_user_orders = PythonOperator(
        task_id="export_fct_user_orders",
        python_callable=export_table_to_csv,
        op_args=["fct_user_orders"]
    )

    # Task 2 - Export fct_user_product_reorders.csv
    export_user_reorders = PythonOperator(
        task_id="export_fct_user_product_reorders",
        python_callable=export_table_to_csv,
        op_args=["fct_user_product_reorders"]
    )

    # Task 3 - Export fct_customer_orders.csv
    export_customer_orders = PythonOperator(
        task_id="export_fct_customer_orders",
        python_callable=export_table_to_csv,
        op_args=["fct_customer_orders"]
    )

    # task dependencies
    export_user_orders >> export_user_reorders >> export_customer_orders
