-- dim_exchange
INSERT INTO dim_exchange (san_niem_yet, mo_ta)
VALUES ('HOSE', 'Sở Giao dịch Chứng khoán Thành phố Hồ Chí Minh'),
       ('HNX', 'Sở Giao dịch Chứng khoán Hà Nội'),
       ('UPCOM', 'Thị trường UPCOM là nơi giao dịch các chứng khoán của các công ty đại chúng chưa được niêm yết tại HOSE hoặc HNX');

-- dim_icb
INSERT INTO dim_icb (Ma_ICB, Ten_nhom_nganh)
VALUES ('8633', 'Các công ty đầu cơ và phát triển bất động sản'),
       ('8637', 'Dịch vụ bất động sản');

-- dim_match_period: thời điểm khớp lệnh theo sàn và giờ (định kì mở cửa, đóng cửa, liên tục)

-- dim_match_type: mua, bán

-- dim_report_type
INSERT INTO dim_report_type (Report_type, Mo_ta)
VALUES ('Cân đối kế toán', 'Báo cáo tài sản, nợ phải trả và vốn chủ sở hữu của công ty tại một thời điểm cụ thể.'),
       ('Kết quả kinh doanh', 'Báo cáo thu nhập, chi phí và lợi nhuận của công ty trong một khoảng thời gian nhất định.'),
       ('Lưu chuyển tiền tệ', 'Báo cáo sự lưu thông tiền mặt ra vào trong công ty trong một khoảng thời gian nhất định.');

-- dim_account 
INSERT INTO dim_account (Ma_tai_khoan, Ten_tai_khoan, Loai_tai_khoan, Report_type) VALUES
-- Cân đối kế toán - Tài sản ngắn hạn
('1001', 'Tiền Và Tương Đương Tiền', 'Tài sản ngắn hạn', 'Cân đối kế toán'),
('1002', 'Giá Trị Thuần Đầu Tư Ngắn Hạn', 'Tài sản ngắn hạn', 'Cân đối kế toán'),
('1003', 'Các Khoản Phải Thu', 'Tài sản ngắn hạn', 'Cân đối kế toán'),
('1004', 'Hàng Tồn Kho, Ròng', 'Tài sản ngắn hạn', 'Cân đối kế toán'),
('1005', 'Tài Sản Lưu Động Khác', 'Tài sản ngắn hạn', 'Cân đối kế toán'),

-- Cân đối kế toán - Tài sản dài hạn
('2001', 'Phải Thu Dài Hạn', 'Tài sản dài hạn', 'Cân đối kế toán'),
('2002', 'Tài Sản Cố Định', 'Tài sản dài hạn', 'Cân đối kế toán'),
('2003', 'Giá Trị Ròng Tài Sản Đầu Tư', 'Tài sản dài hạn', 'Cân đối kế toán'),
('2004', 'Tài Sản Dở Dang Dài Hạn', 'Tài sản dài hạn', 'Cân đối kế toán'),
('2005', 'Đầu Tư Dài Hạn', 'Tài sản dài hạn', 'Cân đối kế toán'),
('2006', 'Tài Sản Dài Hạn Khác', 'Tài sản dài hạn', 'Cân đối kế toán'),

-- Cân đối kế toán - Nợ phải trả
('3001', 'Nợ Ngắn Hạn', 'Nợ phải trả', 'Cân đối kế toán'),
('3002', 'Nợ Dài Hạn', 'Nợ phải trả', 'Cân đối kế toán'),

-- Cân đối kế toán - Vốn chủ sở hữu
('4001', 'Vốn Và Các Quỹ', 'Vốn chủ sở hữu', 'Cân đối kế toán'),
('4002', 'Quỹ Khen Thưởng, Phúc Lợi (Trước 2010)', 'Vốn chủ sở hữu', 'Cân đối kế toán'),

-- Kết quả kinh doanh - Doanh thu
('5001', 'Doanh Số', 'Doanh thu', 'Kết quả kinh doanh'),
('5002', 'Các Khoản Giảm Trừ', 'Doanh thu', 'Kết quả kinh doanh'),

