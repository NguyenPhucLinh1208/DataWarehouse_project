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