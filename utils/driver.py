import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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