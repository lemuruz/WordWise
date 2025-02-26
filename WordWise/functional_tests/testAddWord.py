from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from wordbank.models import wordBank
import time
class HangmanGameTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def testAddWord(self):
        # คลิกที่ปุ่มเพิ่มคำ
        add_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-word"))
        )
        add_button.click()

        # กรอกข้อมูลคำ
        word_input = self.driver.find_element(By.ID, "word")
        word_input.send_keys("cookie")

        # เลือกประเภทของคำ
        word_type_select = Select(self.driver.find_element(By.ID, "word_type"))
        word_type_select.select_by_visible_text("Noun")

        # กรอกความหมาย
        word_mean_input = self.driver.find_element(By.ID, "word_mean")
        word_mean_input.send_keys("คุกกี้")

        # กรอกคำใบ้
        word_clue_input = self.driver.find_element(By.ID, "word_clue")
        word_clue_input.send_keys('dessert that flavor sweet')

        # คลิกปุ่ม submit
        submit_btn = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit"))
        )
        submit_btn.click()

        # ตรวจสอบว่าเพิ่มคำใหม่สำเร็จ
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())

        # ตรวจสอบข้อความใน alert
        alert_message = alert.text
        self.assertEqual(alert_message, "Word added successfully!")  # ปรับข้อความตามที่คุณคาดหวังใน alert

        # ยืนยันการปิด alert
        alert.accept()

        # ตรวจสอบว่าเพิ่มคำใหม่สำเร็จในฐานข้อมูล
        word_exist = wordBank.objects.filter(word="cookie").exists()
        self.assertTrue(word_exist, "cookie should be in database")

        # ตรวจสอบคำที่ถูกเพิ่มมีข้อมูลที่ถูกต้องในฐานข้อมูล
        word = wordBank.objects.get(word="cookie")
        self.assertEqual(word.word_type, "noun")
        self.assertEqual(word.meaning, "dessert that flavor sweet")
        self.assertEqual(word.translates, "คุกกี้")

    def testAddWordWithSameWord(self):
        # เพิ่มคำแรกที่ชื่อ 'cookie'
        wordBank.objects.create(word='cookie', word_type='noun', meaning='dessert that flavor sweet', translates='คุกกี้')

        add_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-word"))
        )
        add_button.click()
        
        # กรอกข้อมูลคำที่ซ้ำกับคำที่มีอยู่แล้ว
        word_input = self.driver.find_element(By.ID, "word")
        word_input.send_keys("cookie")

        word_type_select = Select(self.driver.find_element(By.ID, "word_type"))
        word_type_select.select_by_visible_text("Verb")

        word_mean_input = self.driver.find_element(By.ID, "word_mean")
        word_mean_input.send_keys("คุกกี้")

        word_clue_input = self.driver.find_element(By.ID, "word_clue")
        word_clue_input.send_keys('dessert that flavor sweet')

        submit_btn = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit"))
        )
        submit_btn.click()

        # ตรวจสอบว่ามีข้อความแจ้งเตือนว่า คำนี้มีอยู่แล้ว
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())

        # ตรวจสอบข้อความใน alert
        alert_message = alert.text
        self.assertEqual(alert_message, "This word and meaning already exist!")  # ปรับข้อความตามที่คุณคาดหวังใน alert

        # ยืนยันการปิด alert
        alert.accept()

        self.assertEqual(wordBank.objects.filter(word='cookie').count(), 1)  # คำ 'tear' ไม่เพิ่มซ้ำ
        self.assertEqual(wordBank.objects.filter(word='cookie', word_type='noun').count(), 1)  
        self.assertEqual(wordBank.objects.filter(word='cookie', word_type='verb').count(), 0)  
        

 

