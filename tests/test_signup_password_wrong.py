#TC-ME-008
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session, wait_for_error_message,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)

# 잘못된 비밀번호 테스트 데이터
invalid_passwords = [
    "12345678",
    "abcdefgh",
    # 아래 케이스도 필요하면 활성화 가능
    # "Abcdefg",
    # "Abcdefg@",
    # "Abcdefg2",
]


@pytest.mark.parametrize("password", invalid_passwords)
def test_signup_invalid_password(driver, password):
    test_name = f"회원가입 - 잘못된 비밀번호 조건 테스트 ({password})"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)

        # -----------------------------------
        # 1) 페이지 이동 & 세션 초기화
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
            EC.element_to_be_clickable((By.LINK_TEXT, "Create account"))
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
        # 4) 이메일 입력
        # -----------------------------------
        email_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Email']")
            )
        )
        email_input.clear()
        email_input.send_keys("test123@naver.com")

        # -----------------------------------
        # 5) 비밀번호 입력 (조건 불충족 값)
        # -----------------------------------
        password_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Password']")
            )
        )
        password_input.clear()
        password_input.send_keys(password)

        # -----------------------------------
        # 6) 비밀번호 에러 문구 확인
        # -----------------------------------
        error_msg = wait_for_error_message(
            driver,
            "Please make your password stronger!"
        )

        assert "Please make your password stronger!" in error_msg.text, \
            "비밀번호 규칙 오류 메시지가 표시되지 않음"

        # -----------------------------------
        # 7) Create account 버튼 disabled 상태 확인
        # -----------------------------------
        create_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create account')]")
            )
        )

        assert create_btn.get_attribute("disabled") is not None, \
            "비밀번호 규칙 미충족인데도 Create account 버튼이 비활성화되지 않음"

        # -----------------------------------
        # 8) 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, f"signup_invalid_password_{password}")
        log_test_failure(test_name, str(e), duration)
        raise e
