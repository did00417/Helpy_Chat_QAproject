import time
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from selenium.webdriver.support.ui import WebDriverWait
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD

from selenium.webdriver.common.by import By
from utils.driver import get_driver
from utils.helper import (
    log_test_start,
    log_test_failure,
    save_screenshot,
    BASE_URL
)

# 검색 기능 테스트 케이스 작성: TC-SC-001 작성자 양정은
def test_search_bar():
    test_name = "헬피챗 검색창 정상 노출 검증"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    search_page = SearchPage(driver)
    try:
        #로그인
        print("로그인 시도")
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        #검색 버튼 클릭
        print("검색 버튼 클릭")
        search_page.magnifier_click()
        
        print("클릭 후 검색창 검증 여부 확인")
        assert search_page.is_search_bar_visible(), "검색창이 표시되지 않음"
        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "search_bar")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()  
        
# TC-SC-002
def test_history_click():
    test_name = "헬피챗 검색 기능 테스트 - 히스토리 목록 중 하나 선택"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    search_page = SearchPage(driver)
    
    try:
        #로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        #검색 버튼 클릭
        search_page.magnifier_click()
        
        #검색어 입력
        search_page.search_word_send("홍길동")
        
        time.sleep(3)
        
        #히스토리 목록 
        history_list = search_page.history_list()
        print(len(history_list))
        
        assert len(history_list) > 0, "클릭할 히스토리 항목이 없습니다."
        print("✅ 히스토리 항목 존재 확인")
        # 첫 번째 히스토리 클릭
        history_list2 = search_page.history_list()
        history_list2[0].click()

        # 채팅 화면 전환 검증
        WebDriverWait(driver, 5).until(
            EC.url_contains("/ai-helpy-chat/chats/")
        )
        print("✅ 히스토리 목록 클릭 및 채팅 화면 전환 성공")
    
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "history_click")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
        
# TC-SC-003 - 검색어에 대한 결과가 없는 경우
def test_search_history_no_result():
    test_name = "헬피챗 검색 기능 테스트 - 검색어에 대한 결과가 없는 경우"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    search_page = SearchPage(driver)
    
    try:
        #로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        #검색 버튼 클릭
        search_page.magnifier_click()
        
        #검색어 입력
        search_page.search_word_send("감사")
        
        time.sleep(2)
        
        #히스토리 목록 확인
        history_list = search_page.history_list()
        history_list = len(history_list)
        print(f"히스토리 목록의 개수: {history_list}")
         
        assert history_list == 0, "검색 결과가 확인됩니다."
        print("✅ 검색어에 대한 결과가 없는 경우 성공")

        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "history_list")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()
    
         
# TC-SC-004 히스토리 목록 확인
def test_search_history():
    test_name = "헬피챗 검색 기능 테스트 - 히스토리 목록 확인"
    
    driver = get_driver()
    driver.get(BASE_URL)
    driver.maximize_window()
    start_time = time.time()
    
    login_page = LoginPage(driver)
    search_page = SearchPage(driver)
    
    try:
        #로그인
        login_page.login(
        email=TEST_LOGIN_ID,
        password=TEST_LOGIN_PASSWORD
    )
        
        #검색 버튼 클릭
        search_page.magnifier_click()
        
        #검색어 입력
        search_page.search_word_send("홍길동")
        
        time.sleep(2)
        
        #히스토리 목록 확인
        history_list = search_page.history_list()        
        history_list = len(history_list)
        print(f"히스토리 목록의 개수: {history_list}")
         
        assert history_list > 0, "검색 결과가 없습니다."
        print("✅ 히스토리 목록 확인 성공")

        
    except Exception as e:
        print("코드의 작동이 비정상적입니다.")
        save_screenshot(driver, "history_list")
        log_test_failure(test_name, str(e), time.time() - start_time)
        raise e

    finally:
        driver.quit()