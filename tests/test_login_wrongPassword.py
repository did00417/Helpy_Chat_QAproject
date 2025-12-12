#TC-ME-003

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


def test_login_wrong_password(driver):
    test_name = "잘못된 비밀번호 로그인 실패 테스트"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 로그인 페이지 로드
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
        # 3) 잘못된 비밀번호로 로그인 시도
        # -----------------------------------
        email = "qa3team0501@elicer.com"
        wrong_pw = "wrongPassword123"

        # 이메일 입력
        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "loginId"))
        )
        email_input.clear()
        email_input.send_keys(email)

        # 비밀번호(잘못된 값) 입력
        pw_input = driver.find_element(By.NAME, "password")
        pw_input.clear()
        pw_input.send_keys(wrong_pw)

        # 로그인 버튼 클릭
        login_btn = driver.find_element(By.XPATH, "//button[text()='Login']")
        login_btn.click()

        # -----------------------------------
        # 4) 에러 메시지 검증
        # -----------------------------------
        error_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Email or password does not match')]")
            )
        )

        assert error_element.is_displayed(), "에러 문구가 표시되지 않았습니다."

        # -----------------------------------
        # 5) 테스트 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, test_name)  # 실패 시 스크린샷
