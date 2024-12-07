import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from ScrapingPackage.navigation import select_option_Xpath


def get_hosocongty_data(driver, info):

    CompData = []
    select_option_Xpath(driver, f"//button[text()='{info}']")
    # Lấy dữ liệu với 3 lần thử
    for _ in range(3):
        try:
            company_info_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'company-basic-info'))
            )
            for info in company_info_elements:
                text_elements = info.find_elements(By.CLASS_NAME, 'text-color-tertiary')
                #láy phần tử thứ 2 trên hàng
                if len(text_elements) == 2:
                    value = text_elements[1].text.strip()
                    CompData.append(value)
            break  # Thoát vòng lặp nếu thành công
        except Exception:
            time.sleep(1)  # Chờ một chút trước khi thử lại
    return CompData


def enter_stock_code(driver, stock_code):

    # tìm nơi điền mã
    stock_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ticker[contenteditable='true']"))
    )
    # xóa nội dung cũ
    stock_input.send_keys(Keys.CONTROL + "a")
    stock_input.send_keys(Keys.BACKSPACE)
    stock_input.send_keys(stock_code)

    # sau khi điền, sẽ xuất hiện một menu lựa chọn, cần chờ nó xuất hiện rồi ấn Enter
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.scrollbars").is_displayed())
    stock_input.send_keys(Keys.RETURN)
    
    # sẽ có độ trễ do tải, lúc này, sẽ xuất hiện icon mô tả đang tải, cần chờ nó biến mất
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-spinner"))
    )

def scrape_data_report(driver):
    """
    Hàm thực hiện crawl data trên 1 trang giao diện, tại một thời điểm.
    """
    total_col_names, row_datas = [], []

    # Lấy giá trị tên cột, được đánh dấu trong thẻ thead
    WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, "//thead")))
    # lấy phần tử span trong thẻ thead
    col_names = driver.find_elements(By.XPATH, "//thead//th//span")
    # Lấy tên cột, loại bỏ khoảng trống
    total_col_names = [col.text.strip() for col in col_names if col.text.strip()]  
    # Không có dữ liệu, return
    if not total_col_names:
        return None
    
    # Nếu có dữ liệu, tiến hành crawl các hàng, nằm trong thẻ body
    rows = WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody//tr")))[1:]
    row_datas = [
        [value.text.strip() for value in row.find_elements(By.XPATH, ".//td") if value.text.strip()]
        for row in rows if row.text.strip()
    ]

    Table = pd.DataFrame(row_datas, columns=total_col_names)
    Table_long = pd.melt(Table, id_vars=["CHỈ TIÊU"], var_name="THỜI GIAN", value_name="GIÁ TRỊ")
    return Table_long

def get_financial_data(driver, stock_code, year):

    # Lấy dữ liệu cho từng khoảng thời gian
    select_option_Xpath(driver, "(//div[contains(@class,'list-filter')]//button)[2]")
    select_option_Xpath(driver, f"//div[contains(@class, 'scrollbars')]//a[@title='{year}']")
    df_financial_data = scrape_data_report(driver)
    if df_financial_data is not None:
        df_financial_data["Mã Chứng Khoán"] = stock_code

    return df_financial_data

def get_total_financial_data(driver, report_type, stock_code):
    """
    Lấy dữ liệu của nhiều kì báo cáo
    """
    Total_report = pd.DataFrame()
    select_option_Xpath(driver, f"//li[@class='nav-item m-tabs__item']//a[.//span[text()='{report_type}']]")
    WebDriverWait(driver, 10, poll_frequency=0.1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-spinner")))

    missing_years = None
    skip = False  # Biến kiểm tra để bỏ qua các năm sau nếu cần

    report1 = get_financial_data(driver, stock_code, "2024")
    if report1 is not None:
        Total_report = pd.concat([Total_report, report1], ignore_index=True)
    else:
        missing_years = '2024'
        skip = True  # Nếu report1 là None, bỏ qua các lần sau

    if not skip:
        report2 = get_financial_data(driver, stock_code, "2020")
        if report2 is not None:
            Total_report = pd.concat([Total_report, report2], ignore_index=True)
        else:
            missing_years = '2020'
            skip = True

    if not skip:
        report3 = get_financial_data(driver, stock_code, "2017")
        if report3 is not None:
            Total_report = pd.concat([Total_report, report3], ignore_index=True)
        else:
            missing_years = '2017'

    if missing_years:
        print(f"Dữ liệu {report_type} cho mã {stock_code} thiếu từ các năm: {missing_years}.") 

    return Total_report

