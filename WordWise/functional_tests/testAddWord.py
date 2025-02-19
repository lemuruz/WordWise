from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Changed from LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from wordbank.models import wordBank


class HangmanGameTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        
        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)
    def tearDown(self):
        self.driver.quit()

    def testAddWord(self):
        add_button = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "add-word"))
    )
        add_button.click()
        word_input =  self.driver.find_element(By.ID ,"word").send_keys("cookie")
        word_type_select = Select(self.driver.find_element(By.ID, "word_type"))
        word_type_select.select_by_visible_text("Noun")
        word_mean_input = self.driver.find_element(By.ID , "word_mean").send_keys("คุกกี้")
        word_clue_input = self.driver.find_element(By.ID , "word_clue").send_keys('dessert that flavor sweet')
        
        submit_btn  = WebDriverWait(self.driver , 10).until(
            EC.presence_of_element_located((By.CLASS_NAME ,"submit"))
    )
        submit_btn.click()
        word_exist = wordBank.objects.filter(word="cookie").exists()
        self.assertTrue(word_exist,"cookie is in database")
        