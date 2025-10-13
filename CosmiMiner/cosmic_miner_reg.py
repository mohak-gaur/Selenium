from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import random
import string


id = 37
# plan_id = random.randint(1,4)
random_package_locator = f"//button[contains(@onclick , 'plan_id={random.randint(1,4)}')]" #chooses a random package (1 - Basic , 2 - Pro , 3 - Elite , 4 - Quantum)

#generate random hash
def random_letters(length = 8):
    return ''.join(random.choices(string.ascii_letters , k=length))


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,  # disable all browser notifications
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.set_page_load_timeout(60)
    driver.maximize_window()
    # yield driver
    # driver.quit()
    return driver

def cosmic_register():
    tester_name  = f"cosmic_miner_tester{id}"
    tester_email = f"{tester_name}@yopmail.com"
    # tester_email = "cosmic_miner_tester1@yopmail.com"
    driver = init_driver()
    wait = WebDriverWait(driver,20)
    driver.get("https://www.cosmiminer.in/")
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


    got_it = wait.until(EC.element_to_be_clickable((By.ID , "closePopup")))
    driver.find_element(By.ID , "dontShowAgain").click()
    got_it.click()

    time.sleep(2)



#Find Referral Button

    referral_nav = wait.until(EC.element_to_be_clickable((By.XPATH , "//a[@href='referrals.php']")))
    referral_nav.click()

#Find Referral URL

    referral_url = wait.until(EC.presence_of_element_located ((By.ID , "referralLink")))
    print(referral_url.get_attribute("value"))
    time.sleep(1)

#Going to Dashboard and purchase

    driver.find_element(By.XPATH , "//a[@href='dashboard.php']").click()

#find Upgrade button

    upgrade = wait.until(EC.element_to_be_clickable((By.XPATH , "//a[@href='upgrade_gpc.php']")))
    upgrade.click()

    upgrade_button = wait.until(EC.element_to_be_clickable((By.XPATH , random_package_locator)))
    upgrade_button.click()

    plan_range = driver.find_element(By.XPATH , "//div[@class='plan-range']").text
    # print(plan_range)
    try:
        if plan_range == '30.000 USDT':
            set_amount = int(80)

        if plan_range == '101.000 USDT':
            set_amount = int(200)
    
        if plan_range == '251.000 USDT':
            set_amount = int(800)
    
        if plan_range == '1001.000 USDT':
            set_amount = int(4500)

        print(f"Amount is {set_amount}")

    except Exception:
        print("Cant set the amount")

    try:
        driver.find_element(By.ID , "amount").send_keys(set_amount)
    except Exception:
        print("cant set the amount")
    driver.find_element(By.ID , "pay-now-btn").click()
    time.sleep(1)

    hash = random_letters(8)
    driver.find_element(By.ID , "modal-txn-hash").send_keys(hash)
    wait.until(EC.element_to_be_clickable((By.ID , "modal-submit"))).click()
    time.sleep(2)
    driver.quit()

#Opening Admin Panel and confirming Upgrade Purchase
def order_confirm():
    driver = init_driver()
    driver.get("https://cosmicminer.in/admin/login.php")
    login_dashboard = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable((By.XPATH , "//button[@class = 'btn btn-login']"))
    )
    driver.find_element(By.ID, "username").send_keys("Admin")
    driver.find_element(By.ID , "password").send_keys("123456")
    login_dashboard.click()
    
    plan_user = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable((By.XPATH , "//a[@href = 'planwiseuser.php']"))
    )
    plan_user.click()

    time.sleep(1)

    driver.find_element(By.XPATH , "(//button[@class='action-btn btn-edit'])[1]").click()
    time.sleep(1)
    driver.find_element(By.NAME , "status").click()
    driver.find_element(By.XPATH , "//option[@value='completed']").click()
    driver.find_element(By.NAME , "update_status").click()
    print("Status Updated")


    time.sleep(3)

cosmic_register()
order_confirm()
    