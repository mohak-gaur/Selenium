from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import LoginPageLocators


class LoginPage:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def inputEmail(self,username):
        elem = self.wait.until(EC.presence_of_element_located(LoginPageLocators.Email))
        elem.clear()
        elem.send_keys(username)

    def inputPassword(self,password):
        elem = self.wait.until(EC.presence_of_element_located(LoginPageLocators.Password))
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        self.wait.until(EC.presence_of_element_located(LoginPageLocators.LoginButton)).click()