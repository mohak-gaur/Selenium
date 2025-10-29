from Utils.waiting import get_element_when_visible
from Utils.utils import setup_logging
from Locators.homePageLoc import Home_Page_Locators
from selenium.webdriver.common.by import By

def navigate_to_signup(driver):
    locators = Home_Page_Locators()
    
    setup_logging("Navigating to signup page.")
    
    get_element_when_visible(driver, By.XPATH , locators.cookie_close)    
    cookie_close_button = driver.find_element(By.XPATH , locators.cookie_close)
    cookie_close_button.click()    
    signup_link = driver.find_element(By.LINK_TEXT , locators.signup)
    signup_link.click()
    
    driver.find_element(By.XPATH , locators.advertiser).click()
    get_element_when_visible(driver, By.XPATH , locators.continue_as)
    driver.find_element(By.XPATH , locators.continue_as).click()