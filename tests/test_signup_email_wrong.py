#TC-ME-007

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session, wait_for_error_message,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


# 잘못된 이메일 테스트 데이터
invalid_emails = [
    "홍길동@gmail.com",
    "@#$@gmail.com",
    "漢子@gmail.com",
    "test.gmail@com",
]


@pytest.mark.parametrize("email", invalid_emails)
def test_signup_invalid_email(driver, email):
    test_name = f"회원가입 - 잘못된 이메일 형식 테스트 ({email})"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 회원가입 페이지 이동
        # -----------------------------------
        driver.get("https://qaproject.elice.io/ai-helpy-chat")
        driver.maximize_window()
        time.sleep(1)

        clear_session(driver)
        time.sleep(1)

        # -----------------------------------
        # 2) Create Account 클릭
        # -----------------------------------
        create_account_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Create account')]"))
        )
        create_account_btn.click()

        # -----------------------------------
        # 3) Create account with email 클릭
        # -----------------------------------
        create_email_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Create account with email')]")
            )
        )
        create_email_btn.click()

        # -----------------------------------
        # 4) 이메일 입력
        # -----------------------------------
        login_id = wait.until(
            EC.visibility_of_element_located((By.NAME, "loginId"))
        )
        login_id.clear()
        login_id.send_keys(email)

        # -----------------------------------
        # 5) 이메일 형식 오류 메시지 확인
        # -----------------------------------
        error_msg = wait_for_error_message(driver, "Email address is incorrect")

        assert "Email address is incorrect" in error_msg.text, \
            f"잘못된 이메일 '{email}'에 대해 오류 메시지가 표시되지 않음"

        # -----------------------------------
        # 6) 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, f"signup_invalid_email_{email}")
        log_test_failure(test_name, str(e), duration)
        raise e
