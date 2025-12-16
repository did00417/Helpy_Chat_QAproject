from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class ChatPage:
    """채팅 페이지 관련 공통 기능 클래스"""

    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 30)
        self.driver = driver

    def input_chat_message(self, message: str):
        """채팅 메시지 입력"""
        input_box = self.driver.find_element(By.NAME, "input")
        input_box.clear()
        input_box.send_keys(message)
        return input_box

    def click_send_button(self):
        send_button = self.driver.find_element(
            By.XPATH, '//*[@data-testid="arrow-upIcon"]/ancestor::button'
        )
        send_button.click()
        return send_button
    
    def send_button_assert(self):
        send_button = self.driver.find_element(
        By.XPATH,
        '//*[@data-testid="arrow-upIcon"]/ancestor::button'
    )
        assert not send_button.is_enabled(), "스페이스 입력시 전송 버튼 활성화"


    def send_message(self, message: str = ""):
        self.input_chat_message(message)
        self.click_send_button()
        return self.driver

    def wait_for_ai_reply(self):
        """AI 답변 대기 div -> span으로 수정"""
        reply = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'span[data-status="complete"]')
            )
        )
        return reply

    def click_copy_button(self, reply_element):
        """복사 버튼 클릭 테스트"""
        copy_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="copyIcon"]')
        copy_btn.click()
        return copy_btn

    def paste_to_input_box(self, reply_element):
        """입력창에 붙여넣기"""
        input_box = self.driver.find_element(By.NAME, "input")
        input_box.clear()
        input_box.send_keys(Keys.CONTROL, "v")
        return input_box.get_attribute("value").strip()

    def copy_and_paste(self, reply_element):
        """복사 및 붙여넣기"""
        self.click_copy_button(reply_element)
        value = self.paste_to_input_box(reply_element)
        return value
    
    def puls_Btn(self):
        '''플러스 버튼 클릭'''
        plusBtn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="plusIcon"]'))
        )
        plusBtn.click()
        return plusBtn
        
    def file_upload(self):
        '''파일 업로드 메뉴 클릭'''
        file_upload_Btn = self.wait.until(
            EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@data-testid="paperclipIcon"]/ancestor::*[@role="menuitem"]',
                )))
        file_upload_Btn.click()
        return file_upload_Btn
    
    # 수정내용 관련 메서드
    def hover_update_message(self):
        update_hover = self.driver.find_element(By.XPATH,
        '//span[@data-status="complete" and contains(text(), "홍길동")]/ancestor::div[contains(@class, "MuiPaper-root")]')
        ActionChains(self.driver).move_to_element(update_hover).perform()
        return update_hover
    
    def click_update_button(self):
        update_Btn = self.driver.find_element(By.XPATH,
    '//button[contains(@aria-label, "수정")]')
        update_Btn.click()
        return update_Btn
        
    def update_message(self, u_message:str):
        update_box = self.driver.find_element(By.XPATH,
        '//from[.//textarea[@name = "input"]]')
        update_box.click()
        update_box.send_keys(Keys.CONTROL, "a")
        update_box.send_keys(Keys.BACKSPACE)
        update_box.send_keys(u_message)
        return update_box
    
    def update_send_btn(self):
        update_send_Btn = self.driver.find_element(By.XPATH, '//button[contains(text(), "보내기")]')
        update_send_Btn.click()
        return update_send_Btn
    
    def test(self):
        print("안녕하세요")