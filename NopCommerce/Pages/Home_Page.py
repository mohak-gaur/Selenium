from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Locators.locators import HomePageLocators

class HomePage:
    def __init__(self,driver):
        self.wait = WebDriverWait(driver,10)
        self.driver = driver
    
    def Register(self):
        self.wait.until(EC.presence_of_element_located(HomePageLocators.Register)).click()


    def Login(self):
        self.wait.until(EC.presence_of_element_located(HomePageLocators.Login)).click()