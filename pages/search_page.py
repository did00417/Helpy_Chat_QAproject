from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SearchPage:
    
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 30)
        self.driver = driver
    
    # 검색 버튼 클릭
    def magnifier_click(self):
        magnifier_btn= self.driver.find_element(By.CSS_SELECTOR, '[data-testid="magnifying-glassIcon"]')
        magnifier_btn.click()
        return magnifier_btn
    
    def is_search_bar_visible(self):
        visible_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
        return visible_bar   
    
    # 검색어 입력
    def search_word_send(self, word:str):
        search_box = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
        search_box.send_keys(word)
        return search_box
    
    # 히스토리 목록 확인
    def history_list(self):
        history_items = self.driver.find_elements(
            By.XPATH, '//div[@role="dialog"]//a[contains(@href, "/ai-helpy-chat/chats/")]')
        return history_items
