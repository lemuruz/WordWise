
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from ordergame.models import sentences

MAX_WAIT = 10

class orderword_is_functional(StaticLiveServerTestCase):
    fixtures = ["ordergame/fixtures/sentence_data.json"]

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_orderword(self):
        # 1. -หลังจากที่ปาร์คได้ทดสอบความรู้แล้วปาร์คต้องการเรียนรู้ Grammar เพื่อสื่อสารดยการกดลิงค์ go to ordergame
        self.browser.get(self.live_server_url+"/ordergame/test")
        
        # Check if JavaScript is loaded
        is_js_loaded = self.browser.execute_script("return document.readyState") == "complete"
        self.assertTrue(is_js_loaded, "JavaScript did not fully load")

        

        # 2. มีคำแสดงขึ้นบนหน้าเว็บมีคำว่า violin, play, I และมีช่องว่างในส่วนด้านบน และมีปุ่มเขียนว่า OK มุมล่างขวา
        words = self.browser.find_element(By.ID, "word-line")
        children = words.find_elements(By.XPATH, './*') #XPATH is some type of query lang for selecting nodes in XML
        self.assertEqual(len(children), 4, "number of initial words not equal to 4")
        contain_words = {
            "I" : False,
            "play" : False,
            "violin" : False,
            "." : False
        }
        for child in children:
            contain_words[child.text.strip()] = True
        for word in contain_words.keys():
            self.assertTrue(contain_words[word], f"Word \"{word}\" is not showing")

        sentence_space = self.browser.find_element(By.ID, "blank-blocks")
        self.assertTrue(sentence_space.is_displayed(), "Space for sentence not visible")

        OK_button = self.browser.find_element(By.ID, "check-btn")
        self.assertTrue(OK_button.is_displayed(), "OK button not visible")

        #3.ปาร์คกดไปที่คำว่า I I แสดงในช่องแรก ปาร์คกดคำว่า play คำว่า play แสดงในช่องที่2 ปาร์คกดคำว่า violin คำว่า violin แสดงในช่องที่ 3 ปาร์คกดคำว่า . . แสดงในช่องที่ 4
        words.find_element(By.XPATH, "./*[text()='I']").click()                            #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 1, "number of words in sentence should be 1")    #
        self.assertEqual(word_in_sen[0].text, "I", "not displayed word \"I\"")              #
                                                                                            #
        words.find_element(By.XPATH, "./*[text()='play']").click()                         #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 2, "number of words in sentence should be 2")    #
        self.assertEqual(word_in_sen[1].text, "play", "not displayed word \"play\"")        #
                                                                                            # May change to check the word dynamically
        words.find_element(By.XPATH, "./*[text()='violin']").click()                       #              (For whole test)
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 3, "number of words in sentence should be 3")    #
        self.assertEqual(word_in_sen[2].text, "violin", "not displayed word \"violin\"")    #
                                                                                            #
        words.find_element(By.XPATH, "./*[text()='.']").click()                            #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 4, "number of words in sentence should be 4")    #
        self.assertEqual(word_in_sen[3].text, ".", "not displayed word \".\"")              #

        #ปาร์คกดปุ่มที่เขียนว่า OK
        OK_button.click()

        #หน้าจอแสดงข้อความ “ถูกต้อง”
        popup = self.browser.find_element(By.ID, "popup")
        self.assertTrue(popup.is_displayed(), "popup not showing after pressing OK")
        popup_text = popup.find_element(By.ID, "popup-message")
        self.assertIn("✅ Correct!", popup_text.text, "Not showing correct even the sentence is correct.")

    def test_addwordpage(self):
        #Navigate to add_sentence page
        self.browser.get(self.live_server_url+"/ordergame/game")
        add_sentence_link = self.browser.find_element(By.LINK_TEXT, "help us add more sentence")
        add_sentence_link.click()

        #Add sentence "I like ordergame"
        sentence_box = self.browser.find_element(By.ID, "data")
        submit_button = self.browser.find_element(By.ID, "submit-btn")

        sentence_box.send_keys("I like ordergame.")
        submit_button.click()
        time.sleep(2)

        I_like_ordergame = sentences.objects.filter(sentence="I like ordergame.").exists()
        self.assertTrue(I_like_ordergame, "I like ordergame not added to database")

        #Show "thank you" - popup
        thank_you = self.browser.find_element(By.ID, "popup")
        self.assertTrue(thank_you.is_displayed(), "thank_you not showing")
        re_adding = self.browser.find_element(By.ID, "popup-close")
        re_adding.click()

        #Add sentence "I play ordergame"
        sentence_box = self.browser.find_element(By.ID, "data")
        submit_button = self.browser.find_element(By.ID, "submit-btn")

        sentence_box.send_keys("I play ordergame.")
        submit_button.click()
        time.sleep(2)

        I_play_ordergame = sentences.objects.filter(sentence="I play ordergame.").exists()
        self.assertTrue(I_play_ordergame, "I play ordergame not added to database")