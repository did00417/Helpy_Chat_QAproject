#TC-ME-011

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    get_wait, clear_session,
    log_test_start, log_test_success, log_test_failure, save_screenshot
)


def test_signup_agree_required_checkboxes(driver):
    test_name = "회원가입 - 필수 체크 미완료 시 버튼 비활성화 확인"
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
        # 4) 이메일 / 비밀번호 / 이름 입력
        # -----------------------------------
        wait.until(EC.visibility_of_element_located((By.NAME, "loginId"))).send_keys("test_mem@mail.com")
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys("Testtest1!")
        wait.until(EC.visibility_of_element_located((By.NAME, "fullname"))).send_keys("testuser")

        # -----------------------------------
        # 5) 약관 아코디언 펼치기
        # -----------------------------------
        try:
            expand_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//svg[@data-icon='chevron-down']")
                )
            )
            expand_btn.click()
        except:
            pass  # 이미 열려 있다면 패스

        # -----------------------------------
        # 6) 체크박스 선택 (필수 중 일부만 선택)
        # -----------------------------------
        # 필수 체크 1: 나는 14세 이상입니다 ← 클릭
        age_checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()=\"I'm 14 years or older.\"]]")
            )
        )
        age_checkbox.click()

        # Optional 체크박스 선택 (의무 아님)
        optional_checkbox = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()='[Optional] Receive updates and promotional emails.']]")
            )
        )
        optional_checkbox.click()

        # ⚠ "Agree All" 과 "필수 이용약관 동의" 등을 일부러 클릭하지 않음
        # → 이 상태에서 버튼이 활성화되면 안 됨

        # -----------------------------------
        # 7) Create account 버튼 disabled 확인
        # -----------------------------------
        create_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create account')]")
            )
        )

        assert create_btn.get_attribute("disabled") is not None, \
            "필수 약관 동의를 모두 하지 않았는데 Create account 버튼이 활성화되어 있음"

        # -----------------------------------
        # 8) 성공 처리
        # -----------------------------------
        duration = time.time() - start
        log_test_success(test_name, duration)

    except Exception as e:
        duration = time.time() - start
        save_screenshot(driver, "signup_agree_required_fail")
        log_test_failure(test_name, str(e), duration)
        raise e
