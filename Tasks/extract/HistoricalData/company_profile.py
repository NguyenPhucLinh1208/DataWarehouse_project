# export PYTHONPATH=/opt/datawarehouse

import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ScrapingPackage.browser import init_driver
from ScrapingPackage.navigation import select_option_Xpath, select_option_CSS_SELECTOR
from ScrapingPackage.scraper import get_hosocongty_data

def main_hosocongty():

    with open("Tasks/extract/HistoricalData/MaCks.txt", "r") as f:
        MaCks = [line.strip() for line in f]
    
    # Khởi tạo trình duyệt
    driver = init_driver("http://chrome:4444/wd/hub")
    driver.get("https://iboard.ssi.com.vn/")

    ComDatas = []

    # click vào mã chứng khoán đầu tiên xuất hiện, bất kì.
    select_option_CSS_SELECTOR(driver,  'div.ag-cell.stock-symbol[col-id="stockSymbol"]')

    # click vào mục Hồ Sơ
    select_option_Xpath(driver, "//a[text()='Hồ sơ']")

    for MaCK in MaCks:
        # Tìm vị trí để nhập các mã chứng khoán
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "downshift-3-input"))
        )
        # Thao tác xóa và nhập giá trị mới
        input_element.send_keys(Keys.CONTROL + "a") # bôi đen
        input_element.send_keys(Keys.BACKSPACE) # xóa
        input_element.send_keys(MaCK) # nhập mã chứng khoán
        input_element.send_keys(Keys.RETURN) # enter

        # Lấy tên công ty
        nameComp = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flex-none.font-bold.pt-1"))
        )
        nameComp = [nameComp.text.strip()]        

        # lấy thông tin cơ bản
        TTCoBanData = get_hosocongty_data(driver, "TT cơ bản")
        # lấy thông tin niêm yết
        TTNiemYet = get_hosocongty_data(driver, "TT niêm yết")
        ComData = nameComp + TTCoBanData + TTNiemYet

        ComDatas.append(ComData)
    driver.quit()
    return ComDatas

if __name__ == "__main__":

    column_names = [
    'Tên công ty', 'Mã SIC', 'Tên ngành', 'Mã ngành ICB', 'Năm thành lập', 'Vốn điều lệ', 
    'Số lượng nhân viên', 'Số lượng chi nhánh', 'Ngày niêm yết', 'Nơi niêm yết', 
    'Giá chào sàn (x1000)', 'KL đang niêm yết', 'Thị giá vốn', 'SLCP lưu hành'
    ]

    ComDatas = main_hosocongty()
    company_info = pd.DataFrame(ComDatas, columns = column_names)
    company_info.to_csv("/opt/datawarehouse/Tasks/extract/HistoricalData/company_info.csv", index=False)

    print("Lấy data Hồ Sơ Công Ty thành công")
        



        

