from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from unittest.mock import patch
from wordbank.models import wordBank
import time

class HangmanGameTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        # สร้าง server จำลอง 
        self.driver.get(self.live_server_url)
    def tearDown(self):
        self.driver.quit()

    def test_hangman_game(self):
        # สร้าง database จำลอง 
        wordBank.objects.create(word="BED", meaning="A piece of furniture for sleeping on")

        # ปาร์คกดเข้าลิงค์ Hangman game จากหน้าเมนู 
        time.sleep(1)
        hangman_link = self.driver.find_element(By.LINK_TEXT, "Hangman Game")
        hangman_link.click()

        # รอจนกว่าจะสร้างมีกล่อง class word 
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'word'))
        )
        
        # ปาร์คสังเกตเห็นว่ามีเส้นประ 3 เส้น มีปุ่มที่มีคำว่า Guess และ มีเห็นคำว่า Guessed Letters: None"
        label = self.driver.find_element(By.CSS_SELECTOR, "label[for='letter']")
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        word_display = self.driver.find_element(By.CLASS_NAME, 'word')
        guess_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.assertTrue(len(word_display.text.split()) == 3)  # 3-letter word
        self.assertTrue(word_display.text == "_ _ _")
        self.assertEqual(label.text, "Enter a letter:")  # ตรวจสอบข้อความใน label
        self.assertEqual(guessed_letters ,"Guessed Letters: None")
        self.assertIn("Guess",guess_button.text)

        # คำใบ้จาก database มาเทียบกับหน้า web ว่าตรงกันมั้ย
        word_obj = wordBank.objects.get(word="BED")
        expected_hint = word_obj.meaning
        hint = self.driver.find_element(By.CSS_SELECTOR, ".meaning").text
        self.assertEqual("Hint: "+expected_hint, hint)

        # ปาร์คใส่ตัวอักษร A และกดปุ่ม Guess
        input_field = self.driver.find_element(By.NAME, "letter")
        guess_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        time.sleep(1)
        input_field.send_keys("A")
        time.sleep(1)
        guess_button.click()

        # ปาร์คเห็นว่า Guessed Letters: จาก None กลายเป็น A และAttempts Left: เหลือ 5 
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text
        self.assertEqual("Guessed Letters: A", guessed_letters)
        self.assertEqual("Attempts Left: 5", attempts_left)
        time.sleep(1)

        # รอจนกว่า input field สำหรับกรอกตัวอักษรจะพร้อมใช้งานอีกครั้ง
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 

        # ส่ปาร์คใส่ตัวอักษร E และกดปุ่ม Guess
        input_field.send_keys("E")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        time.sleep(1)          
        guess_button.click()
        word_display = self.driver.find_element(By.CLASS_NAME, 'word')
        guessed_letters = self.driver.find_element(By.ID, "guess").text
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text
        self.assertEqual("Guessed Letters: A E", guessed_letters)
        self.assertEqual("Attempts Left: 5", attempts_left)
        self.assertTrue(word_display.text == "_ E _")
        
        # ตัวอักษรที่ต้องการเดาต่อให้ครบคำว่า "BED"
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 

        # ปาร์คใส่ตัว B 
        input_field.send_keys("B")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        time.sleep(0.5)
        guess_button.click()

        # ปาร์คใส่ตัว D 
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("D")
        time.sleep(0.5)
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()

        # ปาร์คเห็นข้อความ 🎉 Congratulations! You won! 🎉
        message =  self.driver.find_element(By.CLASS_NAME,"message")
        self.assertEqual("🎉 Congratulations! You won! 🎉",message.text)
        time.sleep(2)

         # ทดสอบว่ามีปุ่ม Start New Game มั้ย
        start_button = self.driver.find_element(By.CSS_SELECTOR, "button#restart")
        self.assertEqual("Start New Game",start_button.text);

        # เปลี่ยนคำใน database 
        wordBank.objects.all().delete() 
        wordBank.objects.create(word="WE", meaning="Referring to the speaker and others")

        # ปาร์คกดปุ่ม Start New Game 
        start_button.click()
        time.sleep(1)
        # รอจนกว่าจะมี element ที่มี class word ปรากฏ ในที่นี้ก็คือ word_display 
        new_word = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'word'))
        )
        word_obj = wordBank.objects.get(word="WE")
        expected_hint = word_obj.meaning

        hint = self.driver.find_element(By.CSS_SELECTOR, ".meaning").text
        # ปาร์คสังเกตได้ว่ามีเส้นประ 2 ช่อง และคำใบ้เปลี่ยนไปเป็นคำว่า Hint: Referring to the speaker and others 
        self.assertEqual("Hint: "+expected_hint, hint)
        self.assertEqual(new_word.text,"_ _")
        time.sleep(1)

        # ปาร์คลองใส่ตัว A , B , C ปรากฏว่าไม่ถูกเลยทำให้ attempts_left เหลือ 3 

        #  ------------------A--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("A")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        time.sleep(0.5)   
        # ------------------B--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("B")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        time.sleep(0.5)   
        # ------------------C--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("C")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        attempts_left = self.driver.find_element(By.CSS_SELECTOR, ".attempts").text

        # เทสว่า attempts_left เหลือ 3 จริงป่าว 
        self.assertEqual(attempts_left ,"Attempts Left: 3")
        time.sleep(1)   

        # ปาร์คลองใส่ตัว A ปรากฏว่ามีการเเจ้งเตือนว่า 'You already guessed that letter!'
        input_field = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "letter"))
        )
        input_field.send_keys("A")
        time.sleep(0.5)

        # ปาร์คกดปุ่ม Guess
        guess_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        # รอจนกว่าข้อความแจ้งเตือนจะปรากฏ
        alert_message = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "message"))
        )

        # ตรวจสอบว่าข้อความแจ้งเตือนถูกต้อง
        self.assertEqual(alert_message.text, "You already guessed that letter!")
        time.sleep(2)
        
        # ปาร์คลองใส่ "ก" ปรากฏว่ามีการแจ้งเตือนว่า 'Please enter a valid single letter!'
        input_field = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "letter"))
        )
        input_field.send_keys("ก")
        time.sleep(0.5)

        # ปาร์คกดปุ่ม Guess
        guess_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        # รอจนกว่าข้อความแจ้งเตือนจะปรากฏ
        alert_message = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.NAME, "letter"))
        )
        input_field.clear()
        time.sleep(1)

        
        # ตรวจสอบว่าข้อความแจ้งเตือนถูกต้อง
        self.assertEqual(alert_message.get_attribute("title"), "Please enter a valid single English letter (A-Z)!")
        time.sleep(1)
        # ปาร์คลองใส่อักษรที่เหลือคือ D , Z , T ปรากฏว่าไม่ถูกเลยทำให้ attempts_left เหลือ 0 และขึ้นข้อความ "😢 Game Over! The word was: WE"
        
        #  ------------------D--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("D")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        time.sleep(1)   
        # ------------------Z--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("Z")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        time.sleep(1)   
        # ------------------T--------------------
        input_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "letter"))
        ) 
        input_field.send_keys("T")
        guess_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        guess_button.click()
        attempts_left = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,".attempts"))
        ).text

        # เทสว่า attempts_left เหลือ 0 จริงป่าว 
        self.assertEqual(attempts_left ,"Attempts Left: 0")
        time.sleep(1) 
        # ปาร์คเห็นข้อความ "😢 Game Over! The word was: WE"
        message =  self.driver.find_element(By.CLASS_NAME,"message")
        self.assertEqual("😢 Game Over! The word was: WE",message.text)
        time.sleep(2)
        # ปาร์คเห็นปุ่มที่มีคำว่า Back to menu และกดปุ่ม ทำให้ปาร์คกลับมาอยู่ในหน้าเมนูและเห็นลิงค์ Hangman Game
        back = self.driver.find_element(By.CLASS_NAME,"back_to_menu")
        self.assertEqual(back.text,"Back to menu")
        back.click()
        time.sleep(1)
        hangman_link = self.driver.find_element(By.LINK_TEXT, "Hangman Game")
        self.assertIsNotNone(hangman_link) 
        time.sleep(1)