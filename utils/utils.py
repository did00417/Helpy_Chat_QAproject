"""
Utility functions for Selenium UI automation tests.
"""
import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io/ai-helpy-chat")
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")

LOGIN_URL = (
    "https://accounts.elice.io/accounts/signin/me"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=en-US&org=qaproject"
)


# 로그인 처리 공통 함수
def login(driver, username: str, password: str):
    
    print("로그인 페이지로 이동")
    driver.get(LOGIN_URL)

    log_test_step("아이디 입력")
    input_id = driver.find_element(By.NAME, "loginId")
    input_id.clear()
    input_id.send_keys(username)

    log_test_step("비밀번호 입력")
    input_pw = driver.find_element(By.NAME, "password")
    input_pw.clear()
    input_pw.send_keys(password)

    log_test_step("로그인 버튼 클릭")
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    log_test_step("로그인 완료 대기")
    wait_for_url_contains(driver, "/")  # 로그인 후 이동하는 주소에 맞춰 수정


log_file = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def log_test_start(test_name: str):
    """Log the start of a test."""
    logger.info(f"{'='*60}")
    logger.info(f"TEST START: {test_name}")
    logger.info(f"{'='*60}")


def get_driver():
    """Create and return a Chrome WebDriver instance."""
    chrome_options = Options()
    # Set HEADLESS=true for headless mode (default is false for local browser window)
    if os.environ.get("HEADLESS", "false").lower() != "false":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def save_screenshot(driver, name: str):
    """Save a screenshot with timestamp."""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath


def wait_for_element(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be present."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_element_clickable(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be clickable."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_element_visible(driver, test_id: str, timeout: int = 10):
    """Wait for element with data-testid to be visible."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{test_id}"]'))
    )


def wait_for_url_contains(driver, url_part: str, timeout: int = 10):
    """Wait for URL to contain specified string."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.url_contains(url_part))


def get_element_by_testid(driver, test_id: str):
    """Get element by data-testid attribute."""
    return driver.find_element(By.CSS_SELECTOR, f'[data-testid="{test_id}"]')


def click_element(driver, test_id: str):
    """Click element with data-testid."""
    element = wait_for_element_clickable(driver, test_id)
    element.click()
    return element


def type_text(driver, test_id: str, text: str):
    """Type text into element with data-testid."""
    element = wait_for_element(driver, test_id)
    element.clear()
    element.send_keys(text)
    return element


def get_body_class(driver):
    """Get the class attribute of the body element."""
    body = driver.find_element(By.TAG_NAME, "body")
    return body.get_attribute("class") or ""


def generate_unique_username():
    """Generate a unique username for testing."""
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}"


def navigate_to(driver, path: str):
    """Navigate to a specific path."""
    driver.get(f"{BASE_URL}{path}")


def clear_session(driver):
    """Clear all cookies and local storage."""
    driver.delete_all_cookies()
    try:
        driver.execute_script("localStorage.clear();")
        driver.execute_script("sessionStorage.clear();")
    except:
        pass


def log_test_step(step_name: str):
    """Log a test step."""
    logger.info(f"  ▶ {step_name}")


def log_test_success(test_name: str, duration: float):
    """Log test success."""
    logger.info(f"✓ PASSED: {test_name} ({duration:.2f}s)")


def log_test_failure(test_name: str, error: str, duration: float):
    """Log test failure."""
    logger.error(f"✗ FAILED: {test_name} ({duration:.2f}s)")
    logger.error(f"  Error: {error}")
