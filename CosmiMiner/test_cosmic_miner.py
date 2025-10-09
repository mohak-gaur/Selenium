from locators import Login_Page_Locators as LL
from locators import Close_PopUp
from locators import Start_Mining
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import allure
import time

USERNAME = "cosmic_test_108@yopmail.com"
PASSWORD = "Admin123!"

#WebDriverWait added and directly hit the url from this method
def init_url(driver):
    wait = WebDriverWait(driver,20)
    driver.get("https://cosmiminer.in/ravi/login.html")
    wait.until(EC.presence_of_element_located(LL.email))

def login(driver):
    init_url(driver)
    driver.find_element(*LL.email).send_keys(USERNAME)
    driver.find_element(*LL.password).send_keys(PASSWORD)
    driver.find_element(*LL.remember_me).click()
    driver.find_element(*LL.login).click()
    time.sleep(1)
    driver.find_element(*Close_PopUp.dont_show).click()
    driver.find_element(*Close_PopUp.close_popup).click()
    time.sleep(3)

#Valid Credentials Test
@pytest.mark.validLogin
def test_valid_login(driver):
    login(driver)
    # driver.get_screenshot_as_png()
    if "dashboard.php" in driver.current_url.lower():
        allure.attach(
            driver.get_screenshot_as_png(),
            name = "Login Success",
            attachment_type=allure.attachment_type.PNG
        )
    assert "dashboard.php" in driver.current_url.lower() , \
    "Not able to login"

#Invalid Credentails Test
@pytest.mark.invalidLogin
def test_invalid_login(driver):
    init_url(driver)
    driver.find_element(*LL.email).send_keys("admin@yopmail.com")
    driver.find_element(*LL.password).send_keys("admin123")
    driver.find_element(*LL.remember_me).click()
    driver.find_element(*LL.login).click()
    time.sleep(2)

    actual_text = driver.find_element(*LL.invalid_creds).text
    print(f"Text ye hai: {actual_text}")
    # driver.get_screenshot_as_png()
    if actual_text == "Error: Invalid User id and password":
        allure.attach(
            driver.get_screenshot_as_png(),
            name = "Invalid Login",
            attachment_type= allure.attachment_type.PNG
        )
    assert actual_text == "Error: Invalid User id and password", "Something occurred"

@pytest.mark.startMining
def test_start_mining(driver):
    login(driver)
    mining_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable(Start_Mining.start_button))
    driver.execute_script("arguments[0].scrollIntoView(true);" , mining_button)
    mining_button.click()
    time.sleep(3)

    
    time.sleep(3)

    # assert status_text == " MINING" , "Mining not started"
    time_remain = WebDriverWait(driver,20).until(EC.presence_of_element_located(Start_Mining.time_left))
    # driver.get_screenshot_as_png()
    if time_remain.is_displayed():
        allure.attach(
            driver.get_screenshot_as_png(),
            name = "Mining Started",
            attachment_type= allure.attachment_type.PNG
        )
    assert time_remain.is_displayed() , "Mining not started"