from airflow.providers.postgres.hooks.postgres import PostgresHook

def hosocongty_transform_and_load():

    sql_transform = """
            SELECT 
                Ten_Cong_Ty AS Ten_cong_ty,
                Ma_SIC,
                Ma_Nganh_ICB AS Ma_ICB,
                TO_DATE(Nam_Thanh_Lap, 'DD/MM/YYYY') AS Nam_thanh_lap,  -- Chuyển đổi ngày tháng đúng định dạng
                REPLACE(REPLACE(Von_Dieu_LE, 'Tỷ', ''), ',', '')::NUMERIC(10,2) AS Von_dieu_le,
                REPLACE(So_Luong_Nhan_Vien, ',', '')::INT AS So_luong_nhan_vien,
                TO_DATE(Ngay_Niem_Yet, 'DD/MM/YYYY') AS Ngay_niem_yet,  -- Chuyển đổi ngày tháng đúng định dạng
                Noi_Niem_Yet AS San_niem_yet,
                (Gia_Chao_San::NUMERIC(15,2) * 1000) AS Gia_chao_san,
                REPLACE(KL_Dang_Niem_Yet, ',', '')::BIGINT AS KL_dang_niem_yet,
                REPLACE(REPLACE(Thi_Gia_Von, ',', ''), 'Tỷ', '')::NUMERIC(10,2) AS Thi_gia_von,
                REPLACE(SLCP_Luu_Hanh, ',', '')::BIGINT AS SLCP_luu_hanh
            FROM HoSoCongTy;
    """

    staging_hook = PostgresHook(postgres_conn_id="load_to_staging")
    staging_conn = staging_hook.get_conn()
    staging_cursor = staging_conn.cursor()

    staging_cursor.execute(sql_transform)
    transformed_data = staging_cursor.fetchall()

    sql_insert = """
            INSERT INTO dim_company (
                Ten_cong_ty, Ma_SIC, Ma_ICB, Nam_thanh_lap, Von_dieu_le,
                So_luong_nhan_vien, Ngay_niem_yet, San_niem_yet, Gia_chao_san,
                KL_dang_niem_yet, Thi_gia_von, SLCP_luu_hanh
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    dwh_hook = PostgresHook(postgres_conn_id="load_to_dwh")
    dwh_conn = dwh_hook.get_conn()
    dwh_cursor = dwh_conn.cursor()
    dwh_cursor.executemany(sql_insert, transformed_data)
    dwh_conn.commit()

    # Đóng kết nối
    staging_cursor.close()
    staging_conn.close()
    dwh_cursor.close()
    dwh_conn.close()

    print("ETL process completed successfully.")

def fact_Price_History_transform_load():
    sql_transform = """
            SELECT 
                Thoi_Gian AS date_id,
                (Gia_Opening::NUMERIC(10,2) * 1000) AS open,
                (Gia_High::NUMERIC(10,2) * 1000) AS hight,
                (Gia_Low::NUMERIC(10,2) * 1000) AS low,
                (Gia_Closing::NUMERIC(10,2) * 1000) AS close,
                khoi_luong AS volume,
                Ma_SIC
            FROM LichSuGia
            WHERE Status = 'New';
    """

    staging_hook = PostgresHook(postgres_conn_id="load_to_staging")
    staging_conn = staging_hook.get_conn()
    staging_cursor = staging_conn.cursor()

    staging_cursor.execute(sql_transform)
    transformed_data = staging_cursor.fetchall()

    sql_insert = """
            INSERT INTO fact_Price_History (
                date_id, open, hight, low, close, volume, Ma_SIC
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    dwh_hook = PostgresHook(postgres_conn_id="load_to_dwh")
    dwh_conn = dwh_hook.get_conn()
    dwh_cursor = dwh_conn.cursor()
    dwh_cursor.executemany(sql_insert, transformed_data)
    dwh_conn.commit()

    # Cập nhật trạng thái sang 'Processed'
    sql_update_status = """
        UPDATE LichSuGia
        SET Status = 'Processed'
        WHERE Status = 'New';
    """
    staging_cursor.execute(sql_update_status)
    staging_conn.commit()

    # Đóng kết nối
    staging_cursor.close()
    staging_conn.close()
    dwh_cursor.close()
    dwh_conn.close()

    print("ETL process completed successfully.")

def fact_financials_tranform_load():

    sql_transform = """
        SELECT 
            CASE 
                WHEN chi_tieu = 'Tiền Và Tương Đương Tiền' THEN '1001'
                WHEN chi_tieu = 'Giá Trị Thuần Đầu Tư Ngắn Hạn' THEN '1002'
                WHEN chi_tieu = 'Các Khoản Phải Thu' THEN '1003'
                WHEN chi_tieu = 'Hàng Tồn Kho, Ròng' THEN '1004'
                WHEN chi_tieu = 'Tài Sản Lưu Động Khác' THEN '1005'
                WHEN chi_tieu = 'Phải Thu Dài Hạn' THEN '2001'
                WHEN chi_tieu = 'Tài Sản Cố Định' THEN '2002'
                WHEN chi_tieu = 'Giá Trị Ròng Tài Sản Đầu Tư' THEN '2003'
                WHEN chi_tieu = 'Tài Sản Dở Dang Dài Hạn' THEN '2004'
                WHEN chi_tieu = 'Đầu Tư Dài Hạn' THEN '2005'
                WHEN chi_tieu = 'Tài Sản Dài Hạn Khác' THEN '2006'
                WHEN chi_tieu = 'Nợ Ngắn Hạn' THEN '3001'
                WHEN chi_tieu = 'Nợ Dài Hạn' THEN '3002'
                WHEN chi_tieu = 'Vốn Và Các Quỹ' THEN '4001'
                WHEN chi_tieu = 'Quỹ Khen Thưởng, Phúc Lợi (Trước 2010)' THEN '4002'
                ELSE NULL -- Trường hợp không khớp
            END AS Ma_tai_khoan,
            thoi_gian AS time_period_id,
            REPLACE(REPLACE(gia_tri, ',', ''), '--', '0')::NUMERIC(10,2),
            ma_sic
        FROM candoiketoan
        WHERE chi_tieu NOT IN ('TỔNG TÀI SẢN', 'TÀI SẢN NGẮN HẠN', 'TÀI SẢN DÀI HẠN', 
                            'NỢ PHẢI TRẢ', 'VỐN CHỦ SỞ HỮU', 'LỢI ÍCH CỦA CỔ ĐÔNG THIỂU SỐ', 
                            'TỔNG CỘNG NGUỒN VỐN') AND status = 'New';

    """

    sql_transform_1 = """
        SELECT 
            CASE 
                WHEN chi_tieu = 'Doanh Số' THEN '5001'
                WHEN chi_tieu = 'Các Khoản Giảm Trừ' THEN '5002'
                WHEN chi_tieu = 'Giá Vốn Hàng Bán' THEN '6001'
                WHEN chi_tieu = 'Chi Phí Bán Hàng' THEN '6002'
                WHEN chi_tieu = 'Chi Phí Quản Lý Doanh Nghiệp' THEN '6003'
                WHEN chi_tieu = 'Thu Nhập Tài Chính' THEN '7001'
                WHEN chi_tieu = 'Thu Nhập Khác, Ròng' THEN '7002'
                WHEN chi_tieu = 'Chi Phí Tài Chính' THEN '8001'
                WHEN chi_tieu = 'Chi Phí Thuế Thu Nhập Doanh Nghiệp' THEN '8002'
                WHEN chi_tieu = 'Lãi Gộp' THEN '9001'
                WHEN chi_tieu = 'Lãi/(Lỗ) Từ Hoạt Động Kinh Doanh' THEN '9002'
                WHEN chi_tieu = 'Lãi/(Lỗ) Từ Công Ty Liên Doanh (Từ Năm 2015)' THEN '9003'
                WHEN chi_tieu = 'Lãi/(Lỗ) Từ Công Ty Liên Doanh (Trước Năm 2015)' THEN '9004'
                WHEN chi_tieu = 'Lãi/(Lỗ) Ròng Trước Thuế' THEN '9005'
                WHEN chi_tieu = 'Lãi/(Lỗ) Thuần Sau Thuế' THEN '9006'
                WHEN chi_tieu = 'Lợi Ích Của Cổ Đông Thiểu Số' THEN '0001'
                WHEN chi_tieu = 'Lợi Nhuận Của Cổ Đông Của Công Ty Mẹ' THEN '0002'
                WHEN chi_tieu = 'Lãi Cơ Bản Trên Cổ Phiếu (VND)' THEN '0003'
                WHEN chi_tieu = 'Lãi Trên Cổ Phiếu Pha Loãng (VND)' THEN '0004'
                WHEN chi_tieu = 'EBITDA' THEN '0005'
                ELSE NULL -- Trường hợp không khớp
            END AS Ma_tai_khoan,
            thoi_gian AS time_period_id,
            REPLACE(REPLACE(gia_tri, ',', ''), '--', '0')::NUMERIC(10,2),
            ma_sic
        FROM ketquakinhdoanh
        WHERE chi_tieu NOT IN (
            'Doanh Số Thuần'
        ) AND 
        status = 'New';

    """

    sql_transform_2 = """
        SELECT 
            CASE 
                WHEN chi_tieu = 'Lưu Chuyển Tiền Tệ Ròng Từ Các Hoạt Động Sản Xuất Kinh Doanh' THEN '10001'
                WHEN chi_tieu = 'Lưu Chuyển Tiền Tệ Ròng Từ Hoạt Động Đầu Tư' THEN '10002'
                WHEN chi_tieu = 'Lưu Chuyển Tiền Tệ Từ Hoạt Động Tài Chính' THEN '10003'
                WHEN chi_tieu = 'Tiền Và Tương Đương Tiền Đầu Kỳ' THEN '10004'
                WHEN chi_tieu = 'Ảnh Hưởng Của Chênh Lệch Tỷ Giá' THEN '10005'
                ELSE NULL -- Trường hợp không khớp
            END AS Ma_tai_khoan,
            thoi_gian AS time_period_id,
            REPLACE(REPLACE(gia_tri, ',', ''), '--', '0')::NUMERIC(10,2),
            ma_sic
        FROM luuchuyentiente
        WHERE chi_tieu NOT IN (
            'Lưu Chuyển Tiền Thuần Trong Kỳ',
            'Tiền Và Tương Đương Tiền Cuối Kỳ'
        ) AND 
        status = 'New';
    """


    sql_insert = """
            INSERT INTO fact_fanancials (
                Ma_tai_khoan, time_period_id, Gia_tri, Ma_SIC
            ) VALUES (%s, %s, %s, %s);
    """

    staging_hook = PostgresHook(postgres_conn_id="load_to_staging")
    staging_conn = staging_hook.get_conn()
    staging_cursor = staging_conn.cursor()

    staging_cursor.execute(sql_transform_1)
    transformed_data_1 = staging_cursor.fetchall()

    staging_cursor.execute(sql_transform)
    transformed_data = staging_cursor.fetchall()

    staging_cursor.execute(sql_transform_2)
    transformed_data_2 = staging_cursor.fetchall()

    dwh_hook = PostgresHook(postgres_conn_id="load_to_dwh")
    dwh_conn = dwh_hook.get_conn()
    dwh_cursor = dwh_conn.cursor()
    dwh_cursor.executemany(sql_insert, transformed_data)
    dwh_cursor.executemany(sql_insert, transformed_data_1)
    dwh_cursor.executemany(sql_insert, transformed_data_2)

    dwh_conn.commit()

    # Cập nhật trạng thái sang 'Processed'
    sql_update_status = """
        UPDATE candoiketoan
        SET Status = 'Processed'
        WHERE Status = 'New';
    """
    sql_update_status_1 = """
        UPDATE ketquakinhdoanh
        SET Status = 'Processed'
        WHERE Status = 'New';
    """
    sql_update_status_2 = """
        UPDATE luuchuyentiente
        SET Status = 'Processed'
        WHERE Status = 'New';
    """
    staging_cursor.execute(sql_update_status)
    staging_cursor.execute(sql_update_status_1)
    staging_cursor.execute(sql_update_status_2)

    staging_conn.commit()

    # Đóng kết nối
    staging_cursor.close()
    staging_conn.close()
    dwh_cursor.close()
    dwh_conn.close()

    print("ETL process completed successfully.")

