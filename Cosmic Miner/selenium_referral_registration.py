from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from collections import deque
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------- CONFIG ----------
EXCEL_FILE = r'Cosmic Miner/users.xlsx'        # Excel file path
EXCEL_SHEET = 'users'           # sheet name
START_REFERRAL_CODE = 'ZJO9U2CY'  # Level 1 referral code you will give (can be a full referral URL)
children_per_parent = 3         # how many users to create under each parent
max_levels = 5                  # safety cap on levels (optional)
SITE_REGISTER_URL = 'https://cosmiminer.in/ravi/register.html'  # registration page
HEADLESS = False                # set True for headless mode
PAGE_LOAD_WAIT = 2              # seconds to wait after navigation / submission (adjust as needed)
DEFAULT_PIN = '0000'            # 4-digit PIN to set when redirected to pin.php

# Selectors - best effort defaults (update if site differs)
selectors = {
    'name': '//input[@placeholder="Enter your Name"]',
    'email': 'input[name="email"]',
    'user_name': '//input[@placeholder="Enter your UserName"]',   # or the exact locator
    'password': 'input[name="password"]',
    'confirm_password': 'input[name="confirm_password"]',
    'referral_code': 'input[name="refer_code"]',
    'terms_checkbox': 'input[type="checkbox"]',  # ya uska exact CSS selector
    'submit': 'button[type="submit"]',
    # PIN page selectors (common pattern: two inputs and a submit)
    # 'pin_input': 'input[name="pin"]',
    # 'pin_next': '//button[@id=nextBtn"]',
    # 'pin_confirm_input': 'input[name="pin_confirm"]',
    # 'pin_submit': '//button[@id="setPinBtn"]'
}

# ---------- HELPERS ----------

def create_webdriver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)
    driver.maximize_window()
    return driver


def read_users_from_excel(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet, engine='openpyxl')
    expected_cols = ['Name', 'Email', 'Password', 'ConfirmPassword']
    for c in expected_cols:
        if c not in df.columns:
            raise ValueError(f"Excel missing required column: {c}")
    df = df.dropna(subset=['Name', 'Email', 'Password'])
    return df.to_dict(orient='records')


def safe_find(driver, by, selector, timeout=2):
    """Try to find element, return None if not present."""
    try:
        return driver.find_element(by, selector)
    except Exception:
        return None


def fill_and_submit_registration(driver, user, referral_code):
    """Fill registration form and submit. After submission, handle PIN page if shown.
    Returns True if submission attempted.
    """
    driver.get(SITE_REGISTER_URL)
    time.sleep(PAGE_LOAD_WAIT)

    # Fill fields
    el = safe_find(driver, By.XPATH, selectors['name'])
    el.clear(); el.send_keys(user['Name'])
    # else:
    #     logging.warning('Name input not found with default selector')

    #UserName
    if elem := safe_find(driver, By.XPATH, selectors.get('user_name', '')):
        elem.clear()
        elem.send_keys(user['Name'])


    el = safe_find(driver, By.CSS_SELECTOR, selectors['email'])
    if el:
        el.clear(); el.send_keys(user['Email'])

    el = safe_find(driver, By.CSS_SELECTOR, selectors['password'])
    if el:
        el.clear(); el.send_keys(user['Password'])

    el = safe_find(driver, By.CSS_SELECTOR, selectors['confirm_password'])
    if el:
        el.clear(); el.send_keys(user['ConfirmPassword'])

    # Referral code (could be a full referral URL or short code)
    if referral_code:
        # Some sites require clicking an "I have a referral" checkbox or putting code in a field; try the field first
        el = safe_find(driver, By.CSS_SELECTOR, selectors['referral_code'])
        if el:
            el.clear(); el.send_keys(referral_code)
        else:
            logging.info('Referral input not found; will try visiting referral URL directly if provided')

    #checkbox

    # Tick the Terms & Conditions checkbox if present
    if elem := safe_find(driver, By.CSS_SELECTOR, selectors.get('terms_checkbox', '')):
        try:
            if not elem.is_selected():
                driver.execute_script("arguments[0].click();", elem)
            print("✅ Terms checkbox ticked successfully.")
        except Exception as e:
            print(f"⚠️ Unable to tick checkbox: {e}")


    # Submit
    el = safe_find(driver, By.CSS_SELECTOR, selectors['submit'])
    if el:
        el.click()
    else:
        logging.error('Submit button not found; cannot submit registration')
        return False

    time.sleep(PAGE_LOAD_WAIT + 1)

    # If redirected to PIN set page, handle it
    try:
        current = driver.current_url
        if 'pin.php' in current or 'pin' in current.lower():
            logging.info('Detected PIN page. Setting PIN...')
            handle_pin_page(driver, DEFAULT_PIN)
            time.sleep(1)
    except Exception as e:
        logging.warning(f'Error while checking/handling PIN page: {e}')

    return True