-- Kết quả kinh doanh - Chi phí sản xuất, kinh doanh
('6001', 'Giá Vốn Hàng Bán', 'Chi phí sản xuất, kinh doanh', 'Kết quả kinh doanh'),
('6002', 'Chi Phí Bán Hàng', 'Chi phí sản xuất, kinh doanh', 'Kết quả kinh doanh'),
('6003', 'Chi Phí Quản Lý Doanh Nghiệp', 'Chi phí sản xuất, kinh doanh', 'Kết quả kinh doanh'),

-- Kết quả kinh doanh - Thu nhập khác
('7001', 'Thu Nhập Tài Chính', 'Thu nhập khác', 'Kết quả kinh doanh'),
('7002', 'Thu Nhập Khác, Ròng', 'Thu nhập khác', 'Kết quả kinh doanh'),

-- Kết quả kinh doanh - Chi phí khác
('8001', 'Chi Phí Tài Chính', 'Chi phí khác', 'Kết quả kinh doanh'),
('8002', 'Chi Phí Thuế Thu Nhập Doanh Nghiệp', 'Chi phí khác', 'Kết quả kinh doanh'),

-- Kết quả kinh doanh - Xác định kết quả kinh doanh
('9001', 'Lãi Gộp', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),
('9002', 'Lãi/(Lỗ) Từ Hoạt Động Kinh Doanh', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),
('9003', 'Lãi/(Lỗ) Từ Công Ty Liên Doanh (Từ Năm 2015)', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),
('9004', 'Lãi/(Lỗ) Từ Công Ty Liên Doanh (Trước Năm 2015)', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),
('9005', 'Lãi/(Lỗ) Ròng Trước Thuế', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),
('9006', 'Lãi/(Lỗ) Thuần Sau Thuế', 'Xác định kết quả kinh doanh', 'Kết quả kinh doanh'),

-- Cân đối kế toán - Tài khoản ngoài bảng
('0001', 'Lợi Ích Của Cổ Đông Thiểu Số', 'Tài khoản ngoài bảng', 'Kết quả kinh doanh'),
('0002', 'Lợi Nhuận Của Cổ Đông Của Công Ty Mẹ', 'Tài khoản ngoài bảng', 'Kết quả kinh doanh'),
('0003', 'Lãi Cơ Bản Trên Cổ Phiếu (VND)', 'Tài khoản ngoài bảng', 'Kết quả kinh doanh'),
('0004', 'Lãi Trên Cổ Phiếu Pha Loãng (VND)', 'Tài khoản ngoài bảng', 'Kết quả kinh doanh'),
('0005', 'EBITDA', 'Tài khoản ngoài bảng', 'Kết quả kinh doanh'),

-- Lưu chuyển tiền tệ
('10001', 'Lưu Chuyển Tiền Tệ Ròng Từ Các Hoạt Động Sản Xuất Kinh Doanh', 'Tài khoản lưu chuyển tiền tệ', 'Lưu chuyển tiền tệ'),
('10002', 'Lưu Chuyển Tiền Tệ Ròng Từ Hoạt Động Đầu Tư', 'Tài khoản lưu chuyển tiền tệ', 'Lưu chuyển tiền tệ'),
('10003', 'Lưu Chuyển Tiền Tệ Từ Hoạt Động Tài Chính', 'Tài khoản lưu chuyển tiền tệ', 'Lưu chuyển tiền tệ'),
('10004', 'Tiền Và Tương Đương Tiền Đầu Kỳ', 'Tài khoản lưu chuyển tiền tệ', 'Lưu chuyển tiền tệ'),
('10005', 'Ảnh Hưởng Của Chênh Lệch Tỷ Giá', 'Tài khoản lưu chuyển tiền tệ', 'Lưu chuyển tiền tệ');


