from pages.admin_page import AdminPage
from config.credentials import ADMIN_EMAIL, ADMIN_PASS

def test_admin_login_valid(driver):
    ap = AdminPage(driver)
    ap.open()
    ap.login(ADMIN_EMAIL, ADMIN_PASS)
    assert driver.current_url != ap.URL
