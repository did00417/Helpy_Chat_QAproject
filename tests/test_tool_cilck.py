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
테스트 케이스:TC-TO-001~TC-TO-004, TC-TO-008 완료
코드 작성자: 양정은
===========================
'''
def test_click_detail_note():
    test_name = "AI 헬피챗 세부특기사항 클릭 테스트"
    
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
        
        # 세부 특기 사항 클릭
        tool_page.open_detail_note()
        
        time.sleep(3)
        
        # 세부 특기 사항 검증
        assert tool_page.get_detail_note()
        print("✅ 세부 특기 사항 클릭 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "detail_note")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()

def test_click_behavior_summary():
    test_name = "AI 헬피챗 세부특기사항 클릭 테스트"
    
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
        
        # 행동특성 및 종합의견 페이지 클릭
        tool_page.open_behavior_summary_page()
        
        time.sleep(3)
        
        # 행동특성 및 종합의견 페이지 검증
        assert tool_page.get_behavior_summary()
        print("✅ 행동특성 및 종합의견 클릭 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "behavior_summary")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()        
        
def test_click_lesson_plan():
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
        
        # 수업 지도안 클릭
        tool_page.open_lesson_plan()
        
        time.sleep(3)
        
        # 수업 지도안 검증
        assert tool_page.get_lesson_plan()
        print("✅ 수업 지도안 클릭 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "lesson_plan")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit() 
        
def test_click_ppt_generation():
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
        
        time.sleep(3)
        
        # PPT 생성 메뉴 클릭 후 검증
        assert tool_page.get_ppt_generation()
        print("✅ PPT 생성 클릭 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "get_ppt_generation")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()       
        
def test_click_qize():
    test_name = "AI 헬피챗 퀴즈 생성 클릭 테스트"
    
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
        
        # Qize 클릭
        tool_page.open_quiz_card()
        
        time.sleep(3)
        
        # Qize 메뉴 클릭 후 검증
        assert tool_page.get_quiz()
        print("✅ Quiz 클릭 성공")
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "get_qize")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()   
      
        
          