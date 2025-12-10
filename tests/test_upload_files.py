import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from utils import open_advanced_menu, get_wait


def test_upload_pdf_with_prompt_and_regenerate():
    

    driver = open_advanced_menu()          # 1) 메인 + 고급 메뉴까지 열린 상태
    wait = get_wait(driver, timeout=10)
    try:
        # 2) '파일업로드' 아이콘 클릭
        paperclip_icon = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="papercliplcon"]')
            )
        )
        paperclip_icon.click()

        # 3) 파일 업로드 input[type="file"]
        file_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='file']")
            )
        )
        assert file_input.is_enabled(), "파일 업로드 input[type='file'] 요소가 활성화되어 있지 않습니다."

        # 4) PDF 파일 경로
        pdf_path = r"C:\Users\user\Downloads\CPMAI+v7+-+02+The+Application+of+AI.pdf"
        assert os.path.isfile(pdf_path), f"테스트 파일이 존재하지 않습니다: {pdf_path}"
        file_input.send_keys(pdf_path)

        # 5) 프롬프트 입력
        prompt_textarea = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'textarea[name="input"]')
            )
        )
        assert prompt_textarea.is_enabled(), "프롬프트 입력창(textarea[name='input'])이 비활성화 상태입니다."

        prompt = (
            "파일을 한국어로 번역해서 1000자로 요약하고, 주요 키워드를 표로 만들어서, "
            "보통 난이도의 객관식 단수 유형의 퀴즈 10개를 만들어줘."
        )
        prompt_textarea.clear()
        prompt_textarea.send_keys(prompt)

        # 6) 전송 버튼 클릭
        send_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="arrow-upIcon"]')
            )
        )
        send_button.click()

        # 7) 결과 대기
        copy_button = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="copyIcon"]')
            )
        )
        reload_button = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )
        assert copy_button.is_displayed()
        assert reload_button.is_displayed()

        # 9) 다시 생성
        regenerate_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[aria-label="다시 생성"]')
            )
        )
        regenerate_button.click()

        # 10) 재결과 대기
        copy_button_after = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="copyIcon"]')
            )
        )
        reload_button_after = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="arrows-rotateIcon"]')
            )
        )
        assert copy_button_after.is_displayed()
        assert reload_button_after.is_displayed()

    finally:
        driver.quit()