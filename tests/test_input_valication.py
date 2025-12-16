import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.driver import get_driver
from utils.helper import (
    log_test_start,
    log_test_failure,
    save_screenshot
    )
'''
===========================
테스트 케이스 TC-CB-009, TC-CB-011 진행중
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
        login_page.login()
        
        # 2.  채팅 입력창에 "   " 공백(스페이스바) 입력 & 전송
        chat_page.send_message("    ")
        
        time.sleep(3)
        
        #3. 전송 버튼 활성화 유무 조회
        chat_page.send_button_assert()
        print("검증이 완료 됐습니다.")
        
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
        login_page.login()
        
        # 2.  A 20000자 입력
        long_str = "A" * 20000
        chat_page.send_message(long_str)
        
        time.sleep(30)
        
        assert chat_page.send_button_assert.is_enabled()
       
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "long_str")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()

