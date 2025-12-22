import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD

from utils.driver import get_driver
from utils.helper import (
    log_test_start,
    log_test_failure,
    save_screenshot,
    BASE_URL
)

# 테스트 케이스 TC-CB-015 (보류 -> 수동테스트 진행)

def test_chat_update():
    test_name = "채팅 수정에 따른 검증 테스트"
    log_test_start(test_name)

    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()

    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)
    start_time = time.time()
    
    try:
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        chat_page.send_message("홍길동에 대해 5줄 이내로 알려줘")
        chat_page.wait_for_ai_reply()
        
        time.sleep(5)
        chat_page.hover_update_message()
        
        chat_page.click_update_button()
        updated_text = "홍길동의 가족에 대해 3줄로 알려줘"
        actual = chat_page.update_message(updated_text)
        chat_page.update_send_btn()
        
        assert actual == updated_text, "수정이 반영되지 않았습니다"
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
