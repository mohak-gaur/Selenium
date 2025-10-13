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
import random
import string

# ---------- CONFIG ----------
EXCEL_FILE = r'Cosmic Miner/users.xlsx'
EXCEL_SHEET = 'users'
START_REFERRAL_CODE = 'QM1JEHOY'
CHILDREN_PER_PARENT = 3
MAX_LEVELS = 5
DEFAULT_PIN = "0000"
SITE_HOME_URL = "https://www.cosmiminer.in/"
REGISTER_URL = "https://www.cosmiminer.in/register.html"

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "123456"
ADMIN_URL = "https://cosmicminer.in/admin/login.php"

# ---------- HELPERS ----------
def init_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
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
    driver.get(REGISTER_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your Name']"))).send_keys(user["Name"])
    driver.find_element(By.ID, "email").send_keys(user["Email"])
    driver.find_element(By.XPATH, "//input[@placeholder='Enter your UserName']").send_keys(user["Name"])
    driver.find_element(By.ID, "password").send_keys(user["Password"])
    driver.find_element(By.ID, "confirm_password").send_keys(user["ConfirmPassword"])
    driver.find_element(By.ID, "referral_id").send_keys(referral_code)
    driver.find_element(By.ID, "remember").click()
    driver.find_element(By.ID, "Register").click()

def handle_pin_setup(driver, wait):
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
    try:
        checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#dontShowAgain")))
        checkbox.click()
    except Exception:
        pass
    try:
        popup_close = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "closePopup")))
        popup_close.click()
    except Exception:
        pass
    try:
        start_mining = wait.until(EC.element_to_be_clickable((By.ID, "startMiningBtn")))
        driver.execute_script("arguments[0].scrollIntoView(true);", start_mining)
        start_mining.click()
        time.sleep(3)
    except Exception:
        pass

def extract_referral_link(driver, wait):
    try:
        referral_nav = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='referrals.php']")))
        referral_nav.click()
        referral_url = wait.until(EC.presence_of_element_located((By.ID, "referralLink"))).get_attribute("value")
        parsed = urlparse(referral_url)
        referral_code = parse_qs(parsed.query).get('ref', [None])[0]
        print(f"Referral URL: {referral_url}")
        print(f"Extracted Referral Code: {referral_code}")
        return referral_code
    except Exception as e:
        logging.error(f"Failed to extract referral: {e}")
        return None

# ----------- NEW FUNCTIONALITIES ------------- #
def random_letters(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

# ---------- Modified portions: improved logging + admin-in-new-tab flow ----------

def perform_plan_upgrade(driver, wait):
    """
    Perform plan upgrade on the logged-in user dashboard.
    Returns True if upgrade flow completed (modal submitted), False otherwise.
    """
    try:
        logging.info("Navigating to Dashboard -> Upgrade page")
        # Go to dashboard and click upgrade nav
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='dashboard.php']"))).click()
        upgrade_nav = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='upgrade_gpc.php']")))
        upgrade_nav.click()

        # choose a random plan id between 1 and 4
        random_id = random.randint(1, 4)
        logging.info(f"Selecting random pack with plan_id={random_id}")
        random_package_locator = f"//button[contains(@onclick , 'plan_id={random_id}')]"
        upgrade_button = wait.until(EC.element_to_be_clickable((By.XPATH, random_package_locator)))
        upgrade_button.click()

        time.sleep(1)  # allow modal/plan details to appear
        # read plan amount text
        plan_range = driver.find_element(By.XPATH, "//div[@class='plan-range']").text
        logging.info(f"Selected plan range text: {plan_range}")

        amount_lookup = {
            '30.000 USDT': 80,
            '101.000 USDT': 200,
            '251.000 USDT': 800,
            '1001.000 USDT': 4500
        }
        set_amount = ''
        for key, val in amount_lookup.items():
            if key in plan_range:
                set_amount = val
                break

        if set_amount != '':
            try:
                logging.info(f"Setting amount to {set_amount}")
                amt_input = wait.until(EC.presence_of_element_located((By.ID, "amount")))
                amt_input.clear()
                amt_input.send_keys(str(set_amount))
            except Exception as e:
                logging.warning(f"Couldn't set the amount input: {e}")

        # Click pay now
        wait.until(EC.element_to_be_clickable((By.ID, "pay-now-btn"))).click()
        time.sleep(1)

        # generate random txn hash and submit
        txn_hash = random_letters(8)
        logging.info(f"Submitting fake transaction hash: {txn_hash}")
        wait.until(EC.presence_of_element_located((By.ID, "modal-txn-hash"))).send_keys(txn_hash)
        wait.until(EC.element_to_be_clickable((By.ID, "modal-submit"))).click()

        # wait a little for modal to close / success message
        time.sleep(2)
        logging.info("Plan upgrade flow completed (client-side) — awaiting admin confirmation.")
        return True
    except Exception as e:
        logging.error(f"Error during perform_plan_upgrade: {e}", exc_info=True)
        return False


