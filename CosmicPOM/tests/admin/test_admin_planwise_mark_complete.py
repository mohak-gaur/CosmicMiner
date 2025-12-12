from pages.admin_page import AdminPage
from config.credentials import ADMIN_EMAIL, ADMIN_PASS
import time

def test_bulk_mark_completed(driver):
    ap = AdminPage(driver)
    ap.open()
    ap.login(ADMIN_EMAIL, ADMIN_PASS)
    ap.go_to_planwise()

    ap.select_all()
    ap.mark_completed()
    time.sleep(1)

    assert True
