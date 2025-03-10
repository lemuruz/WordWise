from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,random


class MultiUserFlashcardTest(StaticLiveServerTestCase):
    fixtures = ['flashcard/fixtures/flashcard_data.json',
                'flashcard/fixtures/user_data.json',
                'flashcard/fixtures/word_data.json',]

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_multiple_users_flashcard_access(self):
        # ปาร์คล็อกอิน
        self.browser.get(self.live_server_url + "/user/login/")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        submit_button = self.browser.find_element(By.ID, "submitLoginBtn")

        username_input.send_keys("park")
        password_input.send_keys("Park$194")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        alert.accept()

        time.sleep(1)

        # ปาร์คเข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด TOIC และ study item
        self.browser.get(self.live_server_url + "/flashcard/")
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "TOIC"))
        )
        toic_card = self.browser.find_element(By.ID, "TOIC")
        study_item_card = self.browser.find_element(By.ID, "study item")

        self.assertTrue(toic_card.is_displayed())
        self.assertTrue(study_item_card.is_displayed())
        time.sleep(1)

        # ปาร์คกด menu และล็อกเอาต์
        home_button = self.browser.find_element(By.ID, "homeBtn")
        home_button.click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "logout-btn"))
        )
        logout_button = self.browser.find_element(By.ID, "logout-btn")
        logout_button.is_displayed()
        logout_button.click()
        time.sleep(1)

        # best ล็อกอิน
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "login-btn"))
        )
        login_button = self.browser.find_element(By.ID,"login-btn")
        login_button.click()
        time.sleep(1)

        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        submit_button = self.browser.find_element(By.ID, "submitLoginBtn")

        username_input.send_keys("best")
        password_input.send_keys("Best$483")
        time.sleep(1)
        submit_button.click()
        time.sleep(1)

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        time.sleep(1)
        alert.accept()

        # best เข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด animal
        self.browser.get(self.live_server_url + "/flashcard/")
        animal_card = self.browser.find_element(By.ID, "animal")
        self.assertTrue(animal_card.is_displayed())
        time.sleep(1)

        # best ลองเล่น flashcard animal
        animal_card.click()
        time.sleep(1)
        # best เห็นคำว่า cat
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "wordDisplay"))
        )
        word_display = self.browser.find_element(By.ID, "wordDisplay")
        self.assertEqual(word_display.text, "1. cat")  # Check if the word is 'cat'
        time.sleep(0.5)

        # best จำได้ว่าคำนี้แปลว่าแมว

        # best กด ดูคำตอบและเห็นคำว่าแมว
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "showAnswer"))
        )
        showAnswerBtn = self.browser.find_element(By.ID, "showAnswer")
        time.sleep(0.5)
        showAnswerBtn.click()
        time.sleep(0.5)
        answer = self.browser.find_element(By.ID, "answer")
        self.assertIn("แมว", answer.text)  # Check if the translation is correct
        time.sleep(0.5)

        # best เห็นปุ่ม easy medium hard
        easyBtn = self.browser.find_element(By.ID, "easyBtn")
        mediumBtn = self.browser.find_element(By.ID, "mediumBtn")
        hardBtn = self.browser.find_element(By.ID, "hardBtn")
        easyBtn.is_displayed()
        mediumBtn.is_displayed()
        hardBtn.is_displayed()
        time.sleep(1)
        #best กด easy
        easyBtn.click()
        time.sleep(1)

        while True:
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.ID, "wordDisplay"))
            )
            word_display = self.browser.find_element(By.ID, "wordDisplay")
            
            self.assertTrue(word_display.is_displayed())
            time.sleep(0.5)

            # Click to show the answer
            showAnswerBtn = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.ID, "showAnswer"))
            )
            showAnswerBtn.click()
            time.sleep(0.5)

            # Proceed to the next word
            easyBtn.click()
            time.sleep(1)  # Optional sleep to avoid fast clicking that might cause errors

            # Check if we've reached the last word and end the loop
            successMessage = self.browser.find_element(By.ID,"Congratulationstext")
            if successMessage.is_displayed():
                time.sleep(1)
                # best เห็น text "Congratulations! You Have Finish this Flashcard"
                break



