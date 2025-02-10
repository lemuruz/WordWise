import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # Changed from LiveServerTestCase
from flashcard.models import flashCardDeck
from user.models import Account

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):  # Changed to StaticLiveServerTestCase
    fixtures = ['test_data.json']
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        # Ensure the test data is loaded before printing
        self.setUpClass()
        decks = flashCardDeck.objects.all()
        print("Available decks:", [deck.name for deck in decks])
        Account.objects.create(username="best", password="1234")

    def tearDown(self):
        self.browser.quit()


    def test_flashcard_game(self):
        # 1. ปาร์คเปิดหน้าแรกของเว็บไซต์
        self.browser.get(self.live_server_url)

        # 2. ปาร์คคลิกที่ลิงก์ "Go to Flashcard Game" เพื่อเข้าสู่เกมแฟลชการ์ด
        self.browser.find_element(By.LINK_TEXT, "Flashcard Game").click()
        self.assertIn("Choose Your Flashcard Deck", self.browser.page_source)

        # 3. ปาร์คเห็นตัวเลือก study_item,animal และเลือก study_item
        animal = self.browser.find_element(By.ID, "animal")
        self.assertTrue(animal.is_displayed())
        study_item = self.browser.find_element(By.ID, "study item")
        self.assertTrue(study_item.is_displayed())
        #เลือก verybasc
        study_item.click()
        
        self.assertIn("flashcard/play", self.browser.current_url)
        # 4. ปาร์คเห็นคำศัพท์ "school" และปุ่ม "ดูคำตอบ"
        word_element = self.browser.find_element(By.ID, "wordDisplay")
        self.assertIn("school", word_element.text)
        
        # 5. ปาร์คนึกได้ว่าคำนี้แปลว่าโรงเรียน และ กด “ดูคำตอบ” 
        show_answer_button = self.browser.find_element(By.ID, "showAnswer")
        show_answer_button.click()

        # 6. ปาร์คเห็นคำว่าโรงเรียน ทำให้เค้ารู้ว่าเขาจำคำนี้ได้ 
        word_element = self.browser.find_element(By.ID, "answer")
        self.assertIn("โรงเรียน", word_element.text)
        

        # 7. ปาร์คเห็นปุ่มให้คะแนน(1:ง่าย 2:ปานกลาง 3:ยาก) และตัดสินใจกด "ง่าย"
        easy = self.browser.find_element(By.ID, "easyBtn")
        medium = self.browser.find_element(By.ID, "mediumBtn")
        self.assertTrue(medium.is_displayed())
        hard = self.browser.find_element(By.ID, "hardBtn")
        self.assertTrue(hard.is_displayed())
        easy.click()

        # 8. ปาร์คทำซ้ำแบบนี้จนครบ 4 ข้อ
        for _ in range(3):
            show_answer_button = self.browser.find_element(By.ID, "showAnswer")
            show_answer_button.click()

            rate_easy_button = self.browser.find_element(By.ID, "easyBtn")
            rate_easy_button.click()
            time.sleep(0.5)  # หน่วงเวลาเล็กน้อย เพื่อให้สมจริงเหมือนผู้ใช้จริง

        # ----ยกเลิก
        # 9. ปาร์คเห็นคะแนนรวมของเขาในหน้าผลลัพธ์
        # score_element = self.browser.find_element(By.ID, "userScore")
        # self.assertTrue("score : 12 / 12" in score_element.text)
        #-----

        #9. ปาร์คพอใจกับคะแนนของเขา และเขาเห็นปุ่ม home เข้าจึงลองกดดู
        home_button = self.browser.find_element(By.ID, "homeBtn")
        home_button.click()

        #10. ปาร์คเห็นหน้า home
        self.assertIn("Choose Your Flashcard Deck", self.browser.page_source)

# from django.contrib.staticfiles.testing import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from user.models import Account
# from flashcard.models import flashCardDeck

# class MultiUserFlashcardTest(LiveServerTestCase):
#     def setUp(self):
#         self.browser = webdriver.Chrome()
        
#         animal_deck = flashCardDeck.objects.create(name='animal')
#         toic_deck = flashCardDeck.objects.create(name='TOIC')
#         study_item_deck = flashCardDeck.objects.create(name='study item')

#         park = Account.objects.create(username="park", password="1234")
#         best = Account.objects.create(username="best", password="5678")

#         park.flashcard.add(toic_deck, study_item_deck)
#         best.flashcard.add(animal_deck)
        

#     def tearDown(self):
#         self.browser.quit()

#     def test_multiple_users_flashcard_access(self):
#         # ปาร์คล็อกอิน
#         self.browser.get(self.live_server_url + "/user/login/")
#         username_input = self.browser.find_element(By.ID, "username")
#         password_input = self.browser.find_element(By.ID, "password")
#         submit_button = self.browser.find_element(By.TAG_NAME, "Login")

#         username_input.send_keys("park")
#         password_input.send_keys("1234")
#         submit_button.click()

#         WebDriverWait(self.browser, 5).until(EC.alert_is_present())
#         alert = self.browser.switch_to.alert
#         self.assertEqual(alert.text, "Login successful!")
#         alert.accept()

#         # ปาร์คเข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด TOIC และ study item
#         self.browser.get(self.live_server_url + "/flashcard/")
#         WebDriverWait(self.browser, 5).until(
#             EC.presence_of_element_located((By.ID, "TOIC"))
#         )
#         toic_card = self.browser.find_element(By.ID, "TOIC")
#         study_item_card = self.browser.find_element(By.ID, "study item")

#         self.assertTrue(toic_card.is_displayed())
#         self.assertTrue(study_item_card.is_displayed())

#         # ปาร์คกด menu และล็อกเอาต์
#         home_button = self.browser.find_element(By.TAG_NAME, "menu")
#         home_button.click()
#         logout_button = self.browser.find_element(By.ID, "logout-btn")
#         logout_button.click()

#         WebDriverWait(self.browser, 5).until(EC.alert_is_present())
#         alert = self.browser.switch_to.alert
#         self.assertEqual(alert.text, "Logged out successfully!")
#         alert.accept()

#         # best ล็อกอิน
#         username_input = self.browser.find_element(By.ID, "username")
#         password_input = self.browser.find_element(By.ID, "password")
#         submit_button = self.browser.find_element(By.TAG_NAME, "Login")

#         username_input.send_keys("best")
#         password_input.send_keys("5678")
#         submit_button.click()

#         WebDriverWait(self.browser, 5).until(EC.alert_is_present())
#         alert = self.browser.switch_to.alert
#         self.assertEqual(alert.text, "Login successful!")
#         alert.accept()

#         # best เข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด animal
#         self.browser.get(self.live_server_url + "/flashcard/")
#         animal_card = self.browser.find_element(By.ID, "animal")
#         self.assertTrue(animal_card.is_displayed())
