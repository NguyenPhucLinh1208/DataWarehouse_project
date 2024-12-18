import sys
sys.path.append("/opt")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from datetime import timedelta

from Tasks.Load_data.load_data_to_staging import load_csv_to_db_using_copy
from Tasks.transform_and_load_data.transform_and_load import hosocongty_transform_and_load
from Tasks.extract.HistoricalData.company_profile import main_hosocongty
default_args = {
    'owner': 'airflowDWH',
    'start_date': datetime(2024, 12, 6),
    'retries': 1,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    dag_id="load_company_info_to_dwh",
    default_args=default_args,
    schedule_interval='30 19 * * 1-5',
    catchup=False,
) as dag:

    # Điểm bắt đầu DAG
    start = EmptyOperator(task_id="start")

    extract_company_info = PythonOperator(
        task_id = "extract_company_info",
        python_callable=main_hosocongty
    )

    load_to_db = PythonOperator(
        task_id = "load_company_info_to_db",
        python_callable=load_csv_to_db_using_copy,
        op_args=[
            "/opt/Tasks/extract/HistoricalData/company_info.csv",
             "HoSoCongTy",
              ["Ten_Cong_Ty", "Ma_SIC", "Ten_Nganh", "Ma_Nganh_ICB", "Nam_Thanh_Lap", "Von_Dieu_LE", "So_Luong_Nhan_Vien", "So_Luong_Chi_Nhanh", "Ngay_Niem_Yet", "Noi_Niem_Yet", "Gia_Chao_San", "KL_Dang_Niem_Yet", "Thi_Gia_Von", "SLCP_Luu_Hanh"],
        ]
    )
    
    load_to_dim_company = PythonOperator(
        task_id = 'Staging_to_Datawarehouse',
        python_callable=hosocongty_transform_and_load
    )
    # Điểm kết thúc DAG
    end = EmptyOperator(task_id="end")

    start >> extract_company_info >> load_to_db >> load_to_dim_company >> end