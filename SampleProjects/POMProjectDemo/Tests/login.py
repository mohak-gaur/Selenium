from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from POMProjectDemo.Pages.homePage import HomePage
from POMProjectDemo.Pages.loginPage import LoginPage
from selenium.webdriver.common import a
import unittest
import time


class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = "C:/Programs/chromedriver.exe"
        cls.service = Service(executable_path=cls.path)
        cls.driver = webdriver.Chrome(service=cls.service)
        cls.driver.maximize_window()

    def test_login_valid(self):
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        login = LoginPage(driver)
      
        login.enter_username('Admin')
        login.enter_password('admin123')
        login.enter_login()

        homepage = HomePage(driver)
        homepage.click_dropdown()
        homepage.click_logout()

        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print('Test Completed')

if __name__ == '__main__':
    unittest.main()