import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import (
    get_driver,
    login,
    log_test_start,
    log_test_failure,
    log_test_step,
    save_screenshot,
)
# 테스트 케이스 
def test_upload_image():
    test_name = "AI 헬피챗 파일 첨부"
    log_test_start(test_name)
    
    driver = get_driver()
    start_time = time.time()
    
    try:
        # 1. 파일 업로드 준비
        CURRENT_DIR = os.path.dirname(__file__)
        FILE_DIR = os.path.join(CURRENT_DIR, "test-data")
        file_path = os.path.join(FILE_DIR, "duck.jpg")
        
        assert os.path.exsist(file_path), f"업로드 파일이 존재하지 않습니다: {file_path}"
        log_test_step("업로드 완료")
        
        # 2. 로그인
        login(driver, "qa3team0501@elicer.com", "team05fighting!")
        log_test_step("로그인 성공 및 업로드 페이지 열기 성공")
        
        time.sleep(2)
        
        log_test_step("업로드 버튼 선택")
        upload_image = driver.find_element(By.CSS_SELECTOR, '[]')
        
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_input_fail")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e
    finally:
        driver.quit()
        
def send_file(driver, message: str):
    log_test_step("채팅 입력창에 파일 넣기")
    input_box = driver.find_element(By.NAME, 'input')
    input_box.clear()
    input_box.send_keys("test-data/오리.jpg")

    log_test_step("전송 버튼 클릭")
    send_button = driver.find_element(
        By.XPATH,
        '//*[@data-testid="arrow-upIcon"]/ancestor::button'
    )
    send_button.click()
    
    

    