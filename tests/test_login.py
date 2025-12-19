import time #테스트에 걸린 시간
from selenium.webdriver.common.by import By #selenium 요고 찾을 때 쓰는
from selenium.webdriver.support import expected_conditions as EC #expected conditions 조건이 나타날때까지 기다려라 
from pages.login_page import LoginPage 
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_wait #get_driver fixture 사용하고 있기 때문에 쓰지 않아도 괜찮음
from utils.helper import (
    BASE_URL,
    clear_session, #쿠키/세션/스토리 지우기
    log_test_start, #테스트 시작
    log_test_failure, #실패 로그
    log_test_success, #성공 
    wait_for_error_message,
    save_screenshot #실패 시 스크린샷 
    #clear_session #중복 제거해도 괜찮음
    )

# ============================
# 테스트 케이스 : TC-ME-001
# 테스트 내용 : 로그인 성공
# ============================

def test_login_success(driver):
    test_name = "로그인 정상 동작 테스트 (POM)"
    log_test_start(test_name)

    driver.get(BASE_URL) 
    driver.maximize_window()
    time.sleep(1)

    clear_session(driver)
    time.sleep(1)

    wait = get_wait(driver)

    login_page = LoginPage(driver) #POM 객체 생성
    login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )

    wait.until(EC.url_contains("/ai-helpy-chat")) #"/ai-helpy-chat" 나올 때까지 기달리기
    assert "/ai-helpy-chat" in driver.current_url, \
        "로그인 후 메인 페이지로 이동하지 못했습니다." #진짜로 이동했는지 확인 

    print("✅ 로그인 성공")


# ==================================
# 테스트 케이스 :TC-ME-005
# 테스트 내용 : 이메일 형식 오류 
# ==================================

def test_login_wrong_email_format(driver):
    test_name = "이메일 형식 오류 노출 테스트 (POM)"
    log_test_start(test_name)

    driver.get(BASE_URL)
    driver.maximize_window()
    time.sleep(1)

    clear_session(driver)
    time.sleep(1)

    login_page = LoginPage(driver)
    login_page.login(
        email="wrongemail",               # ❌ @, . 없는 형식
        password=TEST_LOGIN_PASSWORD
    )

    error = wait_for_error_message(driver, "Invalid email format")
    assert "Invalid email format" in error.text, \
        "이메일 형식 오류 메시지가 노출되지 않았습니다."

    print("✅ 이메일 형식 오류 시 에러 메시지 정상 노출")


# ==================================
# 테스트 케이스 :TC-ME-003
# 테스트 내용 : 비밀번호 형식 오류 
# ==================================

def test_login_wrong_password(driver):
    test_name = "TC-ME-003 | 정상 이메일 + 잘못된 비밀번호"
    log_test_start(test_name)

    driver.get(BASE_URL)
    driver.maximize_window()
    time.sleep(1)

    clear_session(driver)
    time.sleep(1)

    login_page = LoginPage(driver)
    login_page.login(
        email=TEST_LOGIN_ID,       # ✅ 정상 이메일 (helper)
        password="wrongPassword123"   # ❌ 잘못된 비밀번호
    )
    error = wait_for_error_message(driver, "Email or password does not match")
    assert "Email or password does not match" in error.text
    
    print("✅ 비밀번호 형식 오류 시 에러 메시지 정상 노출")






























# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from pages.login_page import LoginPage
# from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
# from utils.driver import get_driver , get_wait
# from utils.helper import (
#     clear_session,
#     log_test_start,
#     log_test_failure,
#     log_test_success,
#     save_screenshot,
#     clear_session
#     )


# # TC-ME-001
# def test_login_success(driver):
#     test_name = "로그인 정상 동작 테스트"

#     login_page = LoginPage(driver)

#     start = time.time()
#     log_test_start(test_name)

#     try:
#         wait = get_wait(driver)

#         # -----------------------------------
#         # 1) 로그인 페이지 먼저 열기 (중요!)
#         # -----------------------------------
#         driver.get("https://qaproject.elice.io/ai-helpy-chat")
#         driver.maximize_window()
#         time.sleep(1)

#         # -----------------------------------
#         # 2) 이제 세션 초기화 (localStorage 접근 가능)
#         # -----------------------------------
#         clear_session(driver)
#         time.sleep(1)

