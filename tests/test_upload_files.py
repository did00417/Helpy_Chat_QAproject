import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from utils.driver import (get_driver)
from utils.helper import (
    save_screenshot,
    wait_for_url_contains,
)

# 테스트 ID = TC-CA-002

BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"

# 테스트에 사용할 로그인 정보
TEST_LOGIN_ID = "qa3team0501@elicer.com"
TEST_LOGIN_PASSWORD = "team05fighting!"

# 현재 이 파일(test_upload_files.py)이 있는 폴더 기준으로 PDF 파일 경로 설정
BASE_DIR = os.path.dirname(__file__)                 # .../pytest-exam/tests
TEST_PDF_PATH = os.path.join(BASE_DIR, "files", "CPMAI.pdf")  # .../tests/files/CPMAI.pdf


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_login_then_upload_pdf_and_regenerate(driver):
    wait = WebDriverWait(driver, 10)
    
    login_page = LoginPage(driver)
    # 1. 로그인 수행 (공통 함수 사용)
    login_page.login()

    # 2. 로그인 후 예상 URL로 이동했는지 확인 (최대 10초)
    try:
        wait_for_url_contains(driver, BASE_URL)
    except Exception:
        current = driver.current_url
        assert BASE_URL in current, (
            f"로그인 후 예상 URL({BASE_URL})로 이동하지 않았습니다. "
            f"현재 URL: {current}"
        )

    # 3. 채팅 입력창 쪽의 + 버튼 찾기 (data-icon="plus") be 추가로 넣음
    plus_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-icon="plus"]'))
    )
    assert plus_button is not None, "+ 버튼을 찾지 못했습니다."

    # 4. + 버튼 클릭 (고급 메뉴 열기)
    plus_button.click()

    # 5. '파일업로드' 아이콘 클릭
    paperclip_icon = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="paperclipIcon"]')
        )
    )
    paperclip_icon.click()

    # 6. 파일 업로드 input[type="file"] 찾기
    file_input = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        )
    )
    assert file_input.is_enabled(), "파일 업로드 input[type='file'] 요소가 활성화되어 있지 않습니다."

    # PDF 파일 존재 여부 확인 후 업로드
    print("[DEBUG] TEST_PDF_PATH =", TEST_PDF_PATH)
    print("[DEBUG] os.path.isfile?", os.path.isfile(TEST_PDF_PATH))
    assert os.path.isfile(TEST_PDF_PATH), f"테스트 파일이 존재하지 않습니다: {TEST_PDF_PATH}"
    file_input.send_keys(TEST_PDF_PATH)

    # 7. 프롬프트 입력창(textarea[name="input"]) 찾기
    prompt_textarea = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'textarea[name="input"]')
        )
    )
    assert prompt_textarea.is_enabled(), "프롬프트 입력창(textarea[name='input'])이 비활성화 상태입니다."

    # 프롬프트 내용 입력
    prompt = (
        "파일을 한국어로 번역해서 1000자로 요약하고, 주요 키워드를 표로 만들어서, "
        "보통 난이도의 객관식 단수 유형의 퀴즈 10개를 만들어줘."
    )
    prompt_textarea.clear()
    prompt_textarea.send_keys(prompt)

    # 8. 전송 버튼 클릭 (data-testid="arrow-upIcon")
    send_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[data-testid="arrow-upIcon"]')
        )
    )
    send_button.click()

    # 9. 첫 번째 응답 결과 대기 (copyIcon, arrows-rotateIcon 이 보일 때까지) → 최대 3분 대기
    try:
        long_wait = WebDriverWait(driver, 180)  # 3분(180초) 대기
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
        assert copy_button.is_displayed(), "첫 번째 응답의 copyIcon 이 표시되지 않습니다."
        assert reload_button.is_displayed(), "첫 번째 응답의 arrows-rotateIcon 이 표시되지 않습니다."
    except Exception as e:
        save_screenshot(driver, "login_upload_first_response_failed")
        raise AssertionError("첫 번째 응답 생성 확인 중 오류 발생") from e

    # 10. '다시 생성' 버튼 클릭 (aria-label="다시 생성")
    regenerate_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '[aria-label="다시 생성"]')
        )
    )
    regenerate_button.click()

    # 11. 재생성된 응답 결과 대기 (copyIcon, arrows-rotateIcon 다시 확인) → 최대 3분 대기
    try:
        long_wait_2 = WebDriverWait(driver, 180)  # 3분(180초) 대기
        copy_button_after = long_wait_2.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="copyIcon"]')
            )
        )
        reload_button_after = long_wait_2.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )
        assert copy_button_after.is_displayed(), "재생성 후 copyIcon 이 표시되지 않습니다."
        assert reload_button_after.is_displayed(), "재생성 후 arrows-rotateIcon 이 표시되지 않습니다."
    except Exception as e:
        save_screenshot(driver, "login_upload_regenerate_failed")
        raise AssertionError("재생성된 응답 확인 중 오류 발생") from e