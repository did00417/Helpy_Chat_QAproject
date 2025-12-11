import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import (
    create_driver,
    get_wait,
    open_main_page,
    take_screenshot,
)

# 테스트 ID : TC-CA-001

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"

@pytest.fixture
def driver():
    driver = create_driver(headless=False)  # 필요하면 True로 바꿔서 헤드리스 실행
    yield driver
    driver.quit()


def test_login_and_open_plus_menu(driver):
    wait = get_wait(driver, timeout=10)

    # 1, 2. 메인 페이지(로그인 화면 또는 채팅 진입 페이지)로 이동
    open_main_page(driver)

    # 3. 아이디 입력영역 찾기 (name="loginId")
    login_id_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "loginId"))
    )
    assert login_id_input is not None, "아이디 입력 필드를 찾지 못했습니다."

    # 4. 아이디 입력
    login_id_input.clear()
    login_id_input.send_keys("qa3team0501@elicer.com")

    # 5. 비밀번호 입력영역 찾기 (name="password")
    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    assert password_input is not None, "비밀번호 입력 필드를 찾지 못했습니다."

    # 6. 비밀번호 입력
    password_input.clear()
    password_input.send_keys("team05fighting!")

    # 7. login 버튼 찾기 (type="submit")
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"], [type="submit"]'))
    )
    assert login_button is not None, "로그인 버튼을 찾지 못했습니다."

    # 8. login 버튼 클릭
    login_button.click()

    # 9. https://qaproject.elice.io/ai-helpy-chat 로 이동하는지 4초정도 기다리기
    try:
        short_wait = get_wait(driver, timeout=4)
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

    # 11. + 버튼 클릭
    plus_button.click()

    # 12. 화면에 role="menu" 를 가진 레이어 팝업이 떴는지 확인
    try:
        menu_layer = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="menu"]'))
        )
        assert menu_layer.is_displayed(), 'role="menu" 레이어 팝업이 표시되지 않습니다.'
    except Exception as e:
        # 13. 실패 시 스크린샷 저장 후 실패 처리
        take_screenshot(driver, prefix="test_login_and_plus_menu_failed")
        raise AssertionError(
            "로그인 후 + 버튼 클릭 시 role='menu' 레이어 팝업 표시 확인 중 오류 발생"
        ) from e