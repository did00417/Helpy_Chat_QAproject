import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.tool_page import ToolPage
from utils.driver import get_driver
from utils.helper import (
    BASE_URL,
    log_test_start,
    log_test_failure,
    save_screenshot
    )

'''
===========================
테스트 케이스:TC-TO-005~TC-TO-007 진행중(5 6 합침)
코드 작성자: 양정은
===========================
'''

def test_ppt_generation():
    test_name = "AI 헬피챗 수업 지도안 생성 테스트"
    
    driver = get_driver()
    driver.get(BASE_URL)
    start_time = time.time()
    
    login_page = LoginPage(driver)
    tool_page = ToolPage(driver)
    
    try:
        #테스트 시작
        log_test_start(test_name)
        
        # 로그인
        login_page.login()
        
        # 도구 아이콘 클릭
        tool_page.click_tool()
        
        # PPT 생성 클릭
        tool_page.open_qize_card()
        
        # PPT 생성에 필요한 내용 입력
        '''
        객관식 단일 선택 = 0   난이도 상 = 3
        객관식 복수 선택 = 1   난이도 중 = 2
        주관식 = 3             난이도 하 = 1
        '''
        qize_type = 3
        qize_level = 1
        qize_title = "인공지능 서비스 요구사항 도출 및 명세화에서 인공지는 서비스 요구사항 도출과 인공지능 서비스 요구사항 명세화에 대해서  퀴즈 10개를 만들어주고, 정답에 대한 설명도 추가해줘."
        
        tool_page.input_qize_content(qize_type, qize_level, qize_title)
        
        time.sleep(2)
        
        tool_page.get_quiz_generate_button()
        # tool_page.again_generate_click()
        
        time.sleep(5)
        
        # assert tool_page.wait_downlord_button()   
   
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "get_ppt_generation")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()