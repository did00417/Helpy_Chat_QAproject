import time
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

# 테스트 케이스 TC-CB-001, TC-CB-008 완료

def test_ai_chat_reply():
    test_name = "AI 헬피챗 채팅 + 복붙 테스트"
    log_test_start(test_name)

    driver = get_driver()
    start_time = time.time()

    try:
        # 1. 로그인
        login(driver, "qa3team0501@elicer.com", "team05fighting!")

        # 2.  채팅 입력창에 "홍길동에 대해 5줄이내로 알려줘" 입력 및 전송
        send_chat_message(driver, "홍길동에 대해 5줄 이내로 알려줘")

        # 3. AI 답변 대기
        reply_element = wait_for_ai_reply(driver)

        # 4. 복사 붙여넣기
        verify_copy_button(driver, reply_element)

    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
        
# 메세지 입력 + 전송 기능       
def send_chat_message(driver, message: str):
    log_test_step("채팅 입력창에 메시지 입력")
    input_box = driver.find_element(By.NAME, 'input')
    input_box.clear()
    input_box.send_keys(message)

    log_test_step("전송 버튼 클릭")
    send_button = driver.find_element(
        By.XPATH,
        '//*[@data-testid="arrow-upIcon"]/ancestor::button'
    )
    send_button.click()
    
# 답변 대기 기능 30초 기다림
def wait_for_ai_reply(driver):
    log_test_step("AI 답변 대기")
    reply = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-status="complete"]')
        )
    )
    return reply

#복사 기능 검증 함수
def verify_copy_button(driver, reply_element):
    log_test_step("복사 버튼 클릭 테스트")

    # 복사 버튼 클릭
    copy_btn = driver.find_element(
        By.CSS_SELECTOR, '[data-testid="copyIcon"]'
    )
    print("복사 버튼 찾음:", copy_btn)
    copy_btn.click()
    time.sleep(0.3)  # 복사 처리 대기

    # 입력창에 붙여넣기
    input_box = driver.find_element(By.NAME, "input")
    input_box.clear()
    input_box.send_keys(Keys.CONTROL, 'v')
    print("붙여넣기 완료")

    pasted = input_box.get_attribute("value").strip()

    # 붙여넣기 결과 검증
    assert pasted != "", "복사 결과가 비어 있습니다."
    
    save_screenshot(driver, "copy_feature_verified")
    
