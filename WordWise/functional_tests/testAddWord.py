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
        # ปาร์คเห็นปุ่มเพิ่มคำในหน้า menu จึงกดเข้าไป
        add_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-word"))
        )
        time.sleep(1)
        add_button.click()
        time.sleep(1)

        # ปาร์คใส่คำว่า cookie ในช่องใส่คำ
        word_input = self.driver.find_element(By.ID, "word")
        word_input.send_keys("cookie")
        time.sleep(0.5)

        # ปาร์คเลือกว่า cookie เป็นคำ Noun
        word_type_select = Select(self.driver.find_element(By.ID, "word_type"))
        word_type_select.select_by_visible_text("Noun")
        time.sleep(0.5)

        # เพราะปาร์คเป็นคนไทย ปาร์คเลยใส่ในช่องคำแปลว่า คุกกี้
        word_mean_input = self.driver.find_element(By.ID, "word_mean")
        word_mean_input.send_keys("คุกกี้")
        time.sleep(0.5)

        # ปาร์คค่อนข้างฉลาดเขาเลยสามารถใส่คำใบ้ภาษาอังกฤษได้ด้วยว่า dessert that flavor sweet
        word_clue_input = self.driver.find_element(By.ID, "word_clue")
        word_clue_input.send_keys('dessert that flavor sweet')
        time.sleep(0.5)

        # ปาร์คคลิกปุ่ม submit
        submit_btn = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit"))
        )
        submit_btn.click()
        time.sleep(1)

        # ตรวจสอบว่าเพิ่มคำใหม่สำเร็จ
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())

        # ปาร์คเห็นข้อความใน alert ว่า Word added successfully!
        alert_message = alert.text
        self.assertEqual(alert_message, "Word added successfully!")
        time.sleep(1)

        # ปิด alert
        alert.accept()

        # ตรวจสอบว่าเพิ่มคำใหม่สำเร็จในฐานข้อมูล
        word_exist = wordBank.objects.filter(word="cookie").exists()
        self.assertTrue(word_exist, "cookie should be in database")

        # ตรวจสอบคำที่ถูกเพิ่มมีข้อมูลที่ถูกต้องในฐานข้อมูล
        word = wordBank.objects.get(word="cookie")
        self.assertEqual(word.word_type, "noun")
        self.assertEqual(word.meaning, "dessert that flavor sweet")
        self.assertEqual(word.translates, "คุกกี้")
        time.sleep(1)

    def testAddWordWithSameWord(self):
        # มีคำว่า cookie อยู่แล้วใน database (อาจเป็นคำที่ปาร์คเพิ่มเข้าไปก็ได้!) ปาร์คเห็นปุ่มให้เพิ่มคำจึงกดเข้าไป
        wordBank.objects.create(word='cookie', word_type='noun', meaning='dessert that flavor sweet', translates='คุกกี้')

        add_button = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "add-word"))
        )
        time.sleep(1)
        add_button.click()
        time.sleep(1)
        
        # ปาร์คลืมว่าเคยเพิ่ม cookie ลงไปในคลังคำศัพท์แล้วก็กรอกข้อมูลตามเดิมลงไป
        word_input = self.driver.find_element(By.ID, "word")
        word_input.send_keys("cookie")
        time.sleep(0.5)

        word_type_select = Select(self.driver.find_element(By.ID, "word_type"))
        word_type_select.select_by_visible_text("Verb")
        time.sleep(0.5)

        word_mean_input = self.driver.find_element(By.ID, "word_mean")
        word_mean_input.send_keys("คุกกี้")
        time.sleep(0.5)

        word_clue_input = self.driver.find_element(By.ID, "word_clue")
        word_clue_input.send_keys('dessert that flavor sweet')
        time.sleep(0.5)

        submit_btn = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit"))
        )
        submit_btn.click()
        time.sleep(1)

        # ตรวจสอบว่ามีข้อความแจ้งเตือนว่า คำนี้มีอยู่แล้ว
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())

        # Alert บอกปาร์คว่ามีคำนี้ใน database อยู่แล้ว
        alert_message = alert.text
        self.assertEqual(alert_message, "This word and meaning already exist!")  # ปรับข้อความตามที่คุณคาดหวังใน alert
        time.sleep(1)

        # ยืนยันการปิด alert
        alert.accept()

        self.assertEqual(wordBank.objects.filter(word='cookie').count(), 1)  # คำ 'tear' ไม่เพิ่มซ้ำ
        self.assertEqual(wordBank.objects.filter(word='cookie', word_type='noun').count(), 1)  
        self.assertEqual(wordBank.objects.filter(word='cookie', word_type='verb').count(), 0)  
        time.sleep(1)