CREATE TABLE HoSoCongTy (
    Ten_Cong_Ty TEXT,
    Ma_SIC TEXT,
    Ten_Nganh TEXT,
    Ma_Nganh_ICB TEXT,
    Nam_Thanh_Lap TEXT,
    Von_Dieu_LE TEXT,  -- Sử dụng TEXT để lưu giữ giá trị với đơn vị
    So_Luong_Nhan_Vien TEXT,
    So_Luong_Chi_Nhanh INTEGER,
    Ngay_Niem_Yet DATE,
    Noi_Niem_Yet TEXT,
    Gia_Chao_San TEXT,
    KL_Dang_Niem_Yet TEXT,  -- Sử dụng TEXT để lưu giữ dữ liệu có đơn vị
    Thi_Gia_Von TEXT,  -- Sử dụng TEXT để lưu giữ giá trị có đơn vị
    SLCP_Luu_Hanh TEXT  -- Sử dụng TEXT để lưu giữ giá trị có đơn vị
);

CREATE TABLE LichSuGia (
    Thoi_Gian DATE,
    Gia_Opening TEXT,
    Gia_High TEXT,
    Gia_Low TEXT,
    Gia_Closing TEXT,
    Khoi_Luong INTEGER,
    Ma_SIC TEXT
);

CREATE TABLE CanDoiKeToan (
    Chi_Tieu TEXT,
    Thoi_Gian TEXT,
    Gia_Tri TEXT,  -- Sử dụng TEXT vì giá trị có thể có đơn vị
    Ma_SIC TEXT
);

CREATE TABLE KetQuaKinhDoanh (
    Chi_Tieu TEXT,
    Thoi_Gian TEXT,
    Gia_Tri TEXT,  -- Sử dụng TEXT để lưu giá trị có đơn vị
    Ma_SIC TEXT
);

CREATE TABLE LuuChuyenTienTe (
    Chi_Tieu TEXT,
    Thoi_Gian TEXT,
    Gia_Tri TEXT,  -- Sử dụng TEXT để lưu giá trị có đơn vị
    Ma_SIC TEXT
);

CREATE TABLE KetQuaGiaoDich (
    Thoi_Gian DATE,
    Gia TEXT,
    Khoi_Luong INTEGER,
    Loai_Giao_Dich TEXT,
    ID TEXT,
    Ma_SIC TEXT
);

create table TaiKhoan (
	ChiTieu TEXT,
	Ma_Tai_Khoan TEXT
);