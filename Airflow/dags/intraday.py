import sys
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

from Kafka.app.producer import runproducer
from Kafka.app.processor import runprocessor
from Kafka.app.consumer import runconsumer

default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id="run_kafka_app",
    default_args=default_args,
    schedule_interval= None,
    catchup=False,
) as dag:
    
    # Điểm bắt đầu DAG
    start = EmptyOperator(task_id="start")

    with TaskGroup("Kafka_run") as Kafka_run:
        producer = PythonOperator(
            task_id="producer",
            python_callable=runproducer,
        )
        processor = PythonOperator(
            task_id="processor",
            python_callable=runprocessor,
        )
        consumer = PythonOperator(
            task_id="consumer",
            python_callable=runconsumer,
        )
    end = EmptyOperator(task_id="end")

    start >> Kafka_run >> end