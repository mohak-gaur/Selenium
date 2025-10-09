from locators import Login_Page_Locators as LL
from locators import Close_PopUp
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import time

#WebDriverWait added and directly hit the url from this method
def init_url(driver):
    wait = WebDriverWait(driver,20)
    driver.get("https://cosmiminer.in/ravi/login.html")
    wait.until(EC.presence_of_element_located(LL.email))

#Valid Credentials Test
@pytest.mark.validLogin
def test_valid_login(driver):
    init_url(driver)
    driver.find_element(*LL.email).send_keys("cosmic_miner_main@yopmail.com")
    driver.find_element(*LL.password).send_keys("Admin123!")
    driver.find_element(*LL.remember_me).click()
    driver.find_element(*LL.login).click()
    time.sleep(1)
    driver.find_element(*Close_PopUp.dont_show).click()
    driver.find_element(*Close_PopUp.close_popup).click()
    time.sleep(3)
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
    assert actual_text == "Error: Invalid User id and password", "Something occurred"