from selenium.webdriver.common.by import By

class Login_Page_Locators:
        email = (By.NAME , "email")
        password = (By.NAME , "password")
        remember_me = (By.ID , "remember")
        login = (By.ID , "login-btn")
        invalid_creds = (By.XPATH , "//div[@class = 'toast show error']")

class Close_PopUp:
        dont_show = (By.CSS_SELECTOR , "input#dontShowAgain")
        close_popup = (By.ID , "closePopup")

class Start_Mining:
        start_button = (By.ID , "startMiningBtn")
        mining_status_xpath = (By.XPATH , "//div[@class='mining-status active']")
        time_left = (By.ID , "serverTimeLeft")