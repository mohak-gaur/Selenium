from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

path = r'C:\Tools\chromedriver.exe'
url = 'https://demo.nopcommerce.com'

service=Service(executable_path=path)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver,20)

driver.maximize_window()
driver.get(url)

login = wait.until(EC.presence_of_element_located((By.XPATH , "//*[@class='ico-login']")))
login.click()

time.sleep(5)

driver.quit()
driver.close()