def handle_pin_page(driver, pin_value="0000"):
    """Handles PIN entry (0000) and confirm PIN flow on pin.php page."""
    try:
        def fill_pin_boxes(selector, description):
            """Inner helper to safely fill 4 PIN boxes."""
            boxes = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(boxes) < 4:
                print(f"⚠️ {description}: Expected 4 boxes, found {len(boxes)}")
                return False

            print(f"Entering {description}...")
            for i, (box, digit) in enumerate(zip(boxes, pin_value)):
                # Make sure box is visible and editable
                driver.execute_script("arguments[0].scrollIntoView(true);", box)
                driver.execute_script("arguments[0].removeAttribute('readonly');", box)
                driver.execute_script("arguments[0].focus();", box)
                time.sleep(0.2)
                try:
                    box.clear()
                except Exception:
                    pass
                box.send_keys(digit)
                time.sleep(0.3)
            print(f"✅ {description} entered successfully.")
            return True

        time.sleep(2)
        print("🔢 Starting PIN setup...")

        # --- STEP 1: Set PIN ---
        if fill_pin_boxes("input.pin-digit", "PIN (Step 1)"):
            next_btn = safe_find(driver, By.XPATH, "//button[@id='nextBtn']")
            if next_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                driver.execute_script("arguments[0].click();", next_btn)
                print("➡️ Clicked 'Next' after entering PIN.")
            else:
                print("⚠️ 'Next' button not found.")
        else:
            print("❌ PIN input fields not found for Step 1.")
        time.sleep(3)

        # --- STEP 2: Confirm PIN ---
        if fill_pin_boxes("input.pin-digit", "Confirm PIN (Step 2)"):
            setpin_btn = safe_find(driver, By.XPATH, "//button[@id='setPinBtn']")
            if setpin_btn:
                driver.execute_script("arguments[0].scrollIntoView(true);", setpin_btn)
                driver.execute_script("arguments[0].click();", setpin_btn)
                print("🔒 Clicked 'Set PIN' successfully.")
            else:
                print("⚠️ 'Set PIN' button not found.")
        else:
            print("⚠️ Confirm PIN inputs not found.")

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error while handling PIN page: {e}")




