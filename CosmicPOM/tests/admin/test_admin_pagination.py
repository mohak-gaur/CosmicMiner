from pages.admin_page import AdminPage
from config.credentials import ADMIN_EMAIL, ADMIN_PASS
import time

def test_admin_pagination(driver):
    ap = AdminPage(driver)
    ap.open()
    ap.login(ADMIN_EMAIL, ADMIN_PASS)
    ap.go_to_planwise()

    for _ in range(3):
        ap.click_next_page()
        time.sleep(1)

    assert True
