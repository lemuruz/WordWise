
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from flashcard.models import flashCardDeck

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        self.browser = webdriver.Chrome()

        decks = flashCardDeck.objects.all()
        print("Available decks:", [deck.name for deck in decks])

    def tearDown(self):
        self.browser.quit()

    def test_all_game_url_work(self):
        self.browser.get(self.live_server_url)
        # self.assertIn("Go to Flashcard Game", self.browser)
        # self.assertIn("Go to Crossword Game", self.browser)
        # self.assertIn(-เขียน FUNCTIONAL TESTS ในส่วนการทดสอบแอพ FLASHCARD "Go to Order Game", self.browser)

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

    def test_flashcard_game(self):
        # 1. ปาร์คเปิดหน้าแรกของเว็บไซต์
        self.browser.get(self.live_server_url)

        # 2. ปาร์คคลิกที่ลิงก์ "Go to Flashcard Game" เพื่อเข้าสู่เกมแฟลชการ์ด
        self.browser.find_element(By.LINK_TEXT, "Go to Flashcard Game").click()
        self.assertIn("Choose Your Flashcard Deck", self.browser.page_source)

        # 3. ปาร์คเห็นตัวเลือก verybasic,study และเลือก verybasic
        verybasic_button = self.browser.find_element(By.ID, "deck_1")
        self.assertTrue(verybasic_button.is_displayed())
        study_button = self.browser.find_element(By.ID, "deck_2")
        self.assertTrue(study_button.is_displayed())
        #เลือก verybasc
        verybasic_button.click()
        
        self.assertIn("flashcard/play", self.browser.current_url)
        # 4. ปาร์คเห็นคำศัพท์ "cat" และปุ่ม "ดูคำตอบ"
        # word_element = self.browser.find_element(By.ID, "flashcard-word")
        # self.assertIn("cat"||"dog", word_element.text)
        
        # 5. ปาร์คนึกได้ว่าคำนี้แปลว่าแมว และ กด “ดูคำตอบ” 
        # show_answer_button = self.browser.find_element(By.ID, "show-answer")
        # show_answer_button.click()

        # 6. ปาร์คเห็นคำว่าแมว ทำให้เค้ารู้ว่าเข# 4. ปาร์คเห็นคำศัพท์ "cat" และปุ่ม "ดูคำตอบ"
        # word_element = self.browser.find_element(By.ID, "flashcard-word")
        # self.assertIn("cat", word_element.text)
        
        # 5. ปาร์คนึกได้ว่าคำนี้แปลว่าแมว และ กด “ดูคำตอบ” 
        # show_answer_button = self.browser.find_element(By.ID, "show-answer")
        # show_answer_button.click()

        # 6. ปาร์คเห็นคำว่าแมว ทำให้เค้ารู้ว่าเขาจำคำนี้ได้
        # answer_element = self.browser.find_element(By.ID, "flashcard-answer")
        # self.assertIn("แมว", answer_element.text)

        # 7. ปาร์คเห็นปุ่มให้คะแนน(1:ง่าย 2:ปานกลาง 3:ยาก) และตัดสินใจกด "ง่าย"
        # rate_easy_button = self.browser.find_element(By.ID, "rate-1")
        # rate_easy_button.click()

        # 8. ปาร์คทำซ้ำแบบนี้จนครบ 20 ข้อ
        # for _ in range(19):
        #     show_answer_button = self.browser.find_element(By.ID, "show-answer")
        #     show_answer_button.click()

        #     rate_easy_button = self.browser.find_element(By.ID, "rate-1")
        #     rate_easy_button.click()
        #     time.sleep(0.5)  # หน่วงเวลาเล็กน้อย เพื่อให้สมจริงเหมือนผู้ใช้จริง

        # 9. ปาร์คกดปุ่มเช็คคะแนน
        # check_score_button = self.browser.find_element(By.ID, "check-score")
        # check_score_button.click()

        # 9. ปาร์คเห็นคะแนนรวมของเขาในหน้าผลลัพธ์
        # score_element = self.browser.find_element(By.ID, "final-score")
        # self.assertTrue("Your Score:" in score_element.text)
