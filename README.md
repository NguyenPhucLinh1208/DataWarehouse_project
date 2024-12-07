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

