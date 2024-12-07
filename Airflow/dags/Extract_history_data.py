import sys
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# Import các hàm main_report và main_report_1
from Tasks.HistoricalData.company_financial import main_report
from Tasks.HistoricalData.company_financial_1 import main_report_1

default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 0,
}

with DAG(
    'parallel_financial_reports',
    default_args=default_args,
    schedule_interval=None,  # Chạy thủ công
    catchup=False,
) as dag:

    start = EmptyOperator(task_id='start')

    with TaskGroup('financial_reports') as financial_reports_group:
        task_main_report = PythonOperator(
            task_id='run_main_report',
            python_callable=main_report,
        )

        task_main_report_1 = PythonOperator(
            task_id='run_main_report_1',
            python_callable=main_report_1,
        )

    end = EmptyOperator(task_id='end')

    # Định nghĩa thứ tự thực thi
    start >> financial_reports_group >> end