def admin_confirm_order_in_new_tab(driver):
    """
    Opens admin URL in a new tab, logs in and marks the latest pending plan purchase as completed.
    Closes admin tab and switches back to original window.
    Returns True on success, False otherwise.
    """
    original_handle = driver.current_window_handle
    try:
        logging.info("Opening admin panel in a new tab for order confirmation.")
        # Open new tab and navigate to ADMIN_URL
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(0.5)
        handles = driver.window_handles
        admin_handle = handles[-1]
        driver.switch_to.window(admin_handle)
        driver.get(ADMIN_URL)

        wait_admin = WebDriverWait(driver, 20)
        logging.info("Attempting admin login.")
        # login to admin
        wait_admin.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(ADMIN_USERNAME)
        driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
        # click login button (selector from your old code)
        wait_admin.until(EC.element_to_be_clickable((By.XPATH, "//button[@class = 'btn btn-login']"))).click()
        logging.info("Admin login submitted; waiting for dashboard/plan user link.")

        # navigate to planwiseuser page
        plan_user = wait_admin.until(EC.element_to_be_clickable((By.XPATH, "//a[@href = 'planwiseuser.php']")))
        plan_user.click()
        time.sleep(1)

        # Click edit on the first pending order (you had this selector earlier)
        logging.info("Opening first order to edit status.")
        wait_admin.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='action-btn btn-edit'])[1]"))).click()
        time.sleep(1)

        # change status to completed
        # clicking status dropdown & choosing 'completed'
        driver.find_element(By.NAME, "status").click()
        driver.find_element(By.XPATH, "//option[@value='completed']").click()
        driver.find_element(By.NAME, "update_status").click()
        logging.info("Order status updated to 'completed' in admin.")
        time.sleep(2)

        # optionally verify a success message (if available)
        # e.g. wait_admin.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success")))
        return True
    except Exception as e:
        logging.error(f"Admin confirmation failed: {e}", exc_info=True)
        return False
    finally:
        # close admin tab and switch back to original
        try:
            driver.close()
            logging.info("Closed admin tab.")
        except Exception:
            logging.debug("Admin tab close failed or already closed.")
        # switch back to original if available
        try:
            driver.switch_to.window(original_handle)
            logging.info("Switched back to user tab.")
        except Exception:
            logging.warning("Could not switch back to original window (it might be closed).")


def register_user_and_get_referral(user, referral_code):
    """
    Register a single user, extract their referral, perform upgrade, open admin tab and confirm the order.
    Returns the new referral code (or None on failure).
    """
    driver = init_driver()
    wait = WebDriverWait(driver, 20)
    try:
        logging.info(f"Starting registration for {user['Email']} with parent referral {referral_code}")
        driver.get(REGISTER_URL)
        fill_registration_form(driver, wait, user, referral_code)

        # handle pin setup and onboarding popups
        handle_pin_setup(driver, wait)

        # 1) Extract referral for the newly created user (as requested)
        new_referral = extract_referral_link(driver, wait)
        logging.info(f"New referral extracted: {new_referral}")

        # 2) Back to dashboard and perform upgrade
        upgrade_ok = perform_plan_upgrade(driver, wait)
        if not upgrade_ok:
            logging.error("Upgrade failed for user: %s", user["Email"])
            return new_referral  # return extracted referral even if upgrade failed

        # 3) After upgrade, open admin in new tab and confirm the order
        admin_ok = admin_confirm_order_in_new_tab(driver)
        if admin_ok:
            logging.info("Admin confirmed order for user %s", user["Email"])
        else:
            logging.error("Admin confirmation failed for user %s", user["Email"])

        logging.info(f"✅ Registered {user['Email']} | Referral: {new_referral} | Upgrade: {upgrade_ok} | AdminConfirm: {admin_ok}")
        return new_referral
    except Exception as e:
        logging.error(f"Registration flow error for {user['Email']}: {e}", exc_info=True)
        return None
    finally:
        try:
            driver.quit()
            logging.info("Closed browser for this user.")
        except Exception:
            pass

def build_referral_hierarchy(users, start_referral, children_per_parent=3, max_levels=3):
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
            } for (u, parent, new_ref, lvl) in results
        ])
        df_out.to_excel("referral_results.xlsx", index=False)
        logging.info("✅ Saved results to referral_results.xlsx")