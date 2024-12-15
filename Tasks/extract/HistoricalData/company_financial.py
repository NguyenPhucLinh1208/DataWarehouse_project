import sys
sys.path.append("/opt")

import pandas as pd

from ScrapingPackage.browser import init_driver
from ScrapingPackage.login import login
from ScrapingPackage.navigation import switch_to_analysis_iframe, select_option_Xpath
from ScrapingPackage.scraper import enter_stock_code, get_total_financial_data

def main_report():

    with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
        stocks = [line.strip() for line in f]

    stocks = stocks[:65]
    
    # Khởi tạo trình duyệt
    driver = init_driver("http://chrome:4444/wd/hub")
    # Đăng nhập
    login(driver, "https://iboard.ssi.com.vn/analysis/fundamental-analysis", "0865163603", "Linh12345@#$")
    # chuyển vào iframe
    switch_to_analysis_iframe(driver)    

    # chọn xem theo quý
    select_option_Xpath(driver, "//button[contains(@class, 'dropdown-toggle') and @title='Năm']") 
    select_option_Xpath(driver, "//div[contains(@class, 'scrollbars')]//a[@title='Quý']" ) 

    Total_Balance = pd.DataFrame()
    Total_Income = pd.DataFrame()
    Total_CashFlow = pd.DataFrame()

    for idx, stock_code in enumerate(stocks, 1):

        enter_stock_code(driver, stock_code)

        # Tương tự cho "Kết Quả Kinh Doanh"
        try:
            Income = get_total_financial_data(driver, "Kết Quả Kinh Doanh", stock_code)
            Total_Income = pd.concat([Total_Income, Income], ignore_index=True)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Kết Quả Kinh Doanh' cho mã {stock_code}: {e}")
        # Lưu chuyển tiền tệ
        try:
            CashFlow = get_total_financial_data(driver, "Lưu Chuyển Tiền Tệ", stock_code)
            Total_CashFlow = pd.concat([Total_CashFlow, CashFlow], ignore_index=True)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Lưu Chuyển Tiền Tệ' cho mã {stock_code}: {e}")

        # Crawl dữ liệu "Cân Đối Kế Toán"
        try:
            Balance = get_total_financial_data(driver, "Cân Đối Kế Toán", stock_code)
            Total_Balance = pd.concat([Total_Balance, Balance], ignore_index=True)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Cân Đối Kế Toán' cho mã {stock_code}: {e}")

        print(f"Mã {stock_code} đã được xử lý")

        # Lưu vào file sau mỗi 5 mã chứng khoán
        if idx % 5 == 0:
            Total_Balance.to_csv("/opt/Tasks/extract/HistoricalData/Total_Balance_0.csv", index=False)
            Total_Income.to_csv("/opt/Tasks/extract/HistoricalData/Total_Income_0.csv", index=False)
            Total_CashFlow.to_csv("/opt/Tasks/extract/HistoricalData/Total_CashFlow_0.csv", index=False)
            print(f"Đã lưu dữ liệu sau {idx} mã chứng khoán.")

    # Lưu vào file sau khi hoàn thành tất cả
    Total_Balance.to_csv("/opt/Tasks/extract/HistoricalData/Total_Balance_0.csv", index=False)
    Total_Income.to_csv("/opt/Tasks/extract/HistoricalData/Total_Income_0.csv", index=False)
    Total_CashFlow.to_csv("/opt/Tasks/extract/HistoricalData/Total_CashFlow_0.csv", index=False)
    print("Lấy data báo cáo tài chính thành công")

if __name__ == "__main__":
    main_report()




