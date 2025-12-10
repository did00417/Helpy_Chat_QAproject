import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from utils import (
    get_driver,
    login,
    log_test_start,
    log_test_success,
    log_test_failure,
    log_test_step,
    save_screenshot,
)

# 테스트 케이스 TC-CB-001

def test_ai_chat_reply():
    test_name = "AI 헬피챗 채팅 테스트"
    log_test_start(test_name)

    driver = get_driver()
    start_time = time.time()

    try:
        # 1. 로그인
        login(driver, "qa3team0501@elicer.com", "team05fighting!")

        # 2.  채팅 입력창에 "홍길동" 입력
        log_test_step("채팅 입력창에 메시지 입력")
        input_box = driver.find_element(By.NAME, 'input')
        input_box.clear()
        input_box.send_keys("홍길동에 대해 5줄이내로 알려줘")

        # 3. 전송 버튼 클릭 (↑ 아이콘)
        log_test_step("전송 버튼 클릭")
        send_button = driver.find_element(
            By.XPATH,
            '//*[@data-testid="arrow-upIcon"]/ancestor::button'
        )
        send_button.click()

        # 4. AI 답변 기다리기
        log_test_step("AI 답변 대기")
        time.sleep(2)  # 필요 시 WebDriverWait으로 교체 가능

        # AI 답변을 최대 30초까지 기다림
        reply = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[data-status="complete"]'))
            )

        assert reply is not None, "AI가 답변을 생성하지 않았습니다."
        save_screenshot(driver, "chat_reply_received")

    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()