from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.utils import setup_logging

def get_element_when_visible(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.visibility_of_element_located((by, value)))
    return element

setup_logging("Waiting utility initialized.")

