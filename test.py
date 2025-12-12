from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, logging

def get_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    return driver

def admin_login(driver):
    wait = WebDriverWait(driver, 20)
    driver.get("https://cosmiminer.in/owebest/website/admin/login.php")
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    username_input.send_keys("cosmipower")
    password_input.send_keys("bgHxQ4MkrziTpbq")
    login_button = driver.find_element(By.XPATH, "//button[@class='btn btn-login']")
    login_button.click()
    time.sleep(2)

def mark_completed_on_page(driver, page_num):
    """Goes to a specific page number and marks all as completed"""
    url = f"https://cosmiminer.in/owebest/website/admin/planwiseuser.php?page={page_num}&per_page=100"
    driver.get(url)
    wait = WebDriverWait(driver, 15)

    try:
        # Wait for table to load
        wait.until(EC.presence_of_element_located((By.ID, "selectAllPW")))
        checkbox = driver.find_element(By.ID, "selectAllPW")

        # Scroll safely to view and adjust for header
        driver.execute_script("arguments[0].scrollIntoView(false);", checkbox)
        driver.execute_script("window.scrollBy(0, -100)")
        time.sleep(0.5)

        # Click via JS to avoid interception
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        # Click mark completed
        driver.find_element(By.XPATH, "//button[@onclick=\"prepareBulkPW('completed')\"]").click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='confirmBulkPW()']"))).click()
        time.sleep(2)
        logging.info(f"✅ Page {page_num} marked completed successfully.")

        return True

    except Exception as e:
        logging.warning(f"⚠️ Skipping page {page_num}: {e}")
        return False

def main():
    driver = get_driver(headless=False)
    try:
        admin_login(driver)

        # Loop over pages dynamically
        page = 1
        consecutive_fails = 0
        MAX_FAILS = 3  # stop if 3 consecutive pages not found

        while True:
            success = mark_completed_on_page(driver, page)
            if not success:
                consecutive_fails += 1
                if consecutive_fails >= MAX_FAILS:
                    logging.info("No more valid pages found, stopping.")
                    break
            else:
                consecutive_fails = 0

            page += 1  # move to next page
            time.sleep(1)

    finally:
        driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    main()