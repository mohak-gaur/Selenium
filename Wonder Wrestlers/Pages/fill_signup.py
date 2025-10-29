from Utils.waiting import get_element_when_visible
from Utils.utils import setup_logging
from Locators.signupFormLoc import SignUp_Form_Locators
from selenium.webdriver.common.by import By
from Utils.utils import (USERNAME, FULLNAME, EMAIL, DATEOFBIRTH, PHONENUMBER, UPLOADIDPATH, PASSWORD)

def fill_signup_form(driver):
    locators = SignUp_Form_Locators()
    
    get_element_when_visible(driver, By.XPATH , locators.username)
    
    setup_logging("Filling signup form.")
    
    driver.find_element(By.XPATH , locators.username).send_keys(USERNAME)
    driver.find_element(By.XPATH , locators.full_name).send_keys(FULLNAME)
    driver.find_element(By.XPATH , locators.email).send_keys(EMAIL)
    driver.find_element(By.XPATH , locators.dob).send_keys(DATEOFBIRTH)
    driver.find_element(By.XPATH , locators.phone_number).send_keys(PHONENUMBER)
    
    upload_id_element = driver.find_element(By.XPATH , locators.upload_id)
    upload_id_element.send_keys(UPLOADIDPATH)
    
    driver.find_element(By.XPATH , locators.password).send_keys(PASSWORD)
    driver.find_element(By.XPATH , locators.confirm_password).send_keys(PASSWORD)
    
    driver.find_element(By.XPATH , locators.tnc).click()
    
    driver.find_element(By.XPATH , locators.create_account).click()
    
    setup_logging("Signup form submitted.")