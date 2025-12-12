#TC-ME-009

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session, wait_for_error_message,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


def test_signup_registered_email(driver):
    test_name = "회원가입 - 이미 가입된 이메일 입력 시 에러 메시지 확인"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 페이지 이동 및 세션 초기화
        # -----------------------------------
        driver.get("https://qaproject.elice.io/ai-helpy-chat")
        driver.maximize_window()
        time.sleep(1)

        clear_session(driver)
        time.sleep(1)

        # -----------------------------------
        # 2) Create account 클릭
        # -----------------------------------
        create_account = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Create account')]"))
        )
        create_account.click()

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
        # 4) 이미 가입된 이메일 입력
        # -----------------------------------
        registered_email = "qa3team05@elicer.com"

        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "loginId"))
        )
        email_input.clear()
        email_input.send_keys(registered_email)

        # -----------------------------------
        # 5) 에러 메시지 확인
        # -----------------------------------
        error_msg = wait_for_error_message(
            driver,
            "This is an already registered email address"
        )

        assert "This is an already registered email address" in error_msg.text, \
            "이미 등록된 이메일임에도 오류 메시지가 표시되지 않음"

        # OPTIONAL: Create account 버튼이 비활성화인지 확인
        create_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create account')]")
            )
        )
        assert create_btn.get_attribute("disabled") is not None, \
            "이미 등록된 이메일인데도 Create account 버튼이 비활성화되지 않음"

        # -----------------------------------
        # 6) 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, "signup_registered_email_fail")
        log_test_failure(test_name, str(e), duration)
        raise e
