from Utils.utils import create_driver
from Pages.age_conf import handle_age_confirmation
from Pages.selectAdvOrCon import navigate_to_signup
from Pages.fill_signup import fill_signup_form
import time



def main():
    driver = create_driver()
    driver.maximize_window()
    driver.get("https://wwrestlers.stage04.obdemo.com/")
    handle_age_confirmation(driver)
    navigate_to_signup(driver)
    fill_signup_form(driver)
    time.sleep(2)
    driver.quit()
    
    
if __name__ == "__main__":
    main()