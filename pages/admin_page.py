from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class AdminPage:
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config

    def confirm_latest_order(self):
        self.driver.get(self.config.ADMIN_URL)
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(self.config.ADMIN_USERNAME)
        self.driver.find_element(By.ID, "password").send_keys(self.config.ADMIN_PASSWORD)
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-login']").click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href = 'planwiseuser.php']"))).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "(//button[@class='action-btn btn-edit'])[1]").click()
        self.wait.until(EC.presence_of_element_located((By.NAME, "status"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value='completed']"))).click()
        logging.info("Payment status has been updated to 'Completed'")
        # self.driver.find_element(By.XPATH, "//option[@value='completed']").click()
        self.driver.find_element(By.NAME, "update_status").click()
