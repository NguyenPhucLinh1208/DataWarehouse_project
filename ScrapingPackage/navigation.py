from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# trong cấu trúc trang web này có iframe,cần chuyển vào iframe đó để crawl data.
def switch_to_analysis_iframe(driver):
    iframe = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'https://fiin-app.ssi.com.vn/screen/fundamental')]"))
    )
    driver.switch_to.frame(iframe)
    
# Chờ cho phần tử có thể click, sử dụng Xpath để xác định phần tử
def select_option_Xpath(driver, option_xpath):
    option = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, option_xpath))
    )
    option.click()

def select_option_CSS_SELECTOR(driver, option_css):
    option = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, option_css))
    )
    option.click()