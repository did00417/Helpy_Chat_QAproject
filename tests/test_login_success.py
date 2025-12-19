# #TC-ME-001

# import time
# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC

# from utils import (
#     get_wait, clear_session,
#     log_test_start, log_test_success, log_test_failure, save_screenshot
# )


# def test_login_success(driver):
#     test_name = "로그인 정상 동작 테스트"
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
#         email = "qa3team0501@elicer.com"
#         password = "team05fighting!"

#         email_input = wait.until(
#             EC.presence_of_element_located((By.NAME, "loginId"))
#         )
#         email_input.clear()
#         email_input.send_keys(email)

#         pw_input = driver.find_element(By.NAME, "password")
#         pw_input.clear()
#         pw_input.send_keys(password)

#         login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
#         login_btn.click()

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




# # 테스트 케이스 : TC-ME-001
# # 로그인 정상 동작 테스트 (Page Object Model)

# import time #테스트에 걸린 시간
# from selenium.webdriver.support import expected_conditions as EC  #expected conditions 조건이 나타날때까지 기다려라 
# #from utils.helper import BASE_URL, clear_session #페이지 진입 시 또 길게 쓰기 번거로워 사용함

# #유틸에서 아래 내용 가져오기! 시간,쿠키/로그인 초기화, 테스트 시작, 성공, 실패
# from utils.helper import (
#     BASE_URL,
#     get_wait,
#     clear_session,
#     log_test_start,
# )

# #로그인 페이지 가져오기
# from pages.login_page import LoginPage

# # 
# def test_login_success(driver):
#     test_name = "로그인 정상 동작 테스트 (POM)"
#     start = time.time()
#     log_test_start(test_name)

#     try:
#         wait = get_wait(driver)

#         # -----------------------------------
#         # 1) 페이지 진입 + 세션 초기화
#         # -----------------------------------
#         #driver.get("https://qaproject.elice.io/ai-helpy-chat")
#         driver.get(BASE_URL) #로그인 사이트로 이동
#         driver.maximize_window() #화면 크게 
#         time.sleep(1)

#         clear_session(driver) #세션 초기화
#         time.sleep(1)

#         # -----------------------------------
#         # 2) 로그인 수행 (Page Object)
#         # -----------------------------------
#         login_page = LoginPage(driver)
#         login_page.open()
#         login_page.login(
#             email="qa3team0501@elicer.com",
#             password="team05fighting!"
#         )

#         # -----------------------------------
#         # 3) 로그인 성공 검증
#         # -----------------------------------
#         wait.until(EC.url_contains("/ai-helpy-chat"))
#         assert "/ai-helpy-chat" in driver.current_url, \
#             "로그인 후 메인 페이지로 이동하지 못했습니다."

#         # -----------------------------------
#         # 4) 성공 로그
#         # -----------------------------------
#         print("✅ 로그인 성공")

#     except Exception as e:
#         print(f"❌ 로그인 실패")
#         raise


# TC-ME-001
# 로그인 정상 동작 테스트 (POM)

import time
from selenium.webdriver.support import expected_conditions as EC

from utils.helper import (
    BASE_URL,
    get_wait,
    clear_session,
    log_test_start,
)

from pages.login_page import LoginPage


def test_login_success(driver):
    test_name = "로그인 정상 동작 테스트 (POM)"
    log_test_start(test_name)

    # -----------------------------------
    # 1) 페이지 진입 + 세션 초기화
    # -----------------------------------
    driver.get(BASE_URL)
    driver.maximize_window()
    time.sleep(1)

    clear_session(driver)
    time.sleep(1)

    wait = get_wait(driver)

    # -----------------------------------
    # 2) 로그인 수행 (Page Object)
    # -----------------------------------
    login_page = LoginPage(driver)
    login_page.login(
        email="qa3team0501@elicer.com",
        password="team05fighting!"
    )

    # -----------------------------------
    # 3) 로그인 성공 검증
    # -----------------------------------
    wait.until(EC.url_contains("/ai-helpy-chat"))
    assert "/ai-helpy-chat" in driver.current_url, \
        "로그인 후 메인 페이지로 이동하지 못했습니다."

    print("✅ 로그인 성공")
