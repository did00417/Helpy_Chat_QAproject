#TC-ME-005

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


def test_login_wrong_email_format(driver):
    test_name = "이메일 형식 오류(Invalid email format) 노출 테스트"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 로그인 페이지 이동
        # -----------------------------------
        driver.get("https://qaproject.elice.io/ai-helpy-chat")
        driver.maximize_window()
        time.sleep(1)

        # -----------------------------------
        # 2) 세션 초기화
        # -----------------------------------
        clear_session(driver)
        time.sleep(1)

        # -----------------------------------
        # 3) 잘못된 이메일 형식 입력 (@, . 없음)
        # -----------------------------------
        wrong_email = "wrongemail"
        password = "team05fighting!"

        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "loginId"))
        )
        email_input.clear()
        email_input.send_keys(wrong_email)

        pw_input = driver.find_element(By.NAME, "password")
        pw_input.clear()
        pw_input.send_keys(password)

        # 로그인 버튼 클릭
        login_btn = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
        login_btn.click()

        # -----------------------------------
        # 4) 오류 메시지 노출 확인
        # -----------------------------------
        error_message = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Invalid email format')]")
            )
        )

        assert "Invalid email format" in error_message.text, \
            "Invalid email format 오류 메시지가 표시되지 않았음"

        # -----------------------------------
        # 5) 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, test_name)
        log_test_failure(test_name, str(e), duration)
        raise e
