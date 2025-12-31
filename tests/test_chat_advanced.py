import time
import os
from pages.login_page import LoginPage
from pages.chat_page import ChatPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_driver
from utils.helper import save_screenshot, BASE_URL, log_test_start, log_test_failure

# 고급 기능 모음
# 최적화 작업자: 양정은
# 코드 작성자: 김나라, 양정은

# 테스트 시나리오: 
# TC-CA-01,
# TC-CA-02(TC-CB-002와 동일), 
# TC-CA-003, TC-CA-004

def test_open_advanced_menu(driver):
    # 1. 메인 페이지(로그인 화면)로 이동
    driver.get(BASE_URL)
    driver.maximize_window()
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:
        # 2. 로그인 수행
        login_page.login(
            email=TEST_LOGIN_ID,
            password=TEST_LOGIN_PASSWORD
        )
        # 3. 채팅 입력창 쪽의 + 버튼 찾기
        chat_page.plus_Btn()
        print("✅ 로그인 및 + 버튼 찾기 성공")
        
        # 4. + 버튼 클릭
        assert chat_page.plus_menu_assert().is_displayed(), 'role="menu" 레이어 팝업이 표시되지 않습니다.'
        print('✅ 로그인 후 + 버튼 클릭 시 role="menu" 레이어 팝업 표시 확인 성공')

    except Exception as e:
        save_screenshot(driver, "test_login_and_plus_menu_failed")
        log_test_failure("test_open_advanced_menu", str(e), 0)
        raise AssertionError(
            "로그인 후 + 버튼 클릭 시 role='menu' 레이어 팝업 표시 확인 중 오류 발생"
        ) from e

def test_upload_image(driver):
    test_name = "AI 헬피챗 파일 첨부"
    log_test_start(test_name)
    
    CURRENT_DIR = os.path.dirname(__file__)  # => "qaproject_team5/tests"
    FILE_PATH = os.path.join(CURRENT_DIR, "test-data", "duck.jpg") # => # qaproject_team5/tests/test-data/duck.jpg
    #FILE_DIR = os.path.join(CURRENT_DIR, "test-data") #=> qaproject_team5/tests/test-data
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:        
        assert os.path.exists(FILE_PATH), f"업로드 파일이 존재하지 않습니다: {FILE_PATH}"
        
        # 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # #플러스 버튼 선택, 파일 업로드 메뉴 클릭
        chat_page.plus_Btn()
        chat_page.file_upload()
        time.sleep(0.5)

        # 파일 선택 창에서 파일 선택
        chat_page.file_upload_select(FILE_PATH)

        time.sleep(2)
        
        # 업로드 완료 후 전송 버튼 클릭   
        chat_page.click_upload_send_button()
        print("클릭 완료")
        
        time.sleep(2)

        assert chat_page.uploaded_thumbnail_assert(), "이미지 썸네일이 표시되지 않았습니다"
        print("이미지 업로드 테스트 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "chat_test_failed")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()

def test_generate_image(driver):
    # 1. 메인 페이지(로그인 화면)로 이동
    driver.get(BASE_URL)
    driver.maximize_window()
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    try:
        # 2. 로그인 수행
        login_page.login(
            email=TEST_LOGIN_ID,
            password=TEST_LOGIN_PASSWORD
        )
        # 3. 플러스 아이콘 클릭
        chat_page.plus_Btn()
        print("플러스 아이콘 클릭 성공")
        # 4. 이미지 생성 아이콘 클릭
        chat_page.click_image_icon()
        print("이미지 생성 아이콘 클릭 성공")
        
        # 5. 이미지 생성 질문 입력 및 전송
        chat_page.input_chat_message(
            "강아지와 소녀가 함께 있는 이미지를 생성해줘"
        )
        chat_page.click_send_button()
        print("이미지 생성 질문 전송 성공")
        
        # 6. AI 응답 대기 및 확인
        chat_page.wait_for_ai_reply()
        print("✅ 결과 표시 성공")  
        
        # 7. 응답에 이미지 포함 여부 확인
        assert chat_page.ai_reply_coniains_imge() != "", "AI 응답이 비어 있습니다."
        print("✅ 이미지 생성 응답에 이미지 포함 확인 성공")
        save_screenshot(driver, "image_generation_success")
    except Exception:
        # 실패 시 스크린샷 저장 후 예외 다시 던지기
        save_screenshot(driver, "image_generation_failed")
        raise

def test_search_web(driver):
    #TC-CA-004_로그인_웹검색
    # wait = WebDriverWait(driver, 10)
    login_page = LoginPage(driver)
    chat_page = ChatPage(driver)

    # 1. 메인 페이지(로그인 화면)로 이동
    driver.get(BASE_URL)
    driver.maximize_window()


    try:
        # 3. 로그인 수행
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        chat_page.plus_Btn()
        chat_page.web_search_Btn()
        print("웹 검색 메뉴 클릭 성공")

        chat_page.input_chat_message(
            "QA자동화 과정에 들어갈 내용을 구성중인데, 웹 검색 기능을 활용하여 최신 정보를 반영해줘."
        )
        
        chat_page.click_send_button()
        print("웹 검색 질문 전송 성공")
        
        chat_page.wait_for_ai_reply()
        print("✅ 웹 검색 결과 표시 성공")
        print(chat_page.wait_for_ai_reply().text)

        assert chat_page.wait_for_ai_reply().text != "", "AI 응답이 비어 있습니다." 
        
    except Exception:
        save_screenshot(driver, "login_search_web_failed")
        raise
    
    