#         # -----------------------------------
#         # 3) 로그인 정보 입력
#         # -----------------------------------
#         login_page.input_username(TEST_LOGIN_ID)
#         login_page.input_password(TEST_LOGIN_PASSWORD)
#         login_page.click_login_button()

#         # -----------------------------------
#         # 4) 로그인 성공 검증
#         # -----------------------------------
#         wait.until(EC.url_contains("/ai-helpy-chat"))
#         assert "/ai-helpy-chat" in driver.current_url, "로그인 후 페이지 이동 실패"

#         duration = time.time() - start
#         log_test_success(test_name, duration)

#     except Exception as e:
#         duration = time.time() - start
#         save_screenshot(driver, test_name)
#         log_test_failure(test_name, str(e), duration)
#         raise e


# # TC-ME-005
# def test_login_wrong_email_format(driver):
#     test_name = "이메일 형식 오류(Invalid email format) 노출 테스트"
#     start = time.time()
#     log_test_start(test_name)

#     try:
#         wait = get_wait(driver)

#         # -----------------------------------
#         # 1) 로그인 페이지 이동
#         # -----------------------------------
#         driver.get("https://qaproject.elice.io/ai-helpy-chat")
#         driver.maximize_window()
#         time.sleep(1)

#         # -----------------------------------
#         # 2) 세션 초기화
#         # -----------------------------------
#         clear_session(driver)
#         time.sleep(1)

#         # -----------------------------------
#         # 3) 잘못된 이메일 형식 입력 (@, . 없음)
#         # -----------------------------------
#         wrong_email = "wrongemail"

#         login_page = LoginPage(driver)

#         login_page.input_username(wrong_email)
#         login_page.input_password(TEST_LOGIN_PASSWORD)
#         login_page.click_login_button()

#         # -----------------------------------
#         # 4) 오류 메시지 노출 확인
#         # -----------------------------------
#         error_message = wait.until(
#             EC.visibility_of_element_located(
#                 (By.XPATH, "//*[contains(text(), 'Invalid email format')]")
#             )
#         )

#         assert (
#             "Invalid email format" in error_message.text
#         ), "Invalid email format 오류 메시지가 표시되지 않았음"

#         # -----------------------------------
#         # 5) 성공 처리
#         # -----------------------------------
#         duration = time.time() - start
#         log_test_success(test_name, duration)

#     except Exception as e:
#         duration = time.time() - start
#         save_screenshot(driver, test_name)
#         log_test_failure(test_name, str(e), duration)
#         raise e


# # TC-ME-003
# def test_login_wrong_password(driver):
#     test_name = "잘못된 비밀번호 로그인 실패 테스트"
#     start = time.time()
#     log_test_start(test_name)

#     try:
#         wait = get_wait(driver)
#         login_page = LoginPage(driver)

#         # -----------------------------------
#         # 1) 로그인 페이지 로드
#         # -----------------------------------
#         driver.get("https://qaproject.elice.io/ai-helpy-chat")
#         driver.maximize_window()
#         time.sleep(1)

#         # -----------------------------------
#         # 2) 세션 초기화
#         # -----------------------------------
#         clear_session(driver)
#         time.sleep(1)

#         # -----------------------------------
#         # 3) 잘못된 비밀번호로 로그인 시도
#         # -----------------------------------
#         wrong_pw = "wrongPassword123"

#         # 이메일 입력
#         login_page.input_username(TEST_LOGIN_ID)
#         # 비밀번호(잘못된 값) 입력
#         login_page.input_password(wrong_pw)
#         login_page.click_login_button()

#         # -----------------------------------
#         # 4) 에러 메시지 검증
#         # -----------------------------------
#         error_element = wait.until(
#             EC.visibility_of_element_located(
#                 (By.XPATH, "//*[contains(text(), 'Email or password does not match')]")
#             )
#         )

#         assert error_element.is_displayed(), "에러 문구가 표시되지 않았습니다."

#         # -----------------------------------
#         # 5) 테스트 성공 처리
#         # -----------------------------------
#         duration = time.time() - start
#         log_test_success(test_name, duration)

#     except Exception as e:
#         duration = time.time() - start
#         save_screenshot(driver, test_name)  # 실패 시 스크린샷
