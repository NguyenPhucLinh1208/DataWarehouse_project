# 1.Overview
Dự án xây dựng kho dữ liệu chứng khoán bất động sản. Nguồn dữ liệu từ việc web scraping, hoặc từ thư viện Vnstock.

# 2. Kiến trúc dự án

Dưới đây là sơ đồ dự án:
![Sơ đồ dự án](image/architecture.png)

Kiến trúc data warehouse

![Sơ đồ dự án](image/datawarehouse.png)

# 3. Một số luồng dữ liệu:

Pipeline thu thập giá chứng khoán

![Sơ đồ dự án](image/airflowpipeline.png)

Pipeline quản lý mã nguồn kafka 

![Sơ đồ dự án](image/airflowpipeline2.png)

Cách kafka hoạt động
![Sơ đồ dự án](image/kafka.png)

# 4. Một số dashboard:
dashboard lịch sử giá:
![Sơ đồ dự án](image/db1.png)

dashboard chỉ số tài chính
![Sơ đồ dự án](image/db2.png)

dashboard kết quả kinh doanh
![Sơ đồ dự án](image/db3.png)

dashboard kết quả trong ngày
![Sơ đồ dự án](image/db4.png)

# 4. Kết quả đạt được

Hoàn thành các dòng chảy dữ liệu tự động, hoàn chỉnh.