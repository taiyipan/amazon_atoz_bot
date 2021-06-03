from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credential import Credential
from email_interface import EmailInterface
import time

class Login:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://hub.amazon.work/shifts/dashboard'
        self.credential = Credential()
        self.interface = EmailInterface()
        print('Login initialized')

    def run(self):
        self.navigate_to_page()
        self.enter_username()
        self.enter_password()
        time.sleep(5)
        self.request_validation()
        time.sleep(7) # gives enough time to receive email code
        self.verify_identity()

    def navigate_to_page(self):
        self.driver.get(self.url)

    def enter_username(self):
        # locate username field
        username_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'login'
            ))
        )
        # enter username
        username_field.send_keys(self.credential.username())

    def enter_password(self):
        # locate password field
        password_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'password'
            ))
        )
        # enter password
        password_field.send_keys(self.credential.password() + '\n')

    def request_validation(self):
        # locate radio button
        radio_button = WebDriverWait(WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'selectPhone_form'
            ))
        ), 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/div[@class="form-group"]/div[2]/label/input'
            ))
        )
        # click radio button
        self.driver.execute_script("arguments[0].click();", radio_button)

        # locate continue_button
        continue_button = WebDriverWait(WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'selectPhone_form'
            ))
        ), 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                './/div[@class="form-buttons"]/button'
            ))
        )
        # click continue
        self.driver.execute_script("arguments[0].click();", continue_button)

    def verify_identity(self):
        # locate code field
        code_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((
                By.ID,
                'code'
            ))
        )
        # send validation code
        code_field.send_keys(self.interface.get_validation_code() + '\n')
