import time
from datetime import datetime
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
    WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CSS_SELECTOR, "div.scrollbars").is_displayed())
    stock_input.send_keys(Keys.RETURN)
    
    # sẽ có độ trễ do tải, lúc này, sẽ xuất hiện icon mô tả đang tải, cần chờ nó biến mất
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-spinner"))
    )

def scrape_data_report(driver, report_type):
    """
    Hàm thực hiện crawl data trên 1 trang giao diện, tại một thời điểm.
    """
    total_col_names, row_datas = [], []

    # Lấy giá trị tên cột, được đánh dấu trong thẻ thead
    WebDriverWait(driver, 45, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, "//thead")))
    # lấy phần tử span trong thẻ thead
    col_names = driver.find_elements(By.XPATH, "//thead//tr//th//span")
    # Lấy tên cột, loại bỏ khoảng trống
    total_col_names = [col.text.strip() for col in col_names if col.text.strip()]  
    # Không có dữ liệu, return
    if not total_col_names:
        return None

    # Nếu có dữ liệu, tiến hành crawl các hàng, nằm trong thẻ tbody
    rows_xpath = "//tbody//tr"
    if report_type == "Cân Đối Kế Toán":
        rows = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_all_elements_located((By.XPATH, rows_xpath)))[1:]
    else:
        rows = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_all_elements_located((By.XPATH, rows_xpath)))

    row_datas = [
        [value.text.strip() for value in row.find_elements(By.XPATH, ".//td") if value.text.strip()]
        for row in rows if row.text.strip()
    ]

    Table = pd.DataFrame(row_datas, columns=total_col_names)
    Table_long = pd.melt(Table, id_vars=["CHỈ TIÊU"], var_name="THỜI GIAN", value_name="GIÁ TRỊ")
    return Table_long


def get_financial_data(driver, stock_code, year, report_type):
    # Lấy dữ liệu cho từng khoảng thời gian
    select_option_Xpath(driver, "(//div[contains(@class,'list-filter')]//button)[2]")
    # Chờ phần tử tồn tại trong DOM
    option = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'scrollbars')]//a[@title='{year}']"))
    )
    # Cuộn đến phần tử bằng JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", option)
    select_option_Xpath(driver, f"//div[contains(@class, 'scrollbars')]//a[@title='{year}']")
    df_financial_data = scrape_data_report(driver, report_type)
    if df_financial_data is None:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='no-data']/span[text()='Dữ liệu đang cập nhật']")))
        except:
            print(f"Trang năm {year} của mã {stock_code} chưa được load hết")
    else:
        df_financial_data["Mã Chứng Khoán"] = stock_code

    return df_financial_data


def get_total_financial_data(driver, report_type, stock_code):
    """
    Lấy dữ liệu của nhiều kì báo cáo
    """
    Total_report = pd.DataFrame()
    select_option_Xpath(driver, f"//li[@class='nav-item m-tabs__item']//a[.//span[text()='{report_type}']]")
    WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-spinner")))

    missing_years = None
    years = ["2024", "2020", "2017"]

    for year in years:
        report = get_financial_data(driver, stock_code, year, report_type)
        if report is not None:
            Total_report = pd.concat([Total_report, report], ignore_index=True)
        else:
            missing_years = year
            break

    if missing_years:
        print(f"Dữ liệu {report_type} cho mã {stock_code} thiếu từ các năm: {missing_years}.") 

    return Total_report


def scrape_new_data_report(driver, report_type):
    """
    Hàm thực hiện crawl data trên 1 trang giao diện, tại một thời điểm.
    """
    total_col_names, row_datas = [], []

    # Lấy ngày hiện tại
    current_date = datetime.now()

    # Xác định quý hiện tại
    if 1 <= current_date.month <= 3:
        latest_report_quarter = f"Q4 {current_date.year - 1}"
    elif 4 <= current_date.month <= 6:
        latest_report_quarter = f"Q1 {current_date.year}"
    elif 7 <= current_date.month <= 9:
        latest_report_quarter = f"Q2 {current_date.year}"
    else:
        latest_report_quarter = f"Q3 {current_date.year}"

    # Lấy giá trị tên cột, được đánh dấu trong thẻ thead
    WebDriverWait(driver, 45, poll_frequency=0.1).until(EC.presence_of_element_located((By.XPATH, "//thead")))
    # lấy phần tử span trong thẻ thead
    col_names = driver.find_elements(By.XPATH, "//thead//tr//th//span")
    # Lấy tên cột, loại bỏ khoảng trống
    total_col_names = [col.text.strip() for col in col_names if col.text.strip()]  
    # Không có dữ liệu, return
    if not total_col_names:
        print("Lỗi khi tải trang hoặc không có dữ liệu")
        return pd.DataFrame()

    # Nếu có dữ liệu, nhưng nó không phải là dữ liệu mới nhất
    if total_col_names[1] != latest_report_quarter:
        print("Dữ liệu mới nhất chưa được cập nhật")
        return pd.DataFrame()

    # Tiến hành crawl các hàng, nằm trong thẻ tbody
    rows_xpath = "//tbody//tr"
    if report_type == "Cân Đối Kế Toán":
        rows = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_all_elements_located((By.XPATH, rows_xpath)))[1:]
    else:
        rows = WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.presence_of_all_elements_located((By.XPATH, rows_xpath)))

    row_datas = [
        [value.text.strip() for value in row.find_elements(By.XPATH, ".//td") if value.text.strip()]
        for row in rows if row.text.strip()
    ]

    Table = pd.DataFrame(row_datas, columns=total_col_names)
    Table_long = pd.melt(Table, id_vars=["CHỈ TIÊU"], var_name="THỜI GIAN", value_name="GIÁ TRỊ")
    return Table_long


def get_total_financial_new_data(driver, report_type, stock_code):
    """
    Lấy dữ liệu tài chính cho một hoặc nhiều loại báo cáo.
    """
    Total_report = pd.DataFrame()

    # Chọn báo cáo theo loại
    select_option_Xpath(driver, f"//li[@class='nav-item m-tabs__item']//a[.//span[text()='{report_type}']]")
    WebDriverWait(driver, 30, poll_frequency=0.1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loading-spinner")))

    # Scrape dữ liệu báo cáo
    df_financial_data = scrape_new_data_report(driver, report_type)
    
    # Kiểm tra số hàng của df_financial_data
    if df_financial_data.empty:
        return stock_code
    
    # Nếu có dữ liệu hợp lệ, gán mã chứng khoán và thêm vào DataFrame
    df_financial_data["Mã Chứng Khoán"] = stock_code
    Total_report = pd.concat([Total_report, df_financial_data], ignore_index=True)

    return Total_report

