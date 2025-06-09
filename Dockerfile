FROM apache/airflow:2.7.2-python3.10

COPY ./airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
