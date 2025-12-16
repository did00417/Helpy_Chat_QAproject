from selenium.webdriver.common.by import By
from utils.constants import TEST_LOGIN_ID, TEST_LOGIN_PASSWORD


class LoginPage:
    """로그인 페이지 관련 공통 기능 클래스"""

    def __init__(self, driver):
        self.driver = driver

    def input_username(self, username: str = ""):
        """아이디 입력창에 값 입력"""
        username_input = self.driver.find_element(By.NAME, "loginId")
        username_input.clear()
        username_input.send_keys(username)
        return username_input

    def input_password(self, password: str = ""):
        """비밀번호 입력창에 값 입력"""
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)
        return password_input

    def click_login_button(self):
        """로그인 버튼 클릭"""
        login_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        login_button.click()
        return login_button

    def login(self):
        self.input_username(TEST_LOGIN_ID)
        self.input_password(TEST_LOGIN_PASSWORD)
        self.click_login_button()
        return self.driver
    

