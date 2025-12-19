# from selenium.webdriver.common.by import By
# from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD


# class LoginPage:
#     """로그인 페이지 관련 공통 기능 클래스"""

#     def __init__(self, driver):
#         self.driver = driver

#     def input_username(self, username: str = ""):
#         """아이디 입력창에 값 입력"""
#         username_input = self.driver.find_element(By.NAME, "loginId")
#         username_input.clear()
#         username_input.send_keys(username)
#         return username_input

#     def input_password(self, password: str = ""):
#         """비밀번호 입력창에 값 입력"""
#         password_input = self.driver.find_element(By.NAME, "password")
#         password_input.clear()
#         password_input.send_keys(password)
#         return password_input

#     def click_login_button(self):
#         """로그인 버튼 클릭"""
#         login_button = self.driver.find_element(
#             By.CSS_SELECTOR, 'button[type="submit"]'
#         )
#         login_button.click()
#         return login_button

#     def login(self):
#         self.input_username(TEST_LOGIN_ID)
#         self.input_password(TEST_LOGIN_PASSWORD)
#         self.click_login_button()
#         return self.driver
    
#테스트 케이스 : TC-ME-001
#test_login_success.py

from selenium.webdriver.common.by import By #요소 찾을 때 (name,xpath,css etc)
from selenium.webdriver.support import expected_conditions as EC #expected conditions 조건이 나타날때까지 기다려라 

from utils.helper import get_wait, LOGIN_URL #logfin_url 가져오는거


class LoginPage: #로그인틀
    def __init__(self, driver):#로그인 객체 생성
        self.driver = driver #pytest에서 넘겨받은 브라우저
        self.wait = get_wait(driver) #페이지 나올 때까지 기달리기 

    # ================================
    # 요든 요소 위치 요기에 모아두기! 위치 변경되면 여기만 수정
    # ================================
    EMAIL_INPUT = (By.NAME, "loginId") #이메일 텍스트 박스
    PASSWORD_INPUT = (By.NAME, "password") #비밀번호 텍스트 박스 
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]") #로그인 버튼

    # ================================
    # 기능!
    # ================================
    
    #로그인 페이지 이동
    def open(self):
        self.driver.get(LOGIN_URL)

    #이메일 입력하기 
    def enter_email(self, email: str):
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT)) #이메일 텍스트박스 나올 때까지 기달리기
        email_input.clear()
        email_input.send_keys(email) 

    #비밀번호 입력하기
    def enter_password(self, password: str):
        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    #위에 이메일/비밀번호/클릭을 모아둠 
    #다른 페이지에서 로그인 필요한 경우 아래 3줄 입력하면 됨
    #from pages.login_page import LoginPage
    #login_page = LoginPage(driver)
    #login_page.open() < 페이지 이동이 필요한 경우 
    #login_page.login(email, password) < 이미 로그인 페이지인 경우
    
    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()


