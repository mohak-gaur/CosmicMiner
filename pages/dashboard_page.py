from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, random, string
import config

class DashboardPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait   

    def setup_pin_and_onboarding(self):
        # create pin
        for i in range(1,5):
            pin_box = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@oninput='moveToNext(this, {i})']")))
            self.driver.execute_script("arguments[0].removeAttribute('readonly');", pin_box)
            pin_box.send_keys('0')
            time.sleep(0.2)
        try:
            self.driver.find_element(By.ID, "nextBtn").click()
        except Exception:
            pass
        # confirm pin
        try:
            for i in range(1,5):
                pin_box = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@oninput='moveToNextConfirm(this, {i})']")))
                self.driver.execute_script("arguments[0].removeAttribute('readonly');", pin_box)
                pin_box.send_keys('0')
                time.sleep(0.2)
            self.driver.find_element(By.ID, "setPinBtn").click()
            
            time.sleep(2)
        except Exception:
            pass
        # close popups if exist

    def checkbox(self):
        try:
            # Sometimes "don't show again" checkbox appears first
            dont_show = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#dontShowAgain")))
            dont_show.click()
        except Exception:
            pass

    def close_popup(self):
        try:      
            xyz = self.wait.until(EC.element_to_be_clickable((By.ID, "closePopup")))
            xyz.click()
            time.sleep(0.5)
        except Exception:
            pass
        # try:
        #     popup_close = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='closePopup']")))
        #     popup_close.click()
        #     time.sleep(1)        

    def extract_referral(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='referrals.php']"))).click()
            val = self.wait.until(EC.presence_of_element_located((By.ID, "referralLink"))).get_attribute("value")
            from urllib.parse import urlparse, parse_qs
            return parse_qs(urlparse(val).query).get('ref', [None])[0]
        except Exception:
            return None
        
    def back_to_dashboard(self):
        try:
            back_but = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='dashboard.php']")))
            back_but.click()
        except Exception:
            pass

    def upgrade_plan(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='upgrade_gpc.php']"))).click()
            plan_id = random.randint(1,4)
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(@onclick,'plan_id={plan_id}')]")))
            btn.click()
            time.sleep(1)
            txn = ''.join(random.choices(string.ascii_letters, k=8))
            self.wait.until(EC.presence_of_element_located((By.ID, "modal-txn-hash"))).send_keys(txn)
            self.wait.until(EC.element_to_be_clickable((By.ID, "modal-submit"))).click()
            return plan_id
        except Exception:
            return None
