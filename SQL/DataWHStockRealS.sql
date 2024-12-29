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
    Ten_tai_khoan VARCHAR(255),
    Loai_tai_khoan VARCHAR(255),
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
    date_id DATE PRIMARY KEY,
    day INT,
    month INT,
    year INT
);

-- Bảng dim_company
CREATE TABLE dim_company (
    Ten_cong_ty VARCHAR(255),
    Ma_SIC VARCHAR(10) PRIMARY KEY,
    Ma_ICB VARCHAR(50),
    Nam_thanh_lap DATE,
    Von_dieu_le NUMERIC(10,2),
    So_luong_nhan_vien INT,
    Ngay_niem_yet DATE,
    San_niem_yet VARCHAR(50),
    Gia_chao_san NUMERIC(15,2),
    KL_dang_niem_yet BIGINT,
    Thi_gia_von NUMERIC(10,2),
    SLCP_luu_hanh BIGINT,
    FOREIGN KEY (Ma_ICB) REFERENCES dim_icb(Ma_ICB),
    FOREIGN KEY (San_niem_yet) REFERENCES dim_exchange(San_niem_yet)
);

-- Bảng fact_intraday_trading
CREATE TABLE fact_intraday_trading (
    Time TIMESTAMP,
    price NUMERIC(10,2),
    volume BIGINT,
    Match_type VARCHAR(50),
    Ma_SIC VARCHAR(50),
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (Match_type) REFERENCES dim_match_type(Match_type)
);

-- Bảng fact_fanancials
CREATE TABLE fact_fanancials (
    Ma_tai_khoan VARCHAR(50),
    time_period_id VARCHAR(50),
    Gia_tri NUMERIC(10,2),
    Ma_SIC VARCHAR(10),
    FOREIGN KEY (Ma_tai_khoan) REFERENCES dim_account(Ma_tai_khoan),
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (time_period_id) REFERENCES dim_time_period(time_period_id)
);

-- Bảng fact_Price_History
CREATE TABLE fact_Price_History (
    date_id DATE,
    open NUMERIC(10,2),
    hight NUMERIC(10,2),
    low NUMERIC(10,2),
    close NUMERIC(10,2),
    Volume INT,
    Ma_SIC VARCHAR(10),
    FOREIGN KEY (Ma_SIC) REFERENCES dim_company(Ma_SIC),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