class FlashcardSelectionTest(StaticLiveServerTestCase):
    fixtures = ['flashcard/fixtures/flashcard_data.json',
                'flashcard/fixtures/user_data.json',
                'flashcard/fixtures/word_data.json',]

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_flashcard_word_selection_and_scoring(self):
        # เบสล็อกอินเข้าสู่ระบบ
        self.browser.get(self.live_server_url + "/user/login/")
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        submit_button = self.browser.find_element(By.ID, "submitLoginBtn")

        time.sleep(0.5)
        username_input.send_keys("park")
        time.sleep(0.5)
        password_input.send_keys("Park$194")
        time.sleep(0.5)
        submit_button.click()

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        time.sleep(1)
        alert.accept()

        # เบสเข้าไปที่หน้าแฟลชการ์ด
        self.browser.get(self.live_server_url + "/flashcard/")
        time.sleep(1)
        
        # เบสเห็นแฟลชการ์ดชุด TOIC และกดเข้าไป
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "TOIC"))
        )
        toic_card = self.browser.find_element(By.ID, "TOIC")
        self.assertTrue(toic_card.is_displayed())
        toic_card.click()
        time.sleep(1)

        # เบสเห็นคำแรกที่ยังไม่เคยเล่น
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "wordDisplay"))
        )
        word_display = self.browser.find_element(By.ID, "wordDisplay")
        self.assertTrue(word_display.is_displayed())
        time.sleep(1)

        # เบสกดดูคำแปล
        showAnswerBtn = self.browser.find_element(By.ID, "showAnswer")
        showAnswerBtn.click()
        time.sleep(1)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "answer"))
        )
        answer = self.browser.find_element(By.ID, "answer")
        self.assertTrue(answer.is_displayed())
        time.sleep(1)

        # เบสกด hard เพราะจำคำศัพท์ไม่ได้
        hardBtn = self.browser.find_element(By.ID, "hardBtn")
        hardBtn.click()
        time.sleep(1)

        # เบสเล่นต่อไปอีก 5 คำ
        for _ in range(5):
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "wordDisplay"))
            )
            
            # เบสกดดูคำแปล
            showAnswerBtn = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "showAnswer"))
            )
            time.sleep(0.5)
            showAnswerBtn.click()
            time.sleep(0.5)

            # เบสสุ่มกดปุ่มความยาก
            buttons = ['easyBtn', 'mediumBtn', 'hardBtn']
            selected_button = self.browser.find_element(By.ID, random.choice(buttons))
            selected_button.click()

        # เบสออกจากการเล่นแฟลชการ์ด
        time.sleep(1)
        menuBtn = self.browser.find_element(By.ID, "flashcardMenuBtn")
        menuBtn.click()
        time.sleep(1)

        # เบสเข้าเล่นแฟลชการ์ดชุด TOIC อีกครั้ง
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "TOIC"))
        )
        toic_card = self.browser.find_element(By.ID, "TOIC")
        toic_card.click()

        # เบสควรเห็นคำที่เคยตอบ hard อยู่ในชุดคำศัพท์ด้วย
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "wordDisplay"))
        )
        time.sleep(1)
        
        # เบสเล่นจนจบชุดคำศัพท์
        wordcount = 0
        while True:
            wordcount +=1
            time.sleep(0.3)
            word_display = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "wordDisplay"))
            )
            
            showAnswerBtn = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "showAnswer"))
            )
            showAnswerBtn.click()
            time.sleep(0.3)

            easyBtn = self.browser.find_element(By.ID, "easyBtn")
            easyBtn.click()
            
            success_messages = self.browser.find_elements(By.ID, "Congratulationstext")  # Returns a list

            if success_messages and success_messages[0].is_displayed():
                self.assertEqual(success_messages[0].text, "Congratulations! You Have Finish this Flashcard")
                break
        self.assertTrue(wordcount<=20)
        time.sleep(1)