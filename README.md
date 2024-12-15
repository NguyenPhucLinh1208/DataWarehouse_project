# 0. Overview

Thiết lập docker như thế nào:

tôi xây dựng trong devcontainer, sẽ dùng container chính là data warehouse, được build trực tiếp từ dockerfile

để khắc phục các vấn đề như đồng bộ dữ liệu, dùng volumes, và enviroments

để chia sẻ không qua ip, mà qua tên, dùng network

# 1. Dữ liệu

## a. Công ty 

* Đầu tiên, lấy thông tin tên công ty bất động sản, lưu vào file MaCks.txt
* Sau đó, crawl dữ liệu từ SSI về hồ sơ công ty.
* thực hiện crawl trong 127 mã, lấy thông tin cơ bản và thông tin niêm yét

## b. Báo cáo tài chính

LỊCH SỬ:

* sử dụng crawl từ ssi, lý do là dữ liệu ở đây rất đầy đủ, có tính mới nhất và chính xác nhất.
* sử dụng selenium
* tạo 2 container là 2 trình duyệt
* sử dụng 2 tài khoản
* thực hiện crawl song song để giảm 1 nửa thời gian

HIỆN TẠI:
* đã xong

## c. Lịch sử giá

* sử dụng vnstock: sử dụng bởi lượng dữ liệu quá lớn, trực tiếp crawl sẽ tốn rất nhiều thời gian
* crawl song song 5 task

### d. Kết quả giao dịch

* đây là dữ liệu real time, cần sử dụng kafka 

# 2. Transfrome dữ liệu trong staging

## a. check logs, kiểm tra nên giữ hay xóa data nào?

* lỗi và thiếu (từ 2 loại báo cáo trở lên): C21, HPI, HU6, HTN (cần load lại vì đủ hết), DIG (cần load lại), 

## b. Làm sạch và chuyển đổi kiểu dữ liệu

### b0 xử lý dữ liệu thiếu
* lấy dữ liệu từ staging, chỉ lấy những dữ liệu được đánh dấu là "New", tức là những hàng này chưa được xử lý
* ý tưởng thế nào: 
  * tạo view của các bảng chỉ lấy status = New
  * thực hiện transform (b1,b2,b3)
  * thực hiện đổ vào dwh
### b1 Hồ sơ công ty. 

* chuyển đổi năm thành lập, ngày niêm yết thành dạng: năm, tháng, ngày. 
* vốn điều lệ, thị giá vốn (tỷ): bỏ dấu dấu , --> Numeric(10,2)
* số lượng nhân viên: bỏ , --> integer
* giá chào sàn: x 1000 (đồng) --> numeric (15,2)
* khối lượng đang niêm yết, khối lượng cổ phiếu đang lưu hành: bỏ , --> integer
 
### b2 Lịch sử giá. 

* open, high, low, close:  x 1000 (đồng) --> numeric (15,2)

### b3 các báo cáo tài chính:

* thời gian: tách thành thời gian (TEXT), quý (1,2,3,4 int), năm (int)
* giá trị (tỷ): bỏ , --> numeric (15,2)

### b4 cách phân loại tài khoản

TỔNG TÀI SẢN  = Tổng ngắn hạn + tổng dài hạn = TỔNG CỘNG NGUỒN VỐN

Tài khoản loại 1: Tài sản ngắn hạn (TSNH).
TÀI SẢN NGẮN HẠN  = tổng
    Tiền Và Tương Đương Tiền  
    Giá Trị Thuần Đầu Tư Ngắn Hạn  
    Các Khoản Phải Thu  
    Hàng Tồn Kho, Ròng  
    Tài Sản Lưu Động Khác  

Tài khoản loại 2: Tài sản dài hạn (TSDH).
TÀI SẢN DÀI HẠN  = tổng
    Phải Thu Dài Hạn  
    Tài Sản Cố Định  
    Giá Trị Ròng Tài Sản Đầu Tư  
    Tài Sản Dở Dang Dài Hạn  
    Đầu Tư Dài Hạn  
    Tài Sản Dài Hạn Khác  

Tài khoản loại 3: Nợ phải trả (NPT).
NỢ PHẢI TRẢ  = tổng
    Nợ Ngắn Hạn  
    Nợ Dài Hạn  

Tài khoản loại 4: Vốn chủ sở hữu.
VỐN CHỦ SỞ HỮU = tổng
    Vốn Và Các Quỹ  
    Quỹ Khen Thưởng, Phúc Lợi (Trước 2010)  

Tài khoản loại 5: Doanh thu.
Doanh Số Thuần  = tổng
    Doanh Số 
    Các Khoản Giảm Trừ  

Tài khoản loại 6: Chi phí sản xuất, kinh doanh.
Giá Vốn Hàng Bán  
Chi Phí Bán Hàng  
Chi Phí Quản Lý Doanh Nghiệp  

Tài khoản loại 7: Thu nhập khác.
Thu Nhập Tài Chính  
Thu Nhập Khác, Ròng  

