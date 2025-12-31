from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# 채팅 페이지 관련 공통 기능 클래스

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
        return self.driver.find_element(
        By.XPATH,
        '//*[@data-testid="arrow-upIcon"]/ancestor::button'
    )

    def send_message(self, message: str = ""):
        self.input_chat_message(message)
        self.click_send_button()
        return self.driver

    def wait_for_ai_reply(self):
        """AI 답변 대기 """
        reply = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.elice-aichat__markdown[data-status="complete"]')
                )
            )
        return reply
    
    def ai_reply_coniains_imge(self):
        """AI 답변에 이미지 포함 여부 확인"""
        reply_with_image = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.elice-aichat__markdown[data-status="complete"] img')
            )
        )
        return reply_with_image.is_displayed()

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
    
    # 고급 기능 관련 메서드
    
    def plus_Btn(self):
        '''플러스 버튼 클릭'''
        plusBtn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="plusIcon"]'))
        )
        plusBtn.click()
        return plusBtn
    
    def plus_menu_assert(self):
        '''플러스 메뉴 레이어 팝업 표시 여부 확인'''
        menu_layer = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[role="menu"]'))
        )
        return menu_layer
        
    def file_upload(self):
        '''파일 업로드 메뉴 클릭'''
        file_upload_Btn = self.wait.until(
            EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@data-testid="paperclipIcon"]/ancestor::*[@role="menuitem"]',
                )))
        file_upload_Btn.click()
        return file_upload_Btn
    
    def file_upload_select(self, file_path: str):
        '''파일 업로드 - 숨겨진 input[type=file] 요소에 파일 경로 전송'''
        file_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        file_input.send_keys(file_path)
        return file_input
    
    def click_upload_send_button(self):
        '''파일 업로드 후 전송 버튼 클릭'''
        send_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@data-testid="arrow-upIcon"]/ancestor::button')
            )
        )
        send_button.click()
        return send_button
    
    def click_image_icon(self):
        '''이미지 생성 아이콘 클릭'''
        image_icon = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="imageIcon"]')
            )
        )
        image_icon.click()
        return image_icon
    
    def web_search_Btn(self):
        '''웹 검색 메뉴 클릭'''
        web_search_Btn = self.wait.until(
            EC.element_to_be_clickable((
                    By.XPATH,
                    "//li[@role='menuitem'][.//span[text()='웹 검색']]",
                )))
        web_search_Btn.click()
        return web_search_Btn
    
    def uploaded_thumbnail_assert(self):
        '''업로드된 이미지 썸네일 표시 여부 확인'''
        thumbnail = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'div[data-variant="user"][type="image"] img'
                )
            )
        )
        return thumbnail.is_displayed()
    
    # 고급 기능 메서드 종료
    
    # 수정내용 관련 메서드 - 사용 안함
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
    
