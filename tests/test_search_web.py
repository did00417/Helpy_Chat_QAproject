import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_driver
from utils.helper import save_screenshot, BASE_URL

# 최적화 작업자: 양정은
# 테스트 시나리오: TC-CA-004_로그인_웹검색

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_login_then_search_web_flow(driver):
    wait = WebDriverWait(driver, 10)
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    # 1, 2. 메인 페이지(로그인 화면)로 이동
    driver.get(BASE_URL)
    driver.maximize_window()


    try:
        # 3. 로그인 수행
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        chat_page.plus_Btn()
        chat_page.web_search_Btn()
        print("웹 검색 메뉴 클릭 성공")

        chat_page.input_chat_message(
            "QA자동화 과정에 들어갈 내용을 구성중인데, 웹 검색 기능을 활용하여 최신 정보를 반영해줘."
        )
        
        chat_page.click_send_button()
        print("웹 검색 질문 전송 성공")
        
        chat_page.wait_for_ai_reply()
        print("✅ 웹 검색 결과 표시 성공")
        print(chat_page.wait_for_ai_reply().text)

        assert chat_page.wait_for_ai_reply().text != "", "AI 응답이 비어 있습니다." 
        
    except Exception:
        save_screenshot(driver, "login_search_web_failed")
        raise