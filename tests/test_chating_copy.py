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
)

# 테스트 케이스 TC-CB-001, TC-CB-008 완료
# 작성자 양정은


def test_ai_chat_reply():
    test_name = "AI 헬피챗 채팅 + 복붙 테스트"
    log_test_start(test_name)

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
        chat_page.send_message("홍길동에 대해 5줄 이내로 알려줘")

        # 3. AI 답변 대기
        reply_element = chat_page.wait_for_ai_reply()

        # 4. 복사 붙여넣기
        
        value = chat_page.copy_and_paste(reply_element)
        time.sleep(3)
        assert value != "", "복사 결과가 비어 있습니다."

    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
