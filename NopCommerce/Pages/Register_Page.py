from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Locators.locators import RegisterPageLocators

class RegisterPage:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def inputGender(self):
        self.wait.until(EC.presence_of_element_located(RegisterPageLocators.Gender)).click()

    def inputFirstName(self,firstname):
        elem = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.FirstName))
        elem.clear()
        elem.send_keys(firstname)

    def inputLastName(self,lastname):
        elem = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.LastName))
        elem.clear()
        elem.send_keys(lastname)
        
    def inputEmail(self,email):
        elem = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.Email))
        elem.clear()
        elem.send_keys(email)
        
    def inputPassword(self,password):
        elem = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.Password))
        elem.clear()
        elem.send_keys(password)

    def confirmPassword(self,confpassword):
        elem = self.wait.until(EC.presence_of_element_located(RegisterPageLocators.ConfPassword))
        elem.clear()
        elem.send_keys(confpassword)
    
    def click_register(self):
        self.wait.until(EC.presence_of_element_located(RegisterPageLocators.RegisterButton)).click()
