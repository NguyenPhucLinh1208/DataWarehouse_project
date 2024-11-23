-- Bảng dim_exchange
CREATE TABLE dim_exchange (
    San_niem_yet VARCHAR(50) PRIMARY KEY,
    Mo_ta VARCHAR(255)
);

-- Bảng dim_icb
CREATE TABLE dim_icb (
    Ma_ICB VARCHAR(50) PRIMARY KEY,
    Ten_nhom_nganh VARCHAR(255)
);

-- Bảng dim_match_period
CREATE TABLE dim_match_period (
    Match_period VARCHAR(50) PRIMARY KEY,
    Mo_ta VARCHAR(255)
);

-- Bảng dim_match_type
CREATE TABLE dim_match_type (
    Match_type VARCHAR(50) PRIMARY KEY
);

-- Bảng dim_report_type
CREATE TABLE dim_report_type (
    Report_type VARCHAR(50) PRIMARY KEY,
    Mo_ta VARCHAR(255)
);

-- Bảng dim_account
CREATE TABLE dim_account (
    Ma_tai_khoan VARCHAR(50) PRIMARY KEY,
    Chi_tieu VARCHAR(255),
    Report_type VARCHAR(50),
    FOREIGN KEY (Report_type) REFERENCES dim_report_type(Report_type)
);

-- Bảng dim_time_period
CREATE TABLE dim_time_period (
    time_period_id VARCHAR(50) PRIMARY KEY,
    Nam INT,
    Quy INT
);

-- Bảng dim_date
CREATE TABLE dim_date (
    date_id VARCHAR(50) PRIMARY KEY,
    day INT,
    month INT,
    year INT
);

-- Bảng dim_company
CREATE TABLE dim_company (
    Ma_SIC VARCHAR(50) PRIMARY KEY,
    Ten_cong_ty VARCHAR(255),
    Ma_ICB VARCHAR(50),
    Nam_thanh_lap INT,
    Von_dieu_le NUMERIC,
    So_luong_nhan_vien INT,
    So_luong_chi_nhanh INT,
    Ngay_niem_yet DATE,
    San_niem_yet VARCHAR(50),
    Gia_chao_san NUMERIC,
    KL_dang_niem_yet NUMERIC,
    Thi_gia_von NUMERIC,
    SLCP_luu_hanh NUMERIC,
    FOREIGN KEY (Ma_ICB) REFERENCES dim_icb(Ma_ICB),
    FOREIGN KEY (San_niem_yet) REFERENCES dim_exchange(San_niem_yet)
);

-- Bảng fact_intraday_trading
CREATE TABLE fact_intraday_trading (
    Ma_SIC VARCHAR(50),
    Match_period VARCHAR(50),
    Match_type VARCHAR(50),
    price NUMERIC,
    volume NUMERIC,
    Time TIMESTAMP,
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (Match_period) REFERENCES dim_match_period(Match_period),
    FOREIGN KEY (Match_type) REFERENCES dim_match_type(Match_type)
);

-- Bảng fact_fanancials
CREATE TABLE fact_fanancials (
    Ma_tai_khoan VARCHAR(50),
    Ma_SIC VARCHAR(50),
    time_period_id VARCHAR(50),
    Gia_tri NUMERIC,
    FOREIGN KEY (Ma_tai_khoan) REFERENCES dim_account(Ma_tai_khoan),
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (time_period_id) REFERENCES dim_time_period(time_period_id)
);

-- Bảng fact_Price_History
CREATE TABLE fact_Price_History (
    Ma_SIC VARCHAR(50),
    date_id VARCHAR(50),
    open NUMERIC,
    hight NUMERIC,
    low NUMERIC,
    close NUMERIC,
    Volume NUMERIC,
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
