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

* sử dụng crawl từ ssi, lý do là dữ liệu ở đây rất đầy đủ, có tính mới nhất và chính xác nhất.
* sử dụng selenium
* tạo 2 container là 2 trình duyệt
* sử dụng 2 tài khoản
* thực hiện crawl song song để giảm 1 nửa thời gian

## c. Lịch sử giá

* sử dụng vnstock: sử dụng bởi lượng dữ liệu quá lớn, trực tiếp crawl sẽ tốn rất nhiều thời gian

