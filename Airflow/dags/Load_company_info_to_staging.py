import sys
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.empty import EmptyOperator

from Tasks.HistoricalData.load_to_staging import load_csv_to_db_using_copy

default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 0,
}

with DAG(
    dag_id="load_company_info_to_staging_db",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Điểm bắt đầu DAG
    start = EmptyOperator(task_id="start")

    load_to_db = PythonOperator(
        task_id = "load_company_info_to_db",
        python_callable=load_csv_to_db_using_copy,
        op_args=[
            "/opt/Tasks/HistoricalData/company_info.csv",
             "HoSoCongTy",
              ["Ten_Cong_Ty", "Ma_SIC", "Ten_Nganh", "Ma_Nganh_ICB", "Nam_Thanh_Lap", "Von_Dieu_LE", "So_Luong_Nhan_Vien", "So_Luong_Chi_Nhanh", "Ngay_Niem_Yet", "Noi_Niem_Yet", "Gia_Chao_San", "KL_Dang_Niem_Yet", "Thi_Gia_Von", "SLCP_Luu_Hanh"],
        ]
    )
    
    # Điểm kết thúc DAG
    end = EmptyOperator(task_id="end")

    start >> load_to_db >> end