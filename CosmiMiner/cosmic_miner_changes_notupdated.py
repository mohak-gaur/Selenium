from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.parse import urlparse, parse_qs
import pandas as pd
import time
import logging
from collections import deque


# ---------- CONFIG ----------
EXCEL_FILE = r'Cosmic Miner/users.xlsx'
EXCEL_SHEET = 'users'
START_REFERRAL_CODE = 'QM1JEHOY'  # Level 1 referral code
CHILDREN_PER_PARENT = 3
MAX_LEVELS = 3
DEFAULT_PIN = "0000"

SITE_HOME_URL = "https://www.cosmiminer.in/ravi/"
REGISTER_URL = "https://www.cosmiminer.in/ravi/register.html"


# ---------- HELPERS ----------

def init_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.set_page_load_timeout(60)
    driver.maximize_window()
    return driver


def read_users_from_excel(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet)
    required = ['Name', 'Email', 'Password', 'ConfirmPassword']
    for c in required:
        if c not in df.columns:
            raise ValueError(f"Missing column in Excel: {c}")
    return df.to_dict(orient='records')


def fill_registration_form(driver, wait, user, referral_code):
    """Fills and submits registration form for one user."""
    driver.get(REGISTER_URL)

    # Input Name
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your Name']"))).send_keys(user["Name"])
    # Email
    driver.find_element(By.ID, "email").send_keys(user["Email"])
    # UserName (same as Name)
    driver.find_element(By.XPATH, "//input[@placeholder='Enter your UserName']").send_keys(user["Name"])
    # Password + Confirm Password
    driver.find_element(By.ID, "password").send_keys(user["Password"])
    driver.find_element(By.ID, "confirm_password").send_keys(user["ConfirmPassword"])
    # Referral Code
    driver.find_element(By.ID, "referral_id").send_keys(referral_code)
    # time.sleep(5)
    # Tick checkbox
    driver.find_element(By.ID, "remember").click()
    # Click Register
    driver.find_element(By.ID, "Register").click()


def handle_pin_setup(driver, wait):
    """Handles both PIN creation and confirmation pages."""
    # Step 1: Create PIN
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@oninput='moveToNext(this, 1)']")))
    for i in range(1, 5):
        pin_box = driver.find_element(By.XPATH, f"//input[@oninput='moveToNext(this, {i})']")
        driver.execute_script("arguments[0].removeAttribute('readonly');", pin_box)
        driver.execute_script("arguments[0].focus();", pin_box)
        pin_box.send_keys("0")
        time.sleep(0.2)
    driver.find_element(By.ID, "nextBtn").click()

    # Step 2: Confirm PIN
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@oninput='moveToNextConfirm(this, 1)']")))
    for i in range(1, 5):
        pin_box = driver.find_element(By.XPATH, f"//input[@oninput='moveToNextConfirm(this, {i})']")
        driver.execute_script("arguments[0].removeAttribute('readonly');", pin_box)
        driver.execute_script("arguments[0].focus();", pin_box)
        pin_box.send_keys("0")
        time.sleep(0.2)
    driver.find_element(By.ID, "setPinBtn").click()

    # Close popup (if appears)
    try:
        popup_close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "closePopup")))
        popup_close.click()
    except Exception:
        pass


def extract_referral_link(driver, wait):
    """Navigates to referrals page and extracts only the referral code."""
    try:
        referral_nav = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='referrals.php']")))
        referral_nav.click()
        referral_url = wait.until(EC.presence_of_element_located((By.ID, "referralLink"))).get_attribute("value")

        # Extract referral code from ?ref=XYZ
        parsed = urlparse(referral_url)
        referral_code = parse_qs(parsed.query).get('ref', [None])[0]

        print(f"Referral URL: {referral_url}")
        print(f"Extracted Referral Code: {referral_code}")

        return referral_code
    except Exception as e:
        logging.error(f"Failed to extract referral: {e}")
        return None



def register_user_and_get_referral(user, referral_code):
    """Registers a single user and returns their referral link."""
    driver = init_driver()
    wait = WebDriverWait(driver, 20)

    try:
        # driver.get(SITE_HOME_URL)
        # start_mining = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='btn'])[1]")))
        # start_mining.click()
        # driver.find_element(By.XPATH, "//a[@href='register.html']").click()
        # time.sleep(2)

#Changed because I dont want an extra step of going to HomePage and then click on the register button
#Rather it will diretly open the Register Form Page
        driver.get(REGISTER_URL)
        fill_registration_form(driver, wait, user, referral_code)
        handle_pin_setup(driver, wait)
        new_referral = extract_referral_link(driver, wait)
        logging.info(f"✅ Registered {user['Email']} | Referral: {new_referral}")
        return new_referral
    except Exception as e:
        logging.error(f"❌ Registration failed for {user['Email']}: {e}")
        return None
    finally:
        driver.quit()


def build_referral_hierarchy(users, start_referral, children_per_parent=3, max_levels=3):
    """Creates referral hierarchy recursively using BFS."""
    registered = []
    queue = deque([(start_referral, 1)])
    user_idx = 0

    while queue and user_idx < len(users):
        parent_referral, level = queue.popleft()
        if level > max_levels:
            break

        for i in range(children_per_parent):
            if user_idx >= len(users):
                break
            user = users[user_idx]
            logging.info(f"🔹 Registering Level {level} User: {user['Email']} (Parent: {parent_referral})")

            new_referral = register_user_and_get_referral(user, parent_referral)
            registered.append((user, parent_referral, new_referral, level))

            if new_referral:
                queue.append((new_referral, level + 1))

            user_idx += 1

    return registered


# ---------- MAIN ----------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    users = read_users_from_excel(EXCEL_FILE, EXCEL_SHEET)
    logging.info(f"Loaded {len(users)} users from Excel")

    results = build_referral_hierarchy(users, START_REFERRAL_CODE, CHILDREN_PER_PARENT, MAX_LEVELS)

    if results:
        df_out = pd.DataFrame([
            {
                "Name": u["Name"],
                "Email": u["Email"],
                "ParentReferral": parent,
                "MyReferral": new_ref,
                "Level": lvl
            }
            for (u, parent, new_ref, lvl) in results
        ])
        df_out.to_excel("referral_results.xlsx", index=False)
        logging.info("✅ Saved results to referral_results.xlsx")
