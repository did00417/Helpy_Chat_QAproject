from json import tool
import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.tool_page import ToolPage
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD
from utils.driver import get_driver
from utils.helper import (
    log_test_start,
    log_test_failure,
    save_screenshot,
    BASE_URL
    )

'''
===========================
테스트 케이스:TC-TO-005~TC-TO-007 완성 (5, 6합침))
코드 작성자: 양정은
===========================
'''

def test_ppt_generation():
    test_name = "AI 헬피챗 수업 지도안 클릭 테스트"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    tool_page = ToolPage(driver)
    
    try:
        #테스트 시작
        log_test_start(test_name)
        
        # 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # 도구 아이콘 클릭
        tool_page.click_tool()
        
        # PPT 생성 클릭
        tool_page.open_ppt_generation_card()
        
        # PPT 생성에 필요한 내용 입력
        ppt_title = "인공지능 요구사항 종류"
        ppt_instruc = "인공지능 서비스 요구사항 도출 및 명세화에서 인공지는 서비스 요구사항 도출과 인공지능 서비스 요구사항 명세화에 대해서 이미지와 도표를 추가해서 중학생이 이해 할 수 있는 수준으로 설명"
        ppt_slide = 3
        ppt_section =  2
        
        tool_page.input_ppt_content(ppt_title, ppt_instruc, ppt_slide, ppt_section)
        
        time.sleep(2)
        
        tool_page.get_generate_button()
        tool_page.again_generate_click()
        
        time.sleep(2)
        
        assert tool_page.wait_downlord_button()   
        print("✅ PPT 생성 성공, 다운로드 버튼 표시 확인")
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "get_ppt_generation")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
        
# 필수 입력 값 미입력시 다시 생성 버튼 비활성화 검증 
def test_regenerate_disabled_without_subject():
    test_name = "필수 입력 값 미입력시 다시 생성 버튼 비활성화 검증"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    tool_page = ToolPage(driver)
    
    try:
        #테스트 시작
        log_test_start(test_name)
        
        # 로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        # 도구 아이콘 클릭
        tool_page.click_tool()
        
        # PPT 생성 클릭
        tool_page.open_ppt_generation_card()
        
        # PPT 생성에 필요한 내용 입력
        ppt_title = ""
        ppt_instruc = "인공지능 서비스 요구사항 도출 및 명세화에서 인공지는 서비스 요구사항 도출과 인공지능 서비스 요구사항 명세화에 대해서 이미지와 도표를 추가해서 중학생이 이해 할 수 있는 수준으로 설명"
        ppt_slide = 5
        ppt_section =  1
        
        tool_page.input_ppt_content(ppt_title, ppt_instruc, ppt_slide, ppt_section)
        time.sleep(2)
        
        assert not tool_page.again_btn_assert().is_enabled()
        print("✅ 필수 입력 값 미입력시 다시 생성 버튼 비활성화 검증 성공")
   
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "get_ppt_generation")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()