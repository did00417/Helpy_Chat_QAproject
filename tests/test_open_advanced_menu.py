import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from utils.driver import get_driver
from utils.helper import save_screenshot


BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"

@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_login_and_open_plus_menu(driver):
    wait = WebDriverWait(driver, 10)

    # 1. 로그인 수행 (공통 함수 사용)
    login_page = LoginPage(driver)
    driver.get(BASE_URL)
    login_page.login(
        email="qa3team0501@elicer.com",
        password="team05fighting!"
    )

    # 2. URL 확인 (간단 버전)
    short_wait = WebDriverWait(driver, 4)
    try:
        short_wait.until(EC.url_contains(BASE_URL))
    except Exception:
        current = driver.current_url
        assert BASE_URL in current, (
            f"로그인 후 예상 URL({BASE_URL})로 이동하지 않았습니다. "
            f"현재 URL: {current}"
        )

    # 3. 채팅 입력창 쪽의 + 버튼 찾기
    plus_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="plus"]'))
    )
    assert plus_button is not None, "+ 버튼을 찾지 못했습니다."

    # 4. + 버튼 클릭
    plus_button.click()

    # 5. role="menu" 레이어 팝업 확인
    try:
        menu_layer = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="menu"]'))
        )
        assert menu_layer.is_displayed(), 'role="menu" 레이어 팝업이 표시되지 않습니다.'
    except Exception as e:
        save_screenshot(driver, "test_login_and_plus_menu_failed")
        raise AssertionError(
            "로그인 후 + 버튼 클릭 시 role='menu' 레이어 팝업 표시 확인 중 오류 발생"
        ) from e