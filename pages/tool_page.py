from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ToolPage:
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 30)
        self.driver = driver
        
    def click_tool(self):
        tool_Btn = self.driver.find_element(
            By.CSS_SELECTOR, 
            '[data-icon="screwdriver-wrench"]'
            )
        tool_Btn.click()
        return tool_Btn
    
    # 세부 특기 사항
    def open_detail_note(self):
        detail_Btn = self.driver.find_element(
            By.CSS_SELECTOR, 
            '[data-ai-tool-ident="student_evaluation"]'
            )
        detail_Btn.click()
        return detail_Btn
    
    # 세부 특기사항 클릭 후 form 내부 검증
    def get_detail_note(self):
        return self.wait.until(
        EC.presence_of_element_located(
            (By.ID, "tool-factory-student_evaluation")
        )
    )
    
    # 행동특성 및 종합의견 페이지 클릭
    def open_behavior_summary_page(self):
        behavior_Btn = self.driver.find_element(
            By.CSS_SELECTOR, 
            '[data-ai-tool-ident="student_record_generation"]'
            )
        behavior_Btn.click()
        return behavior_Btn
    
    # 행특 및 종합의견 클릭 후 form 내부 검증
    def get_behavior_summary(self):
        return self.wait.until(
            EC.presence_of_element_located(
            (By.ID, "tool-factory-student_record_generation")
        )
    )

    # 수업 지도안 클릭
    def open_lesson_plan(self):
        plan_Btn = self.driver.find_element(
            By.CSS_SELECTOR, 
            '[data-ai-tool-ident="syllabus_generation"]'
            )
        plan_Btn.click()
        return plan_Btn
    
    # 수업 지도안 클릭 후 form 내부 검증
    def get_lesson_plan(self):
        return self.wait.until(
            EC.presence_of_element_located(
            (By.ID, "tool-factory-syllabus_generation")
        )
    )
    
    # # PPT 생성 카드 클릭
    def open_ppt_generation_card(self):
        ppt_Btn = self.driver.find_element(
            By.CSS_SELECTOR, 
            '[data-testid="presentation-screenIcon"]'
            )
        ppt_Btn.click()
        return ppt_Btn
    
    def get_ppt_generation(self):
        return self.wait.until(
            EC.presence_of_element_located(
            (By.ID, "tool-factory-create_pptx")
        )
    )

#--------------------------------------------------------

    def input_ppt_content(self, title: str, instructions:str , slides:int, section:int):
        
        ppt_title_input = self.driver.find_element(By.NAME, "topic")
        ppt_title_input.send_keys(Keys.CONTROL, "a")
        ppt_title_input.send_keys(Keys.BACKSPACE)
        ppt_title_input.send_keys(title)
        
        ppt_Instructions_input = self.driver.find_element(By.NAME, "instructions")
        ppt_Instructions_input.send_keys(Keys.CONTROL, "a")
        ppt_Instructions_input.send_keys(Keys.BACKSPACE)
        ppt_Instructions_input.send_keys(instructions)
        
        ppt_slide_input = self.driver.find_element(By.NAME, "slides_count")
        ppt_slide_input.send_keys(Keys.CONTROL, "a")
        ppt_slide_input.send_keys(Keys.BACKSPACE)
        ppt_slide_input.send_keys(slides)
        
        ppt_section_input = self.driver.find_element(By.NAME, "section_count")
        ppt_section_input.send_keys(Keys.CONTROL, "a")
        ppt_section_input.send_keys(Keys.BACKSPACE)
        ppt_section_input.send_keys(section)
        
        checkbox = self.driver.find_element(By.CSS_SELECTOR, 'input[name="simple_mode"]')
        if checkbox.is_selected():
            ActionChains(self.driver).move_to_element(checkbox).click().perform()
        
        return (ppt_title_input, ppt_Instructions_input, 
                ppt_slide_input, ppt_section_input)
        
    # 입력칸 작성 후 클릭하는 메서드(클릭 누른 후에 또 클릭 버튼 뜸 그것과 별개)
    def get_generate_button(self):
        return self.driver.find_element(
            By.XPATH, 
            "//button[@type='submit' and @form='tool-factory-create_pptx' and normalize-space()='다시 생성']"
            ).click()
    
    def again_generate_click(self):
        """
        '결과 다시 생성하기' 모달의 '다시 생성' 버튼 클릭
        """
        # 모달 내 버튼이 나타날 때까지 대기
        again_btn = self.wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 
                'div[role="dialog"] button[form="tool-factory-create_pptx"]'
            ))
        )
        again_btn.click()
        return again_btn
    
    # 다시 생성 버튼 검증용
    def again_btn_assert(self):
        return self.driver.find_element(
            By.XPATH, 
            '//button[normalize-space()="다시 생성"]')
        
    # 다운로드 버튼 검증용
    def wait_downlord_button(self, timeout=180):
        downlord_btn = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@href, '.pptx') and normalize-space()='생성 결과 다운받기']"
                    )
                )
            )
        return downlord_btn
            

            
            
        