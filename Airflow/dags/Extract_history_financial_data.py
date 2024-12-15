import sys
import os
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from Tasks.Load_data.load_data_to_staging import load_csv_to_db_using_copy
from datetime import datetime
import pandas as pd

# Import các hàm main_report và main_report_1
from Tasks.extract.HistoricalData.company_financial import main_report
from Tasks.extract.HistoricalData.company_financial_1 import main_report_1

def combine_csv_files(filename):
    """Gộp các file CSV tạm thời thành một file duy nhất."""
    temp_files = [f"/opt/Tasks/extract/HistoricalData/{filename}_{i}.csv" for i in range(2)]
    combined = pd.concat([pd.read_csv(f) for f in temp_files], ignore_index=True)
    combined.to_csv(f"/opt/Tasks/extract/HistoricalData/{filename}.csv", index=False)
    # Xóa các file tạm
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print("Đã xóa thành công")
        except OSError as e:
            print(f"Không thể xóa {temp_file}: {e}")

def combine_all_files():
    combine_csv_files('Total_Balance')
    combine_csv_files('Total_CashFlow')
    combine_csv_files('Total_Income')

default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 0,
}

with DAG(
    'parallel_historycal_financial_reports',
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

    combine_task = PythonOperator(
        task_id="combine_csv_files",
        python_callable=combine_all_files,
    )

    with TaskGroup('Load_to_db') as load_to_postgres_group:
        task_load_balance = PythonOperator(
            task_id = 'load_balance_to_staging',
            python_callable=load_csv_to_db_using_copy,
            op_args=[
                "/opt/Tasks/extract/HistoricalData/Total_Balance.csv",
                "CanDoiKeToan",
                ["Chi_Tieu", "Thoi_Gian", "Gia_Tri", "Ma_SIC"],
            ]
        )
        task_load_cashflow = PythonOperator(
            task_id = 'load_cashflow_to_staging',
            python_callable=load_csv_to_db_using_copy,
            op_args=[
                "/opt/Tasks/extract/HistoricalData/Total_CashFlow.csv",
                "LuuChuyenTienTe",
                ["Chi_Tieu", "Thoi_Gian", "Gia_Tri", "Ma_SIC"],
            ]
        )
        task_load_income = PythonOperator(
            task_id = 'load_income_to_staging',
            python_callable=load_csv_to_db_using_copy,
            op_args=[
                "/opt/Tasks/extract/HistoricalData/Total_Income.csv",
                "KetQuaKinhDoanh",
                ["Chi_Tieu", "Thoi_Gian", "Gia_Tri", "Ma_SIC"],
            ]
        )

    end = EmptyOperator(task_id='end')

    # Định nghĩa thứ tự thực thi
    start >> financial_reports_group >> combine_task >> load_to_postgres_group >> end
