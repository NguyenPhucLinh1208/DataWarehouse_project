import sys
import os
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from datetime import datetime
import pandas as pd

from Tasks.extract.HistoricalData.Historical_price_stock import historical_price
from Tasks.Load_data.load_data_to_staging import load_csv_to_db_using_copy

with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
    MaCks = [line.strip() for line in f]

def split_list(lst, n):
    """Chia một danh sách thành các danh sách nhỏ hơn, mỗi danh sách có n phần tử."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


list_of_lists = list(split_list(MaCks, 26))

def process_group(stock_codes, group_id):
    result = historical_price(stock_codes)
    output_path = f"/opt/Tasks/extract/HistoricalData/Temp_HisPrice_Group_{group_id}.csv"
    result.to_csv(output_path, index=False)

# Hàm gộp các file CSV tạm thời
def combine_csv_files():
    """Gộp các file CSV tạm thời thành một file duy nhất."""
    temp_files = [f"/opt/Tasks/extract/HistoricalData/Temp_HisPrice_Group_{i}.csv" for i in range(len(list_of_lists))]
    combined_df = pd.concat([pd.read_csv(f) for f in temp_files], ignore_index=True)
    combined_df.to_csv("/opt/Tasks/extract/HistoricalData/TotalHisPrice.csv", index=False)
    # Xóa các file tạm
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print("Đã xóa thành công")
        except OSError as e:
            print(f"Không thể xóa {temp_file}: {e}")

default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 0,
}

with DAG(
    dag_id="parallel_historical_price_with_group",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Điểm bắt đầu DAG
    start = EmptyOperator(task_id="start")

    # Nhóm các task xử lý nhóm mã chứng khoán
    with TaskGroup("process_groups") as process_groups:
        for i, group in enumerate(list_of_lists):
            PythonOperator(
                task_id=f"process_group_{i}",
                python_callable=process_group,
                op_args=[group, i],
            )

    # Task gộp kết quả
    combine_task = PythonOperator(
        task_id="combine_csv_files",
        python_callable=combine_csv_files,
    )

    load_to_db = PythonOperator(
        task_id = "load_history_price_to_db",
        python_callable=load_csv_to_db_using_copy,
        op_args=[
            "/opt/Tasks/extract/HistoricalData/TotalHisPrice.csv",
             "lichsugia",
              ["Thoi_Gian", "Gia_Opening", "Gia_High", "Gia_Low", "Gia_Closing", "Khoi_Luong", "Ma_SIC", "Status"],
        ]
    )

    
    # Điểm kết thúc DAG
    end = EmptyOperator(task_id="end")

    # Thiết lập thứ tự thực thi
    start >> process_groups >> combine_task >> load_to_db >> end