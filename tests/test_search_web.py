import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.driver import get_driver
from utils.helper import save_screenshot, BASE_URL


#테스트 ID: TC-CA-004

# 로그인 정보
TEST_LOGIN_ID = "qa3team0501@elicer.com"
TEST_LOGIN_PASSWORD = "team05fighting!"


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_login_then_search_web_flow(driver):
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

    # 9. 채팅 화면으로 이동하는지 4초 정도 기다리기
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
        # 12. + 메뉴 안에서 '웹 검색' 항목 클릭
        web_search_item = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), '웹 검색')]")
            )
        )
        web_search_item.click()

        # 13. '웹 검색' 텍스트가 포함된 요소가 보이는지 확인
        web_search_label = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), '웹 검색')]")
            )
        )
        assert web_search_label.is_displayed(), "'웹 검색' 텍스트가 화면에 보이지 않습니다."

        # 14. 입력창(textarea[name='input']) 선택
        prompt_textarea = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'textarea[name="input"]')
            )
        )
        assert prompt_textarea.is_enabled(), "프롬프트 입력창(textarea[name='input'])이 비활성화 상태입니다."

        # 15. 프롬프트 입력
        prompt = (
            "QA자동화 과정에 들어갈 내용을 구성중인데, "
            "참고 할만한 최신 논문을 웹에서 검색해줘."
        )
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt)

        # 16. 전송버튼(data-testid='arrow-upIcon') 클릭
        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="arrow-upIcon"]')
            )
        )
        assert send_button is not None, "전송 버튼을 찾지 못했습니다."
        send_button.click()

        # 17. 검색 결과가 나올 때까지 최대 3분(180초) 대기
        long_wait = WebDriverWait(driver, 180)

        copy_button = long_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="copyIcon"]')
            )
        )
        reload_button = long_wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )

        # 복사/다시검색 버튼이 실제로 화면에 보이는지 확인
        assert copy_button.is_displayed(), "결과 하단의 복사 버튼(copyIcon)이 보이지 않습니다."
        assert reload_button.is_displayed(), "결과 하단의 다시검색 버튼(arrows-rotateIcon)이 보이지 않습니다."

    except Exception:
        save_screenshot(driver, "login_search_web_failed")
        raise