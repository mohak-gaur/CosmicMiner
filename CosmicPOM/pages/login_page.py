from selenium.webdriver.common.by import By
from locators.login_locators import LoginLocators

class LoginPage:
    URL = "https://cosmiminer.in/owebest/website/signin.php"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, email, password):
        self.driver.find_element(By.ID, LoginLocators.EMAIL).send_keys(email)
        self.driver.find_element(By.ID, LoginLocators.PASSWORD).send_keys(password)
        self.driver.find_element(By.XPATH, LoginLocators.LOGIN_BTN).click()
