import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

path = r'C:\Programs\chromedriver.exe'
url = 'https://opensource-demo.orangehrmlive.com/web/index.php/auth/login'

@pytest.fixture
def driver():
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver, username, password):
    driver.get(url)
    wait = WebDriverWait(driver,10)
    try:
        wait.until(EC.presence_of_element_located((By.NAME , 'username'))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.NAME , 'password'))).send_keys(password)
    except TimeoutException:
        pytest.fail('No Elements Found!')

def click_login(driver):
    wait = WebDriverWait(driver,10)
    try:
        login_button  = wait.until(EC.presence_of_element_located((By.XPATH , "//button[@type='submit']")))
        login_button.click()
    except TimeoutException:
        pytest.fail("Login Button not present!")
        
def test_login_success(driver):
    login(driver, "Admin", "admin123")
    click_login(driver)
    assert "dashboard" in driver.current_url.lower()
    # assert driver.find_element(By.CSS_SELECTOR, ".oxd-userdropdown-name").is_displayed()

def test_login_fail(driver):
    login(driver, "Mohak", "mohak123")
    click_login(driver)
    assert "auth/login" in driver.current_url.lower()
    # error_msg = driver.find_element(By.CSS_SELECTOR, ".oxd-alert-content-text").text
    # assert "invalid" in error_msg.lower()


