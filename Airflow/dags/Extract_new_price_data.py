import sys
import os
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import pandas as pd

from Tasks.extract.NewData.price_stock_new import new_price
from Tasks.Load_data.load_data_to_staging import load_csv_to_db_using_copy
from Tasks.transform_and_load_data.transform_and_load import fact_Price_History_transform_load

with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
    MaCks = [line.strip() for line in f]

def split_list(lst, n):
    """Chia một danh sách thành các danh sách nhỏ hơn, mỗi danh sách có n phần tử."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

list_of_lists = list(split_list(MaCks, 26))

def process_group(stock_codes, group_id):
    result = new_price(stock_codes, group_id)
    output_path = f"/opt/Tasks/extract/NewData/Temp_Price_Group_{group_id}.csv"
    result.to_csv(output_path, index=False)

# Hàm gộp các file CSV tạm thời
def combine_csv_files():
    """Gộp các file CSV tạm thời thành một file duy nhất."""
    temp_files = [f"/opt/Tasks/extract/NewData/Temp_Price_Group_{i}.csv" for i in range(len(list_of_lists))]
    output_file = "/opt/Tasks/extract/NewData/TotalPrice.csv"
    
    # Mở file đích và ghi dữ liệu
    with open(output_file, 'w') as outfile:
        for i, fname in enumerate(temp_files):
            with open(fname) as infile:
                # Ghi tiêu đề chỉ từ file đầu tiên
                if i == 0:
                    outfile.write(infile.read())
                else:
                    # Bỏ qua tiêu đề ở các file sau
                    next(infile)
                    outfile.write(infile.read())
    
    # Xóa các file tạm
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            print("Đã xóa thành công", temp_file)
        except OSError as e:
            print(f"Không thể xóa {temp_file}: {e}")

    # Gộp các file stock_block tạm thời thành một file duy nhất
    stock_block_files = [f"/opt/Tasks/extract/NewData/stock_blocks_{i}.txt" for i in range(len(list_of_lists))]
    with open("/opt/Tasks/extract/NewData/stock_blocks.txt", 'w') as outfile:
        for fname in stock_block_files:
            with open(fname) as infile:
                outfile.write(infile.read())
            try:
                os.remove(fname)
                print("Đã xóa thành công", fname)
            except OSError as e:
                print(f"Không thể xóa {fname}: {e}")


default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id="parallel_new_price_with_group",
    default_args=default_args,
    schedule_interval= '45 19 * * 1-5', # tự động chạy lúc 19h45 tối, từ thứ 2 đến thứ 6 hàng tuần
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
        task_id = "load_price_to_db",
        python_callable=load_csv_to_db_using_copy,
        op_args=[
            "/opt/Tasks/extract/NewData/TotalPrice.csv",
             "lichsugia",
              ["Thoi_Gian", "Gia_Opening", "Gia_High", "Gia_Low", "Gia_Closing", "Khoi_Luong", "Ma_SIC", "Status"],
        ]
    )

    load_to_dwh = PythonOperator(
        task_id="Load_to_fact_price",
        python_callable=fact_Price_History_transform_load
    )

    
    # Điểm kết thúc DAG
    end = EmptyOperator(task_id="end")

    # Thiết lập thứ tự thực thi
    start >> process_groups >> combine_task >> load_to_db >> load_to_dwh >> end







