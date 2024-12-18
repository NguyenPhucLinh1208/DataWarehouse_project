from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_csv_to_db_using_copy(csv_file_path, table_name, columns, postgres_conn_id="load_to_staging"):
    """
    Hàm để tải dữ liệu từ file CSV vào bảng PostgreSQL bằng luồng (STDIN).

    :param csv_file_path: Đường dẫn tới file CSV nằm trong container Airflow.
    :param table_name: Tên bảng trong PostgreSQL.
    :param columns: Danh sách các cột trong bảng PostgreSQL để tải dữ liệu vào.
    :param postgres_conn_id: ID kết nối PostgreSQL trong Airflow.
    """
    # Kết nối tới PostgreSQL thông qua PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    if table_name == "HoSoCongTy":
        # Xóa toàn bộ dữ liệu cũ trong bảng
        truncate_sql = "TRUNCATE TABLE HoSoCongTy;"
        cursor.execute(truncate_sql)

    # Chuyển danh sách cột thành một chuỗi
    columns_str = ', '.join(columns)

    # Tạo câu lệnh COPY
    copy_sql = f"""
    COPY {table_name} ({columns_str})
    FROM STDIN
    WITH CSV HEADER
    DELIMITER ',';
    """

    try:
        # Đọc file CSV từ container Airflow
        with open(csv_file_path, "r") as csv_file:
            # Thực thi lệnh COPY với luồng file
            cursor.copy_expert(sql=copy_sql, file=csv_file)
        
        # Commit transaction
        conn.commit()
        print(f"Dữ liệu đã được tải thành công vào bảng {table_name}.")
    except Exception as e:
        print(f"Error during COPY operation: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
