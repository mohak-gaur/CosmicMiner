from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class RegisterPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, url):
        self.driver.get(url)

    def register(self, user, referral_code):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your Name']"))).send_keys(user["Name"])
        self.driver.find_element(By.ID, "email").send_keys(user["Email"])
        self.driver.find_element(By.XPATH, "//input[@placeholder='Enter your UserName']").send_keys(user["Name"])
        self.driver.find_element(By.ID, "password").send_keys(user["Password"])
        self.driver.find_element(By.ID, "confirm_password").send_keys(user["ConfirmPassword"])
        self.driver.find_element(By.ID, "referral_id").send_keys(referral_code)
        self.driver.find_element(By.ID, "remember").click()
        self.driver.find_element(By.ID, "Register").click()
