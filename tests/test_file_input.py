import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from utils import (
    get_driver,
    login,
    log_test_start,
    log_test_failure,
    log_test_step,
    save_screenshot,
)
# 테스트 케이스 TC-CB-002 완료
def test_upload_image():
    test_name = "AI 헬피챗 파일 첨부"
    log_test_start(test_name)
    
    driver = get_driver()
    wait = WebDriverWait(driver, 10) 
    start_time = time.time()
    
    try:
        # 1. 파일 업로드 준비
        CURRENT_DIR = os.path.dirname(__file__)
        FILE_DIR = os.path.join(CURRENT_DIR, "test-data")
        file_path = os.path.join(FILE_DIR, "duck.jpg")
        
        assert os.path.exists(file_path), f"업로드 파일이 존재하지 않습니다: {file_path}"
        log_test_step("업로드 파일 준비 완료")
        
        # 2. 로그인
        login(driver, "qa3team0501@elicer.com", "team05fighting!")
        log_test_step("로그인 성공")
        
        # 3. 플러스 버튼 클릭
        log_test_step("플러스 버튼 선택")
        plusBtn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="plusIcon"]'))
        )
        plusBtn.click()

        time.sleep(0.5)
        
        # 4. 파일 업로드 메뉴 클릭
        log_test_step("파일 업로드 메뉴 클릭")
        file_upload = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@data-testid="paperclipIcon"]/ancestor::*[@role="menuitem"]')
            )
        )
        file_upload.click()

        time.sleep(0.5)

        # 5. 숨겨진 input[type=file] 찾기
        log_test_step("파일 input 요소 찾기")
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        
        # 6. 파일 업로드 실행
        log_test_step("파일 업로드 실행")
        file_input.send_keys(file_path)

        time.sleep(1.5)

        # 7. 전송 버튼 클릭
        log_test_step("전송 버튼 클릭")
        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@data-testid="arrow-upIcon"]/ancestor::button')
            )
        )
        send_button.click()
        time.sleep(1)


    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_input_fail")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
