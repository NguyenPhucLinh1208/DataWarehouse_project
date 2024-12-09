from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ScrapingPackage.navigation import select_option_Xpath

def login(driver, url, username, password):

    driver.get(url)
    # click vào nút đăng nhập
    select_option_Xpath(driver, "//button[text()='Đăng nhập']")
    # Đăng nhập
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "txt-username"))
    )
    username_input.clear()
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "txt-password"))
    )
    password_input.clear()
    password_input.send_keys(password)
    # click vào nút đăng nhập
    select_option_Xpath(driver, "//button[text()='Đăng nhập']")

