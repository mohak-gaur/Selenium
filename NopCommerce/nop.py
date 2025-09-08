from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Pages.Home_Page import HomePage
from Pages.Login_Page import LoginPage
from Pages.Register_Page import RegisterPage
import time

def create_driver():
    service = Service(executable_path=r'C:\Programs\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

def test_home_page():
    driver = create_driver()
    driver.get('https://demo.nopcommerce.com')

    home_page = HomePage(driver)
    home_page.Register()
    time.sleep(5)
    driver.quit()

def test_register_page():
    driver = create_driver()
    driver.get('https://demo.nopcommerce.com/register/')

    register_page = RegisterPage(driver)
    register_page.inputGender()
    register_page.inputFirstName('Mohak')
    register_page.inputLastName('Gaur')
    register_page.inputEmail('common30@tafmail.com')
    register_page.inputPassword('abcd123')
    register_page.confirmPassword('abcd123')
    time.sleep(3)
    register_page.click_register()

    time.sleep(5)
    driver.quit()

def test_login_page():
    driver = create_driver()
    driver.get('https://demo.nopcommerce.com/login')

    login_page = LoginPage(driver)
    login_page.inputEmail('common30@tafmail.com')
    login_page.inputPassword('abcd123')
    login_page.click_login()

    time.sleep(5)

    driver.quit()

if __name__ == "__main__":
    test_home_page()
    test_register_page()
    test_login_page()