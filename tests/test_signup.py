
import time 
import pytest #테스트 실행! 이게 있어야지 자동화 실행 가능
from selenium.webdriver.common.by import By #요소찾기! xpath, name, id 등등등 
from selenium.webdriver.support import expected_conditions as EC #어떤 상태가 될 때까지 기달리기! 예)버튼이 클릭 가능할 때까지 기달리기 
from selenium.webdriver.common.keys import Keys #키보드 입력 관련 (TAB, ENTER 등)
from pages.signup_page import SignupPage
#팀원들과 같이 사용하는 유틸 함수 
from utils.helper import ( 
    get_wait, #webdriverwait 생성 
    clear_session, #쿠키 삭제
    wait_for_error_message, #에러 메시지 나올 때까지 기달리기
    log_test_start, #테스트 시작로그
    log_test_success, #테스트 성공 로그
    log_test_failure, #테스트 실패 로그
    save_screenshot, #테스트 실패 시 스크린샷
    BASE_URL #기본 사이트 주소
)

# ======================================================
# 이메일/비밀번호 형식 잘못 된 테스트 데이터
# ======================================================
invalid_emails = [
    "홍길동@gmail.com",
    "@#$@gmail.com",
    "漢子@gmail.com",
    "test.gmail@com",
]

invalid_passwords = [
    "12345678",
    "abcdefgh",
]

REGISTERED_EMAIL = "qa3team05@elicer.com"


# ======================================================
# 공통 헬퍼: 회원가입 (Email) 페이지 진입
# ======================================================
def go_to_signup_with_email(driver, wait): #회원가입 페이지 가는 함수
    driver.get(BASE_URL) 
    driver.maximize_window()
    time.sleep(1)

    clear_session(driver)
    time.sleep(1)

    # Create account 클릭 가능할 때까지 기달렸다가 클릭
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Create account')]")
        )
    ).click()

    # Create account with email 클릭
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Create account with email')]")
        )
    ).click()


# ======================================================
# TC-ME-007 회원가입 - 잘못된 이메일 형식
# ======================================================
@pytest.mark.parametrize("email", invalid_emails) #invalid_emails 데이터 하나씩 테스트 

def test_signup_invalid_email(driver, email):
    test_name = f"회원가입 - 잘못된 이메일 형식 테스트 ({email})"
    # start = time.time()
    # log_test_start(test_name)

    # try:
    wait = get_wait(driver)
    go_to_signup_with_email(driver, wait)

    SignupPage(driver).input_username(email)#이메일 입력칸에 잘못 된 이메일 입력

    error_msg = wait_for_error_message( #에러 메시지 나올 때까지 기달리기
        driver, "Email address is incorrect"
    )

    assert "Email address is incorrect" in error_msg.text #문구 맞는지 확인 

    # duration = time.time() - start
    # log_test_success(test_name, duration) #테스트 성공 기록
    print("✅ 잘못된 이메일 형식 테스트 성공")

    # except Exception as e:
    #     duration = time.time() - start
    #     save_screenshot(driver, "signup_invalid_email") #스샷 저장
    #     log_test_failure(test_name, str(e), duration)
    #     raise


# ======================================================
# TC-ME-008 회원가입 - 잘못된 비밀번호 조건
# ======================================================
@pytest.mark.parametrize("password", invalid_passwords) #invalid_passwords 하나씩 테스트 

def test_signup_invalid_password(driver, password):
    test_name = f"회원가입 - 잘못된 비밀번호 조건 테스트 ({password})"
    # start = time.time() #테스트 시간 기록
    # log_test_start(test_name)

    # try:
    wait = get_wait(driver) #기다리면서 요소 찾기
    go_to_signup_with_email(driver, wait) #사이트 접속 > 회원가입 진입

    SignupPage(driver).input_username("test123@naver.com")

    #Password 입력칸이 화면에 존재할 때까지 기다리기
    password_input = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Password']")
        )
    )
    print("비밀번호 입력칸 찾음")
    password_input.clear() #혹시 모르니깐 값 삭제
    password_input.send_keys(password) #값입력
    print("비밀번호 입력함")
    
    create_btn = wait.until( #가입 버튼 비활성화 확인 아래 문구 나타 날 때까지 기달리기
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Create account')]")
        )
     )
    assert create_btn.get_attribute("disabled") is not None #버튼 disabled 속성이 있다

    # duration = time.time() - start
    # log_test_success(test_name, duration)
    print("✅ 잘못된 비밀번호 조건 확인 테스트")

    # except Exception as e:
    #     duration = time.time() - start
    #     save_screenshot(driver, "signup_invalid_password")
    #     log_test_failure(test_name, str(e), duration)
    #     raise


