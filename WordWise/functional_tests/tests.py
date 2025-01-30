
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_all_game_url_work(self):
        self.browser.get(self.live_server_url)
        # self.assertIn("Go to Flashcard Game", self.browser)
        # self.assertIn("Go to Crossword Game", self.browser)
        # self.assertIn("Go to Order Game", self.browser)

        link = self.browser.find_element(By.LINK_TEXT, "Go to Flashcard Game")  
        link.click()

        self.assertIn("flashcard", self.browser.page_source)
        self.assertIn("/flashcard/", self.browser.current_url) 

        self.browser.back()
        
        link = self.browser.find_element(By.LINK_TEXT, "Go to Crossword Game")  
        link.click()

        self.assertIn("crossword", self.browser.page_source)
        self.assertIn("/crossword/", self.browser.current_url) 

        self.browser.back()

        link = self.browser.find_element(By.LINK_TEXT, "Go to Order Game")  
        link.click()

        self.assertIn("ordergame", self.browser.page_source)
        self.assertIn("/ordergame/", self.browser.current_url) 

        self.browser.back()