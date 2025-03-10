
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
        self.browser.get(self.live_server_url)
        ordergamelink = self.browser.find_element(By.ID, "ordergamelink")
        time.sleep(0.5)
        ordergamelink.click()
        self.assertEqual(self.live_server_url+"/ordergame/game/", self.browser.current_url)
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
        time.sleep(1)

        #3.ปาร์คกดไปที่คำว่า I I แสดงในช่องแรก ปาร์คกดคำว่า play คำว่า play แสดงในช่องที่2 ปาร์คกดคำว่า violin คำว่า violin แสดงในช่องที่ 3 ปาร์คกดคำว่า . . แสดงในช่องที่ 4
        words.find_element(By.XPATH, "./*[text()='I']").click()                            #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 1, "number of words in sentence should be 1")    #
        self.assertEqual(word_in_sen[0].text, "I", "not displayed word \"I\"")              #
        time.sleep(1)
                                                                                            #
        words.find_element(By.XPATH, "./*[text()='play']").click()                         #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 2, "number of words in sentence should be 2")    #
        self.assertEqual(word_in_sen[1].text, "play", "not displayed word \"play\"")        #
        time.sleep(1)
                                                                                            # May change to check the word dynamically
        words.find_element(By.XPATH, "./*[text()='violin']").click()                       #              (For whole test)
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 3, "number of words in sentence should be 3")    #
        self.assertEqual(word_in_sen[2].text, "violin", "not displayed word \"violin\"")    #
        time.sleep(1)
                                                                                            #
        words.find_element(By.XPATH, "./*[text()='.']").click()                            #
        word_in_sen = sentence_space.find_elements(By.TAG_NAME, "div")                      #
        self.assertEqual(len(word_in_sen), 4, "number of words in sentence should be 4")    #
        self.assertEqual(word_in_sen[3].text, ".", "not displayed word \".\"")              #
        time.sleep(1)

        #ปาร์คกดปุ่มที่เขียนว่า OK
        OK_button.click()
        time.sleep(1)

        #หน้าจอแสดงข้อความ “ถูกต้อง”
        popup = self.browser.find_element(By.ID, "popup")
        self.assertTrue(popup.is_displayed(), "popup not showing after pressing OK")
        popup_text = popup.find_element(By.ID, "popup-message")
        self.assertIn("✅ Correct!", popup_text.text, "Not showing correct even the sentence is correct.")
        time.sleep(1)

        #ปาร์คกดคำว่า Home เพื่อกลับไปที่หน้าแรก
        home_btn = self.browser.find_element(By.ID, "popup-home")
        home_btn.click()
        time.sleep(1)
        self.assertIn(self.live_server_url, self.browser.current_url)
        self.assertEqual(self.browser.title, "Menu")

    def test_addwordpage(self):
        #เริ่มต้นจากหน้า ordergame/game เห็นข้อความว่า help us add more sentence ด้านบน
        self.browser.get(self.live_server_url+"/ordergame/game")
        add_sentence_link = self.browser.find_element(By.LINK_TEXT, "help us add more sentence")
        time.sleep(1)
        add_sentence_link.click()

        #เห็นช่องสำหรับใส่ข้อความและปุ่ม submit button
        sentence_box = self.browser.find_element(By.ID, "data")
        submit_button = self.browser.find_element(By.ID, "submit-btn")

        #ใส่คำว่า I like ordergame. ลงไปในช่อง แล้วกดปุ่ม submit
        sentence_box.send_keys("I like ordergame.")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        I_like_ordergame = sentences.objects.filter(sentence="I like ordergame.").exists()
        self.assertTrue(I_like_ordergame, "I like ordergame not added to database")

        #เห็น popup แสดงความขอบคุณขึ้นมาและถามว่าต้องการใส่ข้อมูลเพิ่มไหม เห็นปุ่มใส่ข้อมูลอีกครั้งจึงกด
        thank_you = self.browser.find_element(By.ID, "popup")
        self.assertTrue(thank_you.is_displayed(), "thank_you not showing")
        thankyou_msg = self.browser.find_element(By.ID, "popup-thank-msg")
        resubmit_msg = self.browser.find_element(By.ID, "popup-resubmit-msg")
        self.assertEqual(thankyou_msg.text, "Thanks For Helping Us Add Create New Content")
        self.assertEqual(resubmit_msg.text, "Do you want to submit more sentence?")
        re_adding = self.browser.find_element(By.ID, "popup-close")
        self.assertEqual(re_adding.text, "Yes")
        re_adding.click()
        time.sleep(1)

        #ใส่ I play ordergame. ลงไปในช่องว่างแล้วกด submit อีกครั้ง
        sentence_box = self.browser.find_element(By.ID, "data")
        submit_button = self.browser.find_element(By.ID, "submit-btn")

        sentence_box.send_keys("I play ordergame.")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        I_play_ordergame = sentences.objects.filter(sentence="I play ordergame.").exists()
        self.assertTrue(I_play_ordergame, "I play ordergame not added to database")
        time.sleep(1)

        #เห็น popup แสดงความขอบคุณอีกครั้ง พึงพอใจแล้วจึงกดปุ่ม Home แล้วก็เห็นว่ากลับไปหน้าแรกแล้ว
        thank_you = self.browser.find_element(By.ID, "popup")
        self.assertTrue(thank_you.is_displayed(), "thank_you not showing")
        home_btn = self.browser.find_element(By.ID, "popup-home")
        self.assertEqual(home_btn.text, "HOME")
        home_btn.click()
        time.sleep(1)

        self.assertIn(self.live_server_url, self.browser.current_url)
        self.assertEqual(self.browser.title, "Menu")