from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        password_input.send_keys("1234")
        submit_button.click()

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        alert.accept()

        # ปาร์คเข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด TOIC และ study item
        self.browser.get(self.live_server_url + "/flashcard/")
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "TOIC"))
        )
        toic_card = self.browser.find_element(By.ID, "TOIC")
        study_item_card = self.browser.find_element(By.ID, "study item")

        self.assertTrue(toic_card.is_displayed())
        self.assertTrue(study_item_card.is_displayed())

        # ปาร์คกด menu และล็อกเอาต์
        home_button = self.browser.find_element(By.ID, "homeBtn")
        home_button.click()
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "logout-btn"))
        )
        logout_button = self.browser.find_element(By.ID, "logout-btn")
        logout_button.is_displayed()
        logout_button.click()

        # best ล็อกอิน
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "login-btn"))
        )
        login_button = self.browser.find_element(By.ID,"login-btn")
        login_button.click()

        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        submit_button = self.browser.find_element(By.ID, "submitLoginBtn")

        username_input.send_keys("best")
        password_input.send_keys("5678")
        submit_button.click()

        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        alert.accept()

        # best เข้าลิงค์แฟลชการ์ด และเห็นแฟลชการ์ด animal
        self.browser.get(self.live_server_url + "/flashcard/")
        animal_card = self.browser.find_element(By.ID, "animal")
        self.assertTrue(animal_card.is_displayed())

        # best ลองเล่น flashcard animal
        animal_card.click()
        # best เห็นคำว่า cat
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, "wordDisplay"))
        )
        word_display = self.browser.find_element(By.ID, "wordDisplay")
        self.assertEqual(word_display.text, "1. cat")  # Check if the word is 'cat'

        # best จำได้ว่าคำนี้แปลว่าแมว

        # best กด ดูคำตอบและเห็นคำว่าแมว
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "showAnswer"))
        )
        showAnswerBtn = self.browser.find_element(By.ID, "showAnswer")
        showAnswerBtn.click()
        answer = self.browser.find_element(By.ID, "answer")
        self.assertIn("แมว", answer.text)  # Check if the translation is correct

        # best เห็นปุ่ม easy medium hard
        easyBtn = self.browser.find_element(By.ID, "easyBtn")
        mediumBtn = self.browser.find_element(By.ID, "mediumBtn")
        hardBtn = self.browser.find_element(By.ID, "hardBtn")
        easyBtn.is_displayed()
        mediumBtn.is_displayed()
        hardBtn.is_displayed()
        #best กด easy
        easyBtn.click()

        while True:
            # Make sure the word and answer appear correctly
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "wordDisplay"))
            )
            word_display = self.browser.find_element(By.ID, "wordDisplay")
            
            self.assertTrue(word_display.is_displayed())

            # Click to show the answer
            showAnswerBtn = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.ID, "showAnswer"))
            )
            showAnswerBtn.click()

            # Proceed to the next word
            easyBtn.click()
            time.sleep(1)  # Optional sleep to avoid fast clicking that might cause errors

            # Check if we've reached the last word and end the loop
            successMessage = self.browser.find_element(By.ID,"Congratulationstext")
            if successMessage.is_displayed():
                # best เห็น text "Congratulations! You Have Finish this Flashcard"
                break

