import sys
sys.path.append("/opt")

import pandas as pd
from datetime import datetime

from ScrapingPackage.browser import init_driver
from ScrapingPackage.login import login
from ScrapingPackage.navigation import switch_to_analysis_iframe, select_option_Xpath
from ScrapingPackage.scraper import enter_stock_code, get_total_financial_new_data


def main_report_new_1():

    first_day_in_month = ['1-1', '4-1', '7-1', '10-1']

    current_date = datetime.now().strftime('%m-%d')

    if current_date in first_day_in_month:
        with open("/opt/Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
            stocks = [line.strip() for line in f]
    else:
        with open("/opt/Tasks/extract/NewData/next_stocks.txt", "r") as f:
            stocks = [line.strip() for line in f]      
    length = len(stocks) // 2
    stocks = stocks[length:]

    last_stocks = set()  # Đây là set rỗng

    # Khởi tạo trình duyệt
    driver = init_driver("http://chrome_1:4444/wd/hub")
    # Đăng nhập
    login(driver, "https://iboard.ssi.com.vn/analysis/fundamental-analysis", "0373416708", "Lt251208@#$")
    # chuyển vào iframe
    switch_to_analysis_iframe(driver)    
    
    # chọn xem theo quý
    select_option_Xpath(driver, "//button[contains(@class, 'dropdown-toggle') and @title='Năm']") 
    select_option_Xpath(driver, "//div[contains(@class, 'scrollbars')]//a[@title='Quý']" )

    # chọn xem theo 1 cột
    select_option_Xpath(driver, "(//div[contains(@class,'list-filter')]//button)[3]") 
    select_option_Xpath(driver, "//div[contains(@class, 'scrollbars')]//a[@title='1']" )
 

    Total_Balance = pd.DataFrame()
    Total_Income = pd.DataFrame()
    Total_CashFlow = pd.DataFrame()

    for idx, stock_code in enumerate(stocks, 1):

        enter_stock_code(driver, stock_code)

        # Tương tự cho "Kết Quả Kinh Doanh"
        try:
            Income = get_total_financial_new_data(driver, "Kết Quả Kinh Doanh", stock_code)
            if isinstance(Income, pd.DataFrame): 
                Total_Income = pd.concat([Total_Income, Income], ignore_index=True)
            else:
                last_stocks.add(Income)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Kết Quả Kinh Doanh' cho mã {stock_code}: {e}")

        # Lưu chuyển tiền tệ
        try:
            CashFlow = get_total_financial_new_data(driver, "Lưu Chuyển Tiền Tệ", stock_code)
            if isinstance(CashFlow, pd.DataFrame): 
                Total_CashFlow = pd.concat([Total_CashFlow, CashFlow], ignore_index=True)
            else:
                last_stocks.add(CashFlow)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Lưu Chuyển Tiền Tệ' cho mã {stock_code}: {e}")

        # Crawl dữ liệu "Cân Đối Kế Toán"
        try:
            Balance = get_total_financial_new_data(driver, "Cân Đối Kế Toán", stock_code)
            if isinstance(Balance, pd.DataFrame): 
                Total_Balance = pd.concat([Total_Balance, Balance], ignore_index=True)
            else:
                last_stocks.add(Balance)
        except Exception as e:
            print(f"Lỗi khi crawl dữ liệu 'Cân Đối Kế Toán' cho mã {stock_code}: {e}")

        print(f"Mã {stock_code} đã được xử lý")


        # Lưu vào file sau mỗi 5 mã chứng khoán
        if idx % 5 == 0:
            Total_Balance.to_csv("/opt/Tasks/extract/NewData/Total_Balance_1.csv", index=False)
            Total_Income.to_csv("/opt/Tasks/extract/NewData/Total_Income_1.csv", index=False)
            Total_CashFlow.to_csv("/opt/Tasks/extract/NewData/Total_CashFlow_1.csv", index=False)
            print(f"Đã lưu dữ liệu sau {idx} mã chứng khoán.")

    # Lưu vào file sau khi hoàn thành tất cả

    Total_Balance = Total_Balance.drop_duplicates()
    Total_Income = Total_Income.drop_duplicates()
    Total_CashFlow = Total_CashFlow.drop_duplicates()
    
    Total_Balance["Status"] = "New"
    Total_Income["Status"] = "New"
    Total_CashFlow["Status"] = "New"
    Total_Balance.to_csv("/opt/Tasks/extract/NewData/Total_Balance_1.csv", index=False)
    Total_Income.to_csv("/opt/Tasks/extract/NewData/Total_Income_1.csv", index=False)
    Total_CashFlow.to_csv("/opt/Tasks/extract/NewData/Total_CashFlow_1.csv", index=False)
    # lưu lại các mã lần sau crawl:

    with open("/opt/Tasks/extract/NewData/next_stocks.txt", 'w') as file:
        for stock in last_stocks:
            file.write(stock + '\n')


    print("Lấy data báo cáo tài chính thành công")

if __name__ == "__main__":
    main_report_new_1()




