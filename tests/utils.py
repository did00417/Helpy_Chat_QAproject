"""
Unified Utility Functions for Selenium UI Automation

"""

import os
import time
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ================================
# 1) 기본 설정 및 로깅 초기화
# ================================

BASE_URL = os.environ.get("BASE_URL", "https://qaproject.elice.io/ai-helpy-chat")

ROOT_DIR = os.path.dirname(__file__)
SCREENSHOT_DIR = os.path.join(ROOT_DIR, "screenshots")
LOG_DIR = os.path.join(ROOT_DIR, "logs")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 파일 생성
log_file = os.path.join(LOG_DIR, f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def log_test_step(step_name: str):
    """테스트 단계 출력 + 로그 남김"""
    logger.info(f"▶ {step_name}")


def log_test_start(test_name: str):
    """테스트 시작 로그"""
    logger.info("=" * 60)
    logger.info(f"TEST START: {test_name}")
    logger.info("=" * 60)


def log_test_success(test_name: str, duration: float):
    """성공 로그"""
    logger.info(f"✓ PASSED: {test_name} ({duration:.2f}s)")


def log_test_failure(test_name: str, error: str, duration: float):
    """실패 로그"""
    logger.error(f"✗ FAILED: {test_name} ({duration:.2f}s)")
    logger.error(f"  Error: {error}")


# ================================
# 2) WebDriver 관련 기능
# ================================

def get_driver(headless: bool = False):
    """
    WebDriver 생성 통합 함수

    """
    chrome_options = Options()

    # headless 옵션 통합
    if headless or os.environ.get("HEADLESS", "false").lower() == "true":
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    return driver


def get_wait(driver, timeout: int = 10):
    """WebDriverWait 공통 헬퍼"""
    return WebDriverWait(driver, timeout)


def wait_for_url_contains(driver, text: str, timeout: int = 10):
    """URL이 특정 문자열을 포함할 때까지 대기"""
    return get_wait(driver, timeout).until(EC.url_contains(text))


# ================================
# 3) Screenshot 통합 기능
# ================================

def save_screenshot(driver, name: str = "screenshot"):
    """
    스크린샷 저장 통합 함수

    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    logger.info(f"[스크린샷 저장] {path}")
    return path


# ================================
# 4) 로그인/로그아웃 기능
# ================================

LOGIN_URL = (
    "https://accounts.elice.io/accounts/signin/me"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=en-US&org=qaproject"
)

def login(driver, username: str, password: str):
    """
    로그인 공통 처리
    - 기존 utils01 코드 정리
    """
    log_test_step("로그인 페이지로 이동")
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
    wait_for_url_contains(driver, "/")


def logout(driver):
    """
    로그아웃 공통 처리
    - utils01.logout 개선
    """
    log_test_step("로그아웃 실행")
    person_icon = driver.find_element(By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
    logout_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="arrow-right-from-bracketIcon"]')

    person_icon.click()
    logout_btn.click()


# ================================
# 5) 기타 유틸 헬퍼
# ================================

def clear_session(driver):
    """쿠키 + localStorage + sessionStorage 초기화"""
    log_test_step("세션 초기화")
    driver.delete_all_cookies()
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")


def generate_unique_username():
    """테스트용 유니크 아이디 생성"""
    return f"testuser_{int(time.time() * 1000)}"


def open_advanced_menu(headless=False):
    """
    '+' 버튼을 눌러 menu가 열린 상태 반환
    utils02 함수 통합하여 유지
    """
    driver = get_driver(headless)
    wait = get_wait(driver)

    log_test_step("메인 페이지 열기")
    driver.get(BASE_URL)

    log_test_step("플러스 버튼 클릭")
    plus_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="plus"]'))
    )
    plus_btn.click()

    log_test_step("메뉴 활성화 대기")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="menu"]')))

    return driver
