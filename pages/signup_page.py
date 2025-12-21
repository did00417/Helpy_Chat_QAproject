from selenium.webdriver.common.by import By

class SignupPage:
    """회원가입 페이지 관련 공통 기능 클래스"""

    def __init__(self, driver):
        self.driver = driver

    def input_username(self, username: str = ""):
        """아이디 입력창에 값 입력"""
        username_input = self.driver.find_element(By.NAME, "loginId")
        username_input.clear()
        username_input.send_keys(username)
        return username_input
