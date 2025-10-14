from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, random, string, logging
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
            upgrade_nav = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='upgrade_gpc.php']")))
            upgrade_nav.click()

        # choose a random plan id between 1 and 4
            plan_id = random.randint(1, 4)
            random_package_locator = f"//button[contains(@onclick , 'plan_id={plan_id}')]"
            upgrade_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, random_package_locator)))
            upgrade_button.click()

            time.sleep(1)  # allow modal/plan details to appear
        # read plan amount text
            plan_range = self.driver.find_element(By.XPATH, "//div[@class='plan-range']").text
            logging.info(f"Selected plan range text: {plan_range}")

            amount_lookup = {
                '30.000 USDT': 80,
                '101.000 USDT': 200,
                '251.000 USDT': 800,
                '1001.000 USDT': 4500
            }
            set_amount = ''
            for key, val in amount_lookup.items():
                if key in plan_range:
                    set_amount = val
                    break

            if set_amount != '':
                try:
                    logging.info(f"Setting amount to {set_amount}")
                    amt_input = self.wait.until(EC.presence_of_element_located((By.ID, "amount")))
                    amt_input.clear()
                    amt_input.send_keys(str(set_amount))
                except Exception as e:
                    logging.warning(f"Couldn't set the amount input: {e}")
                # pass

        # Click pay now
            self.wait.until(EC.element_to_be_clickable((By.ID, "pay-now-btn"))).click()
            time.sleep(1)

        # generate random txn hash and submit
            txn_hash = ''.join(random.choices(string.ascii_letters, k=8))
            logging.info(f"Submitting fake transaction hash: {txn_hash}")
            self.wait.until(EC.presence_of_element_located((By.ID, "modal-txn-hash"))).send_keys(txn_hash)
            self.wait.until(EC.element_to_be_clickable((By.ID, "modal-submit"))).click()

        # wait a little for modal to close / success message
            time.sleep(2)
            logging.info("Plan upgrade flow completed (client-side) — awaiting admin confirmation.")
            return plan_id
        except Exception as e:
            logging.error(f"Error during perform_plan_upgrade: {e}", exc_info=True)
            # return False