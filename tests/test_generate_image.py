import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.driver import get_driver
from utils.helper import  save_screenshot, BASE_URL

# 테스트 ID : TC-CA-003
BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"

# 로그인 정보
TEST_LOGIN_ID = "qa3team0501@elicer.com"
TEST_LOGIN_PASSWORD = "team05fighting!"


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_login_then_generate_image_flow(driver):
    wait = WebDriverWait(driver, 10)

    # 1, 2. 메인 페이지(로그인 화면)로 이동
    driver.get(BASE_URL)
    driver.maximize_window()

    # 3. 아이디 입력영역 찾기 (name="loginId")
    login_id_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "loginId"))
    )
    assert login_id_input is not None, "아이디 입력 필드를 찾지 못했습니다."

    # 4. 아이디 입력
    login_id_input.clear()
    login_id_input.send_keys(TEST_LOGIN_ID)

    # 5. 비밀번호 입력영역 찾기 (name="password")
    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    assert password_input is not None, "비밀번호 입력 필드를 찾지 못했습니다."

    # 6. 비밀번호 입력
    password_input.clear()
    password_input.send_keys(TEST_LOGIN_PASSWORD)

    # 7. login 버튼 찾기 (type="submit")
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"], [type="submit"]')
        )
    )
    assert login_button is not None, "로그인 버튼을 찾지 못했습니다."

    # 8. login 버튼 클릭
    login_button.click()

    # 9. https://qaproject.elice.io/ai-helpy-chat 로 이동하는지 4초 정도 기다리기
    try:
        short_wait = WebDriverWait(driver, 4)
        short_wait.until(EC.url_contains(BASE_URL))
    except Exception:
        current = driver.current_url
        assert BASE_URL in current, (
            f"로그인 후 예상 URL({BASE_URL})로 이동하지 않았습니다. "
            f"현재 URL: {current}"
        )

    # 10. 채팅 입력창 쪽의 + 버튼 찾기 (data-icon="plus")
    plus_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="plus"]'))
    )
    assert plus_button is not None, "+ 버튼을 찾지 못했습니다."

    # 11. + 버튼 클릭 (고급 메뉴 열기)
    plus_button.click()

    try:
        # 12. '이미지 생성' 아이콘(data-testid="imageIcon") 클릭
        image_icon = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="imageIcon"]')
            )
        )
        image_icon.click()

        # 13. '이미지 생성' 텍스트가 포함된 요소가 보이는지 확인
        generate_image_label = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), '이미지 생성')]")
            )
        )
        assert generate_image_label.is_displayed(), "'이미지 생성' 텍스트가 화면에 보이지 않습니다."

        # 14. 프롬프트 입력창(textarea[name="input"]) 찾기
        prompt_textarea = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'textarea[name="input"]')
            )
        )
        assert prompt_textarea.is_enabled(), "프롬프트 입력창(textarea[name='input'])이 비활성화 상태입니다."

        # 15. 프롬프트 입력
        prompt = "QA자동화 과정에 사용할 셀레늄과 파이테스트의 강의자료 이미지를 만들어줘"
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt)

        # 16. 전송 버튼(data-testid="arrow-upIcon") 클릭
        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="arrow-upIcon"]')
            )
        )
        send_button.click()

        # 17. 최대 3분(180초) 동안 결과로 생성된 이미지(img 요소)가 보이는지 확인
        long_wait = WebDriverWait(driver, 180)
        generated_image = long_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "img")
            )
        )
        assert generated_image.is_displayed(), "생성된 이미지(img)가 화면에 보이지 않습니다."
        print("✅ 이미지 생성 성공")

    except Exception:
        # 실패 시 스크린샷 저장 후 예외 다시 던지기
        save_screenshot(driver, "login_generate_image_failed")
        raise