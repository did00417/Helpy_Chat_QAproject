import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils import (
    get_wait,
    clear_session,
    log_test_start,
    log_test_success,
    log_test_failure,
    save_screenshot,
)


# TC-ME-001
def test_login_success(driver):
    test_name = "로그인 정상 동작 테스트"

    login_page = LoginPage(driver)

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
        login_page.input_username(TEST_LOGIN_ID)
        login_page.input_password(TEST_LOGIN_PASSWORD)
        login_page.click_login_button()

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


# TC-ME-005
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

        login_page = LoginPage(driver)

        login_page.input_username(wrong_email)
        login_page.input_password(TEST_LOGIN_PASSWORD)
        login_page.click_login_button()

        # -----------------------------------
        # 4) 오류 메시지 노출 확인
        # -----------------------------------
        error_message = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Invalid email format')]")
            )
        )

        assert (
            "Invalid email format" in error_message.text
        ), "Invalid email format 오류 메시지가 표시되지 않았음"

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


# TC-ME-003
def test_login_wrong_password(driver):
    test_name = "잘못된 비밀번호 로그인 실패 테스트"
    start = time.time()
    log_test_start(test_name)

    try:
        wait = get_wait(driver)
        login_page = LoginPage(driver)

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
        wrong_pw = "wrongPassword123"

        # 이메일 입력
        login_page.input_username(TEST_LOGIN_ID)
        # 비밀번호(잘못된 값) 입력
        login_page.input_password(wrong_pw)
        login_page.click_login_button()

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
