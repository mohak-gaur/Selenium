from Utils.waiting import get_element_when_visible
from Locators.ageConfLoc import Age_Conf_Locators
from selenium.webdriver.common.by import By

def handle_age_confirmation(driver):
    locators = Age_Conf_Locators()    
    get_element_when_visible(driver, By.XPATH , locators.age_title)    
    yes_button = driver.find_element(By.XPATH , locators.yes_button)
    yes_button.click()