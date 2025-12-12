from pages.login_page import LoginPage
from config.credentials import USER_EMAIL, USER_PASS

def test_user_login_valid(driver):
    lp = LoginPage(driver)
    lp.open()
    lp.login(USER_EMAIL, USER_PASS)
    assert driver.current_url != lp.URL
