from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver(chrome_url):
    # Khởi tạo tùy chọn cho Chrome
    chrome_options = Options()
    
    # Tùy chọn giúp tăng độ ổn định khi chạy trong Docker:
    chrome_options.add_argument("--no-sandbox")  # Vô hiệu hóa sandbox để tránh lỗi khi chạy trong container.
    chrome_options.add_argument("--disable-dev-shm-usage")  # Sử dụng bộ nhớ tạm thay vì shared memory (giảm lỗi bộ nhớ).
    # Thiết lập giao diện trình duyệt
    chrome_options.add_argument("--window-size=1920,1080")  # Đặt kích thước cửa sổ trình duyệt cố định (giả lập desktop).
    
    # Tùy chọn để tránh bị phát hiện là bot tự động:
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Ẩn trạng thái "automation".
    chrome_options.add_experimental_option("useAutomationExtension", False)  # Tắt extension tự động của Selenium.
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Vô hiệu hóa một số đặc điểm của Blink Engine.
    
    # Cài đặt chế độ "headless":
    chrome_options.add_argument("--headless=new")  # Chạy trong chế độ không giao diện (headless).
    
    # Thêm user-agent để giả lập trình duyệt người dùng thực:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")  # Đặt user-agent để trình duyệt giống với người dùng thực.
    
    # Tùy chọn khác:
    chrome_options.add_argument("--disable-extensions")  # Vô hiệu hóa các tiện ích mở rộng không cần thiết.
    chrome_options.add_argument("--disable-gpu")  # Tắt GPU (thường không cần thiết trong chế độ headless).
    
    # Cài đặt sở thích (preferences):
    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Tắt tải hình ảnh.
        "profile.managed_default_content_settings.fonts": 2,   # Tắt tải font.
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Khởi tạo Selenium WebDriver để kết nối đến Selenium Server trên container:
    driver = webdriver.Remote(
        command_executor=chrome_url,  # Địa chỉ Selenium Server trong container.
        options=chrome_options  # Truyền các tùy chọn Chrome đã thiết lập.
    )
    return driver  # Trả về đối tượng WebDriver.
