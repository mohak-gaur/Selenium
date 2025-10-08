from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pytest

@pytest.mark.wedding
def test_wedding_couple_signup(driver):
    driver.get("https://www.spurexperiences.com/login")
    wait = WebDriverWait(driver,20)
    wedding_couple = wait.until(EC.presence_of_element_located((By.XPATH , "(//a[@href='/registration/wedding-couple'])[3]")))
    driver.execute_script("arguments[0].scrollIntoView(true);" , wedding_couple)
    wedding_couple.click()

    wait.until(EC.presence_of_element_located((By.ID , "email"))).send_keys("weddingcouple@yopmail.com")
    driver.find_element(By.ID , "passwrd").send_keys("Admin@12345")
    driver.find_element(By.XPATH , "//button[@class='form-control submit-button']").click()
    

    time.sleep(5)

    # assert "step-2" in driver.current_url.lower() , \
    # "Error in Wedding Couple Signup"


    driver.find_element(By.ID , "first_name").send_keys("CoM")
    driver.find_element(By.ID , "last_name").send_keys("MoN")
    driver.find_element(By.ID , "partner_first_name").send_keys("BoT")
    driver.find_element(By.ID , "partner_last_name").send_keys("MoN")
    time.sleep(3)
    driver.find_element(By.ID, "wedding_date").click()

    calender = wait.until(EC.presence_of_element_located((By.XPATH , "//div[@class='bs-datepicker-container ng-tns-c2433879322-19 ng-trigger ng-trigger-datepickerAnimation']")))
    # driver.execute_script("arguments[0].scrollIntoView(true);" , calender)
    time.sleep(5)

    date = driver.find_element(By.XPATH, "(//span[@class='ng-star-inserted'])[25]")
    date.click()


    driver.find_element(By.XPATH , '//input[@placeholder = "Search For Location"]').send_keys("Paris, France")
    driver.find_element(By.XPATH , "//button[@type='submit'][@class = 'form-control submit-button']").click()    
    time.sleep(5)


    driver.find_element(By.ID , "address").send_keys("D41")
    driver.find_element(By.ID , "city").send_keys("Jaipur")
    driver.find_element(By.ID , "state").send_keys("Rajasthan")
    driver.find_element(By.ID , "id").send_keys("302004")
    driver.find_element(By.XPATH, "//div[@aria-label='dropdown trigger']").click()

    time.sleep(1)

    driver.find_element(By.XPATH , "//input[@role='searchbox']").send_keys("Ind")
    wait.until(EC.element_located_to_be_selected((By.XPATH, '//div[@class="p-dropdown-items-wrapper"]')))
    driver.find_element(By.ID , "pn_id_9_0").click()
    driver.find_element(By.XPATH , "//button[@type='submit'][@class='form-control submit-button']").click()

    time.sleep(5)


    # Upload Image

    upload = wait.until(EC.presence_of_element_located((By.XPATH , "//div[@class='upload-round-input']")))
    upload.send_keys(r"C:\Users\Samsung\OneDrive\Pictures\Screenshots\1.png")

    save_but = wait.until(EC.element_to_be_clickable((By.XPATH , '(//button[@type="submit"][@class="btnSubmitCropy"])[4]')))
    save_but.click()
    time.sleep(5)
    assert "step-5" in driver.current_url.lower(), \
    "Signup failed"