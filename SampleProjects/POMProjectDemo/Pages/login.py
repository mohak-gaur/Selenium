from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from homePage import HomePage
from loginPage import LoginPage
import unittest
import time
import HtmlTestRunner


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
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=r'C:\Selenium\SampleProjects\POMProjectDemo\Reports'))