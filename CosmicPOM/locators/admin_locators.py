class AdminLocators:
    ADMIN_USER = "username"
    ADMIN_PASS = "password"
    ADMIN_LOGIN_BTN = "//button[@type='submit']"

    PLANWISE_MENU = "//a[@href='planwiseuser.php']"
    NEXT_BTN = "//a[contains(text(),'Next')]"
    CHECKBOX_ALL = "selectAllPW"
    MARK_COMPLETE_BTN = "//button[@onclick="prepareBulkPW('completed')"]"
    CONFIRM_BTN = "//button[@onclick='confirmBulkPW()']"
