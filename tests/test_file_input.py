import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_driver
from utils.helper import log_test_start, log_test_failure, save_screenshot

# __file__ => 실행 시킨 파이썬 파일
# qaproject_team5/tests/test_file_input.py
# test_file_input.py
# dirname => 파일의 폴더의 위치
CURRENT_DIR = os.path.dirname(__file__)  # => "qaproject_team5/tests"

# qaproject_team5/tests/test-data/duck.jpg
FILE_PATH = os.path.join(CURRENT_DIR, "test-data", "duck.jpg")
# qaproject_team5/tests/test-data
FILE_DIR = os.path.join(CURRENT_DIR, "test-data")


# 테스트 케이스 TC-CB-002 완료 작성자: 양정은
def test_upload_image():
    test_name = "AI 헬피챗 파일 첨부"
    log_test_start(test_name)

    driver = get_driver()
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    wait = WebDriverWait(driver, 10)
    start_time = time.time()
    
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:        
        assert os.path.exists(FILE_PATH), f"업로드 파일이 존재하지 않습니다: {FILE_PATH}"
        
        # 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # #플러스 버튼 선택, 파일 업로드 메뉴 클릭
        chat_page.plus_Btn()
        chat_page.file_upload()
        time.sleep(0.5)

        # 파일 선택 창에서 파일 선택
        chat_page.file_upload_select(FILE_PATH)

        time.sleep(2)
        
        # 업로드 완료 후 전송 버튼 클릭   
        chat_page.click_upload_send_button()
        print("클릭 완료")
        
        time.sleep(2)

        assert chat_page.uploaded_thumbnail_assert(), "이미지 썸네일이 표시되지 않았습니다"
        print("이미지 업로드 테스트 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