-- dim_time_period
INSERT INTO dim_time_period (time_period_id, Nam, Quy)
VALUES
    ('Q1 2007', 2007, 1),
    ('Q2 2007', 2007, 2),
    ('Q3 2007', 2007, 3),
    ('Q4 2007', 2007, 4),
    ('Q1 2008', 2008, 1),
    ('Q2 2008', 2008, 2),
    ('Q3 2008', 2008, 3),
    ('Q4 2008', 2008, 4),
    ('Q1 2009', 2009, 1),
    ('Q2 2009', 2009, 2),
    ('Q3 2009', 2009, 3),
    ('Q4 2009', 2009, 4),
    ('Q1 2010', 2010, 1),
    ('Q2 2010', 2010, 2),
    ('Q3 2010', 2010, 3),
    ('Q4 2010', 2010, 4),
    ('Q1 2011', 2011, 1),
    ('Q2 2011', 2011, 2),
    ('Q3 2011', 2011, 3),
    ('Q4 2011', 2011, 4),
    ('Q1 2012', 2012, 1),
    ('Q2 2012', 2012, 2),
    ('Q3 2012', 2012, 3),
    ('Q4 2012', 2012, 4),
    ('Q1 2013', 2013, 1),
    ('Q2 2013', 2013, 2),
    ('Q3 2013', 2013, 3),
    ('Q4 2013', 2013, 4),
    ('Q1 2014', 2014, 1),
    ('Q2 2014', 2014, 2),
    ('Q3 2014', 2014, 3),
    ('Q4 2014', 2014, 4),
    ('Q1 2015', 2015, 1),
    ('Q2 2015', 2015, 2),
    ('Q3 2015', 2015, 3),
    ('Q4 2015', 2015, 4),
    ('Q1 2016', 2016, 1),
    ('Q2 2016', 2016, 2),
    ('Q3 2016', 2016, 3),
    ('Q4 2016', 2016, 4),
    ('Q1 2017', 2017, 1),
    ('Q2 2017', 2017, 2),
    ('Q3 2017', 2017, 3),
    ('Q4 2017', 2017, 4),
    ('Q1 2018', 2018, 1),
    ('Q2 2018', 2018, 2),
    ('Q3 2018', 2018, 3),
    ('Q4 2018', 2018, 4),
    ('Q1 2019', 2019, 1),
    ('Q2 2019', 2019, 2),
    ('Q3 2019', 2019, 3),
    ('Q4 2019', 2019, 4),
    ('Q1 2020', 2020, 1),
    ('Q2 2020', 2020, 2),
    ('Q3 2020', 2020, 3),
    ('Q4 2020', 2020, 4),
    ('Q1 2021', 2021, 1),
    ('Q2 2021', 2021, 2),
    ('Q3 2021', 2021, 3),
    ('Q4 2021', 2021, 4),
    ('Q1 2022', 2022, 1),
    ('Q2 2022', 2022, 2),
    ('Q3 2022', 2022, 3),
    ('Q4 2022', 2022, 4),
    ('Q1 2023', 2023, 1),
    ('Q2 2023', 2023, 2),
    ('Q3 2023', 2023, 3),
    ('Q4 2023', 2023, 4),
    ('Q1 2024', 2024, 1),
    ('Q2 2024', 2024, 2),
    ('Q3 2024', 2024, 3),
    ('Q4 2024', 2024, 4),
    ('Q1 2025', 2025, 1),
    ('Q2 2025', 2025, 2),
    ('Q3 2025', 2025, 3),
    ('Q4 2025', 2025, 4),
    ('Q1 2026', 2026, 1),
    ('Q2 2026', 2026, 2),
    ('Q3 2026', 2026, 3),
    ('Q4 2026', 2026, 4),
    ('Q1 2027', 2027, 1),
    ('Q2 2027', 2027, 2),
    ('Q3 2027', 2027, 3),
    ('Q4 2027', 2027, 4),
    ('Q1 2028', 2028, 1),
    ('Q2 2028', 2028, 2),
    ('Q3 2028', 2028, 3),
    ('Q4 2028', 2028, 4);

-- dim_date
-- Tự động sinh dữ liệu, bỏ qua những ngày không giao dịch là thứ 7, chủ nhật
INSERT INTO dim_date (date_id, day, month, year)
SELECT 
    d AS date_id,
    EXTRACT(DAY FROM d)::INT AS day,
    EXTRACT(MONTH FROM d)::INT AS month,
    EXTRACT(YEAR FROM d)::INT AS year
FROM 
    generate_series('2015-01-01'::DATE, '2028-12-31'::DATE, '1 day') d
WHERE 
    EXTRACT(DOW FROM d) NOT IN (0, 6);  -- 0 = Chủ nhật, 6 = Thứ 7

-- dim_company: thực hiện bằng ETL

-- fact_Price_History: thực hiện ETL xong
-- fact_fanancials: thực hiện ETL