# ======================================================
# TC-ME-009 회원가입 - 이미 가입된 이메일
# ======================================================
def test_signup_registered_email(driver): #pytest 테스트 함수
    # test_name = "회원가입 - 이미 가입된 이메일 입력 시 에러 메시지 확인" #로그에 남길 테스트 제목 / 리포트 볼 때 한눈에 알 수 있음
    # start = time.time() #테스트 시작 시간 저장
    # log_test_start(test_name) #테스트 시작

    #try: #실패 시 스샷저장/ 실패로그 /테스트 실패 처리
    wait = get_wait(driver) #wait 준비 + 회원가입 페이지 이동
    go_to_signup_with_email(driver, wait) #공통 함수 실행

    #이미 가입된 이메일 입력 > 에러 메시지 노출 > 가입 버튼 비활성화 확인
    SignupPage(driver).input_username(REGISTERED_EMAIL)

    error_msg = wait_for_error_message(
        driver, "This is an already registered email address"
    )

    assert "This is an already registered email address" in error_msg.text

    create_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Create account')]")
        )
    )
    assert create_btn.get_attribute("disabled") is not None #이 버튼에는 disabled라는 속성이 실제로 존재해야 한다

    # duration = time.time() - start
    # log_test_success(test_name, duration)
    print("✅ 이미 가입된 이메일 입력 시 에러 메시지 확인 테스트")

    # except Exception as e:
    #     duration = time.time() - start
    #     save_screenshot(driver, "signup_registered_email_fail")
    #     log_test_failure(test_name, str(e), duration)
    #     raise


# ======================================================
# TC-ME-011 회원가입 - 필수 약관 미동의 시 버튼 비활성화
# ======================================================
def test_signup_required_agreement_not_checked(driver):
    # test_name = "회원가입 - 필수 체크 미완료 시 버튼 비활성화 확인" #로그에 남길 테스트 이름
    # start = time.time() #테스트 시작 저장
    # log_test_start(test_name) #테스트 로그 기록 시작

    #try:
        wait = get_wait(driver) #요소가 나타날 때까지 기다리기
        go_to_signup_with_email(driver, wait) #사이트 접속 → Create account → Create account with email 이동

        # 기본 정보 입력
        wait.until(EC.visibility_of_element_located((By.NAME, "loginId"))).send_keys(
            "test_mem@mail.com"
        )
        wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(
            "Testtest1!"
        )
        wait.until(EC.visibility_of_element_located((By.NAME, "fullname"))).send_keys(
            "testuser"
        )

        # 약관 목록 아코디언 펼치기 (이미 열려 있으면 패스)
        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//svg[@data-icon='chevron-down']")
                )
            ).click()
        except Exception:
            pass #목록이 펼쳐진거면 넘어가기

        # Optional 선택 
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()=\"I'm 14 years or older.\"]]")
            )
        ).click()

        # Optional 선택
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()='[Optional] Receive updates and promotional emails.']]")
            )
        ).click()

        #Create account 버튼 찾고 “비활성화” 확인
        #버튼에 disabled 속성이 있으면 → 비활성화 상태 > 
        create_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create account')]")
            )
        )
        assert create_btn.get_attribute("disabled") is not None #이 버튼에는 disabled라는 속성이 실제로 존재해야 한다

        # duration = time.time() - start
        # log_test_success(test_name, duration)
        print("✅ 필수 체크 미완료 시 버튼 비활성화 테스트 확인")

    # except Exception as e:
    #     duration = time.time() - start
    #     save_screenshot(driver, "signup_required_agreement_fail")
    #     log_test_failure(test_name, str(e), duration)
    #     raise


