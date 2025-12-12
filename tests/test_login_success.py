#TC-ME-001

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


def test_login_success(driver):
    test_name = "로그인 정상 동작 테스트"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 로그인 페이지 먼저 열기 (중요!)
        # -----------------------------------
        driver.get("https://qaproject.elice.io/ai-helpy-chat")
        driver.maximize_window()
        time.sleep(1)

        # -----------------------------------
        # 2) 이제 세션 초기화 (localStorage 접근 가능)
        # -----------------------------------
        clear_session(driver)
        time.sleep(1)

        # -----------------------------------
        # 3) 로그인 정보 입력
        # -----------------------------------
        email = "qa3team0501@elicer.com"
        password = "team05fighting!"

        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "loginId"))
        )
        email_input.clear()
        email_input.send_keys(email)

        pw_input = driver.find_element(By.NAME, "password")
        pw_input.clear()
        pw_input.send_keys(password)

        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()

        # -----------------------------------
        # 4) 로그인 성공 검증
        # -----------------------------------
        wait.until(EC.url_contains("/ai-helpy-chat"))
        assert "/ai-helpy-chat" in driver.current_url, "로그인 후 페이지 이동 실패"

        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, test_name)
        log_test_failure(test_name, str(e), duration)
        raise e
