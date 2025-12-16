import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.driver import get_driver
from utils.helper import log_test_start

# __file__ => 실행 시킨 파이썬 파일
# qaproject_team5/tests/test_file_input.py
# test_file_input.py
# dirname => 파일의 폴더의 위치
CURRENT_DIR = os.path.dirname(__file__)  # => "qaproject_team5/tests"

# qaproject_team5/tests/test-data/duck.jpg
FILE_PATH = os.path.join(CURRENT_DIR, "test-data", "duck.jpg")
# qaproject_team5/tests/test-data
FILE_DIR = os.path.join(CURRENT_DIR, "test-data")


# 테스트 케이스 TC-CB-002 완료
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
        # 1. 파일 업로드 준비
        CURRENT_DIR = os.path.dirname(__file__)
        FILE_DIR = os.path.join(CURRENT_DIR, "test-data")
        FILE_PATH = os.path.join(FILE_DIR, "duck.jpg")

        assert os.path.exists(FILE_PATH), f"업로드 파일이 존재하지 않습니다: {FILE_PATH}"
        
        # 로그인
        login_page.login()
        
        # #플러스 버튼 선택, 파일 업로드 메뉴 클릭
        chat_page.puls_Btn()
        chat_page.file_upload()
        time.sleep(0.5)

        # 숨겨진 input[type=file] 찾기
        print("파일 input 요소 찾기")
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        file_input.send_keys(FILE_PATH)
        print("사진 업로드 완료")

        time.sleep(2)

        # 전송 버튼 대기 후 클릭
        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@data-testid="arrow-upIcon"]/ancestor::button')
            )
        )
        send_button.click()
        print("클릭 완료")
        
        time.sleep(2)

    finally:
        driver.quit()