Tài khoản loại 8: Chi phí khác.
Chi Phí Tài Chính 
Chi Phí Thuế Thu Nhập Doanh Nghiệp   

Tài khoản loại 9: Xác định kết quả kinh doanh.
Lãi Gộp  
Lãi/(Lỗ) Từ Hoạt Động Kinh Doanh  
Lãi/(Lỗ) Từ Công Ty Liên Doanh (Từ Năm 2015)  
Lãi/(Lỗ) Từ Công Ty Liên Doanh (Trước Năm 2015)  
Lãi/(Lỗ) Ròng Trước Thuế  
Lãi/(Lỗ) Thuần Sau Thuế  

Tài khoản loại 0: Tài khoản ngoài bảng.
Lợi Ích Của Cổ Đông Thiểu Số  
Lợi Nhuận Của Cổ Đông Của Công Ty Mẹ  
Lãi Cơ Bản Trên Cổ Phiếu (VND)  
Lãi Trên Cổ Phiếu Pha Loãng (VND)  
EBITDA  

Tài khoản loại 10: Tài khoản lưu chuyển tiền tệ.

Lưu Chuyển Tiền Thuần Trong Kỳ  = Tổng
    Lưu Chuyển Tiền Tệ Ròng Từ Các Hoạt Động Sản Xuất Kinh Doanh 
    Lưu Chuyển Tiền Tệ Ròng Từ Hoạt Động Đầu Tư  
    Lưu Chuyển Tiền Tệ Từ Hoạt Động Tài Chính  

Tiền Và Tương Đương Tiền Cuối Kỳ = tổng
    Tiền Và Tương Đương Tiền Đầu Kỳ
    Lưu Chuyển Tiền Thuần Trong Kỳ  

Ảnh Hưởng Của Chênh Lệch Tỷ Giá 


 TỔNG TÀI SẢN  = Tổng ngắn hạn + tổng dài hạn = TỔNG CỘNG NGUỒN VỐN
-- Cân đối kế toán
Tài khoản loại 1: Tài sản ngắn hạn (TSNH).
    Tiền Và Tương Đương Tiền  
    Giá Trị Thuần Đầu Tư Ngắn Hạn  
    Các Khoản Phải Thu  
    Hàng Tồn Kho, Ròng  
    Tài Sản Lưu Động Khác  

Tài khoản loại 2: Tài sản dài hạn (TSDH).
    Phải Thu Dài Hạn  
    Tài Sản Cố Định  
    Giá Trị Ròng Tài Sản Đầu Tư  
    Tài Sản Dở Dang Dài Hạn  
    Đầu Tư Dài Hạn  
    Tài Sản Dài Hạn Khác  

Tài khoản loại 3: Nợ phải trả (NPT).
    Nợ Ngắn Hạn  
    Nợ Dài Hạn  

Tài khoản loại 4: Vốn chủ sở hữu.
    Vốn Và Các Quỹ  
    Quỹ Khen Thưởng, Phúc Lợi (Trước 2010)  

-- Kết quả kinh doanh
Tài khoản loại 5: Doanh thu.
    Doanh Số 
    Các Khoản Giảm Trừ  

Tài khoản loại 6: Chi phí sản xuất, kinh doanh.
    Giá Vốn Hàng Bán  
    Chi Phí Bán Hàng  
    Chi Phí Quản Lý Doanh Nghiệp  

Tài khoản loại 7: Thu nhập khác.
    Thu Nhập Tài Chính  
    Thu Nhập Khác, Ròng  

Tài khoản loại 8: Chi phí khác.
    Chi Phí Tài Chính 
    Chi Phí Thuế Thu Nhập Doanh Nghiệp   

Tài khoản loại 9: Xác định kết quả kinh doanh.
    Lãi Gộp  
    Lãi/(Lỗ) Từ Hoạt Động Kinh Doanh  
    Lãi/(Lỗ) Từ Công Ty Liên Doanh (Từ Năm 2015)  
    Lãi/(Lỗ) Từ Công Ty Liên Doanh (Trước Năm 2015)  
    Lãi/(Lỗ) Ròng Trước Thuế  
    Lãi/(Lỗ) Thuần Sau Thuế  

Tài khoản loại 0: Tài khoản ngoài bảng.
    Lợi Ích Của Cổ Đông Thiểu Số  
    Lợi Nhuận Của Cổ Đông Của Công Ty Mẹ  
    Lãi Cơ Bản Trên Cổ Phiếu (VND)  
    Lãi Trên Cổ Phiếu Pha Loãng (VND)  
    EBITDA  

-- Lưu chuyển tiền tệ
Tài khoản loại 10: Tài khoản lưu chuyển tiền tệ.

    Lưu Chuyển Tiền Tệ Ròng Từ Các Hoạt Động Sản Xuất Kinh Doanh 
    Lưu Chuyển Tiền Tệ Ròng Từ Hoạt Động Đầu Tư  
    Lưu Chuyển Tiền Tệ Từ Hoạt Động Tài Chính  
    Tiền Và Tương Đương Tiền Đầu Kỳ
    Ảnh Hưởng Của Chênh Lệch Tỷ Giá 