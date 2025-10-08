from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


def init_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.set_page_load_timeout(60)
    driver.maximize_window()
    # yield driver
    # driver.quit()
    return driver

def cosmic_register():
    tester_name  = "cosmic_miner_tester9"
    tester_email = f"{tester_name}@yopmail.com"
    # tester_email = "cosmic_miner_tester1@yopmail.com"
    driver = init_driver()
    wait = WebDriverWait(driver,20)
    driver.get("https://www.cosmiminer.in/ravi/")
    start_mining = wait.until(EC.element_to_be_clickable((By.XPATH , "(//a[@class='btn'])[1]")))
    start_mining.click()
    driver.find_element(By.XPATH , "//a[@href='register.html']").click()
    time.sleep(2)

#input Name
    input_name = wait.until(EC.presence_of_element_located((By.XPATH , "//input[@placeholder = 'Enter your Name']")))
    input_name.send_keys(tester_name)
#input Email
    driver.find_element(By.ID , "email").send_keys(tester_email)
#input UserName
    driver.find_element(By.XPATH , "//input[@placeholder = 'Enter your UserName']").send_keys(tester_name)
#input Password
    driver.find_element(By.ID , "password").send_keys("Admin123!")
#input Confirm Password
    driver.find_element(By.ID , "confirm_password").send_keys("Admin123!")
#input referral code
    driver.find_element(By.ID , "referral_id").send_keys("ZJO9U2CY")
#click checkbox
    driver.find_element(By.ID , "remember").click()
#click Register button
    driver.find_element(By.ID , "Register").click()
    time.sleep(2)

#Create Pin

    wait.until(EC.presence_of_element_located((By.XPATH , "//input[@oninput = 'moveToNext(this, 1)']")))
    # create_pin.send_keys("0")
    for i in range(1,5):
        driver.find_element(By.XPATH , f"//input[@oninput = 'moveToNext(this, {i})']").send_keys("0")
    driver.find_element(By.ID , "nextBtn").click()

#Confirm Pin

    wait.until(EC.presence_of_element_located((By.XPATH , "//input[@oninput='moveToNextConfirm(this, 1)']")))
    for i in range (1,5):
        driver.find_element(By.XPATH , f"//input[@oninput='moveToNextConfirm(this, {i})']").send_keys("0")
    driver.find_element(By.ID , "setPinBtn").click()

    # time.sleep(60)

#Close PopUp

    wait.until(EC.element_to_be_clickable((By.ID , "closePopup"))).click()

    time.sleep(5)



#Find Referral Button

    referral_nav = wait.until(EC.element_to_be_clickable((By.XPATH , "//a[@href='referrals.php']")))
    referral_nav.click()

#Find Referral URL

    referral_url = wait.until(EC.presence_of_element_located ((By.ID , "referralLink")))
    print(referral_url.get_attribute("value"))
    

    time.sleep(3)

cosmic_register()
    