from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from user.models import Account
import time

class UserStoryTest(StaticLiveServerTestCase):
    fixtures = ['flashcard/fixtures/flashcard_data.json',
                'flashcard/fixtures/user_data.json',
                'flashcard/fixtures/word_data.json',]
    
    def setUp(self):
        self.browser = webdriver.Chrome()  # Use Firefox() if preferred

    def tearDown(self):
        self.browser.quit()

    def test_user_registration_and_login(self):
        # ปาร์คกดลิงค์ login
        self.browser.get(self.live_server_url + "/user/login/")

        # ปาร์คเห็นช่องใส่ชื่อ และ รหัสผ่าน และลิงค์ no account? make one!
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        register_link = self.browser.find_element(By.LINK_TEXT, "No account? Make one!")

        self.assertTrue(username_input.is_displayed())
        self.assertTrue(password_input.is_displayed())
        self.assertTrue(register_link.is_displayed())
        time.sleep(1)

        # ปาร์คกด no account? make one!
        register_link.click()
        time.sleep(1)

        # ปาร์คเห็นหัวข้อ register
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        heading = self.browser.find_element(By.TAG_NAME, "h2")
        self.assertEqual(heading.text, "Register")

        # ปาร์คกรอกชื่อ(best) และรหัส(1234)
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        confirm = self.browser.find_element(By.ID , "confirmPassword")
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        username_input.send_keys("best")
        time.sleep(0.5)
        password_input.send_keys("Best$483")
        time.sleep(0.5)
        confirm.send_keys("Best$483")
        time.sleep(0.5)
        submit_button.click()
        time.sleep(1)

        # ปาร์คเห็นว่ามีข้อความขึ้นเตือนว่า Username already exists
        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Username already exists")
        time.sleep(1)
        alert.accept()  # ปาร์คกด OK

        # ปาร์คกรอกชื่อ(sigma) และรหัส(1234)
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        confirm = self.browser.find_element(By.ID , "confirmPassword")
        submit_button = self.browser.find_element(By.TAG_NAME, "button")
        time.sleep(1)
        
        username_input.clear()
        password_input.clear()
        confirm.clear()
        username_input.send_keys("sigma")
        time.sleep(0.5)
        password_input.send_keys("Sigma@467")
        time.sleep(0.5)
        confirm.send_keys("Sigma@467")
        time.sleep(0.5)
        submit_button.click()

        # ปาร์คเห็นว่ามีข้อความขึ้นเตือนว่า "User registered successfully!"
        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "User registered successfully!")
        time.sleep(1)
        alert.accept()  # ปาร์คกด OK

        # Wait for the alert to be dismissed before getting cookies
        WebDriverWait(self.browser, 5).until_not(EC.alert_is_present())
        
        # Now it's safe to get cookies
        cookies = self.browser.get_cookies()

        # Navigate back to login page before adding cookies
        self.browser.get(self.live_server_url + "/user/login/")

        # Apply stored cookies
        for cookie in cookies:
            self.browser.add_cookie(cookie)

        # Reload the login page again after adding cookies
        self.browser.get(self.live_server_url + "/user/login/")

        # ปาร์คกรอกชื่อ(sigma) และรหัส(1234)
        username_input = self.browser.find_element(By.ID, "username")
        password_input = self.browser.find_element(By.ID, "password")
        submit_button = self.browser.find_element(By.TAG_NAME, "button")

        username_input.send_keys("sigma")
        time.sleep(0.5)
        password_input.send_keys("Sigma@467")
        time.sleep(0.5)
        submit_button.click()
        time.sleep(1)
        
        # ปาร์คเห็นคำว่า Login successful!
        WebDriverWait(self.browser, 5).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        self.assertEqual(alert.text, "Login successful!")
        time.sleep(1)
        alert.accept()  # ปาร์คกด OK

        # ปาร์คเห็นว่า Logged in as: sigma
        user_label = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "user-label"))
        )
        self.assertEqual(user_label.text, "👤 sigma")
        time.sleep(1)