from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging

USERNAME = "testing_advertiser_2"
FULLNAME = "Testing Advertiser"
EMAIL = f"{USERNAME}@yopmail.com"
DATEOFBIRTH = "01/01/1990"
PHONENUMBER = "1234567890"
UPLOADIDPATH = r"C:\Users\Samsung\OneDrive\Pictures\Wonder Wrestlers\ForgotPass.png"
PASSWORD = "Admin123!"
# CONFIRMPASSWORD = "Admin123!"


def create_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')