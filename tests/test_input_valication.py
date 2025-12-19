import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_driver
from utils.helper import (
    log_test_start,
    log_test_failure,
    save_screenshot
    )
'''
===========================
테스트 케이스 TC-CB-009, TC-CB-011 완성
코드 작성자: 양정은
===========================
'''

def test_blank():
    test_name = "AI 헬피챗 공백(스페이스) 테스트"

    driver = get_driver()
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    start_time = time.time()
    
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:
        # 1. 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # 2.  채팅 입력창에 "   " 공백(스페이스바) 입력 & 전송
        chat_page.input_chat_message("    ")
        
        time.sleep(3)
        
        #3. 전송 버튼 활성화 유무 조회
        send_button = chat_page.send_button_assert()

        
        assert not send_button.is_enabled(), "공백만 입력했는데 전송 버튼이 활성화됨"
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "blank_Test")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
        
def test_long_str():
    test_name = "헬피젯 긴 문자열 입력 테스트 테스트 코드: TC-CB-011"

    driver = get_driver()
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    start_time = time.time()
    
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:
        # 1. 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # 2.  A 200자 입력
        long_str = "A" * 200
        chat_page.input_chat_message(long_str)
        
        send_button = chat_page.send_button_assert()
        assert send_button.is_enabled(), " 입력 시 전송 버튼이 활성화되지 않음"

    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "long_str")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()

