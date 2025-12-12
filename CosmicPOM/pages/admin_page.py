from selenium.webdriver.common.by import By
from locators.admin_locators import AdminLocators

class AdminPage:
    URL = "https://cosmiminer.in/owebest/website/admin/login.php"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login(self, user, pwd):
        self.driver.find_element(By.ID, AdminLocators.ADMIN_USER).send_keys(user)
        self.driver.find_element(By.ID, AdminLocators.ADMIN_PASS).send_keys(pwd)
        self.driver.find_element(By.XPATH, AdminLocators.ADMIN_LOGIN_BTN).click()

    def go_to_planwise(self):
        self.driver.find_element(By.XPATH, AdminLocators.PLANWISE_MENU).click()

    def click_next_page(self):
        self.driver.find_element(By.XPATH, AdminLocators.NEXT_BTN).click()

    def select_all(self):
        self.driver.find_element(By.ID, AdminLocators.CHECKBOX_ALL).click()

    def mark_completed(self):
        self.driver.find_element(By.XPATH, AdminLocators.MARK_COMPLETE_BTN).click()
        self.driver.find_element(By.XPATH, AdminLocators.CONFIRM_BTN).click()
