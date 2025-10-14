from selenium.webdriver.support.ui import WebDriverWait
from core.driver_manager import get_driver
from pages.register_page import RegisterPage
from pages.dashboard_page import DashboardPage
from pages.admin_page import AdminPage
import config, logging, time

def register_and_upgrade(user, parent_ref, headless=False):
    driver = get_driver(headless=False)
    wait = WebDriverWait(driver, 20)
    try:
        reg = RegisterPage(driver, wait)
        dash = DashboardPage(driver, wait)
        admin = AdminPage(driver, wait, config)

        reg.open(config.REGISTER_URL)
        reg.register(user, parent_ref)
        # small wait for post-registration flow
        time.sleep(2)
        dash.setup_pin_and_onboarding()
        dash.checkbox()
        dash.close_popup()
        dash.start_mining()
        new_ref = dash.extract_referral()
        dash.back_to_dashboard()
        plan_id = dash.upgrade_plan()
        # confirm on admin panel
        if plan_id:
            admin.confirm_latest_order()
        logging.info(f"Registered {user.get('Email')} -> {new_ref} (plan={plan_id})")
        return new_ref, plan_id
    except Exception as e:
        logging.error('registration failed', exc_info=True)
        return None, None
    finally:
        try:
            driver.quit()
        except Exception:
            pass