def extract_referral_code(driver):
    """Extract referral URL/code from dashboard (bottom-right referrals section).
    Uses several fallback strategies and returns a string (could be full URL or code) or None.
    """
    time.sleep(1)
    # Strategy 1: find anchor links that contain 'ref' or 'referral' in href
    try:
        anchors = driver.find_elements(By.TAG_NAME, 'a')
        for a in anchors:
            href = a.get_attribute('href') or ''
            if href and ('ref' in href.lower() or 'referral' in href.lower()):
                logging.info(f'Found referral link in anchor: {href}')
                return href.strip()
    except Exception:
        pass

    # Strategy 2: find any input field (or textarea) that contains the referral URL (value attribute)
    try:
        inputs = driver.find_elements(By.TAG_NAME, 'input') + driver.find_elements(By.TAG_NAME, 'textarea')
        for inp in inputs:
            val = (inp.get_attribute('value') or '').strip()
            if val and ('cosmiminer' in val.lower() or 'ref' in val.lower()):
                logging.info(f'Found referral in input value: {val}')
                return val
    except Exception:
        pass

    # Strategy 3: search for text nodes that include 'referral' or 'Refer' and extract nearby URL
    try:
        elems = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'referral')]")
        for e in elems:
            txt = e.text or ''
            # try to find http substring
            if 'http' in txt:
                start = txt.find('http')
                possible = txt[start:].split()[0]
                logging.info(f'Found referral in text node: {possible}')
                return possible
    except Exception:
        pass

    # Strategy 4: try to open a 'Referrals' widget by clicking bottom-right elements (common patterns)
    try:
        # common selectors for bottom-right widget buttons
        candidates = [
            "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'referral')]",
            "//div[contains(@class,'referral') or contains(@id,'referral')]",
            "//a[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'referral')]",
            "//button[contains(@class,'referral')]",
        ]
        for xp in candidates:
            els = driver.find_elements(By.XPATH, xp)
            if els:
                els[0].click()
                time.sleep(1)
                # after clicking, retry strategies 1 and 2
                # anchor retry
                anchors = driver.find_elements(By.TAG_NAME, 'a')
                for a in anchors:
                    href = a.get_attribute('href') or ''
                    if href and ('ref' in href.lower() or 'referral' in href.lower()):
                        logging.info(f'Found referral link after clicking widget: {href}')
                        return href.strip()
                inputs = driver.find_elements(By.TAG_NAME, 'input')
                for inp in inputs:
                    val = (inp.get_attribute('value') or '').strip()
                    if val and ('cosmiminer' in val.lower() or 'ref' in val.lower()):
                        logging.info(f'Found referral after clicking widget in input: {val}')
                        return val
    except Exception:
        pass

    logging.warning('Could not extract referral code/url using available strategies')
    return None

# ---------- CORE FLOW ----------

def build_referral_hierarchy(users, start_referral, children_per_parent=3, max_levels=5):
    driver = create_webdriver(headless=HEADLESS)
    user_idx = 0
    registered = []  # list of tuples (user_dict, referral_url_or_code, parent_referral, level)

    q = deque()
    q.append((start_referral, 1))

    while q and user_idx < len(users):
        parent_referral, level = q.popleft()
        logging.info(f"Processing parent referral '{parent_referral}' at level {level}")
        if level > max_levels:
            logging.info(f"Reached max_levels ({max_levels}). Stopping further expansion.")
            break

        for c in range(children_per_parent):
            if user_idx >= len(users):
                logging.info('No more users in Excel to register.')
                break
            user = users[user_idx]
            logging.info(f"Registering user {user['Email']} under parent {parent_referral}")
            try:
                # If parent_referral looks like a full URL (contains http), open it first
                if isinstance(parent_referral, str) and parent_referral.startswith('http'):
                    try:
                        driver.get(parent_referral)
                        time.sleep(PAGE_LOAD_WAIT)
                    except Exception as e:
                        logging.warning(f'Could not open parent referral URL: {e}')

                # Fill the registration form and submit
                fill_and_submit_registration(driver, user, parent_referral)

                # After registration flow (and possibly PIN setup), try to navigate to dashboard or extract referral
                new_code = extract_referral_code(driver)
                registered.append((user, new_code, parent_referral, level))
                if new_code:
                    q.append((new_code, level + 1))
            except Exception as e:
                logging.error(f"Error registering user {user['Email']}: {e}")
            user_idx += 1

    driver.quit()
    return registered


if __name__ == '__main__':
    users = read_users_from_excel(EXCEL_FILE, EXCEL_SHEET)
    logging.info(f"Loaded {len(users)} users from Excel")
    registered = build_referral_hierarchy(users, START_REFERRAL_CODE, children_per_parent, max_levels)
    logging.info('Registration run finished. Summary:')
    for u, code, parent, lvl in registered:
        logging.info(f"User: {u['Email']}, parent_referral: {parent}, new_referral: {code}, level: {lvl}")

    if registered:
        rows = []
        for u, code, parent, lvl in registered:
            rows.append({
                'Name': u['Name'],
                'Email': u['Email'],
                'ParentReferral': parent,
                'MyReferralCode': code,
                'Level': lvl
            })
        pd.DataFrame(rows).to_excel('registration_results.xlsx', index=False)
        logging.info('Saved registration_results.xlsx')
