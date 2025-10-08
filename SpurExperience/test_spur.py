import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.ui
def test_spur_experience(driver):
    driver.get("https://www.spurexperiences.com")
    wait = WebDriverWait(driver,20)
    accept_cookie = wait.until(EC.presence_of_element_located((By.XPATH , '//*[@class="accept_cookie"]')))
    accept_cookie.click()
    gift_idea = wait.until(EC.element_to_be_clickable((By.XPATH , "//a[@class='nav-link dropdown-toggle'][@href='/gift-ideas']")))
    gift_idea.click()
    time.sleep(3)
    culture_vul = wait.until(EC.element_to_be_clickable((By.XPATH, "(//figcaption[@class='giftCategoryName'])[2]")))
    # time.sleep(3)
    # wait.until(EC.presence_of_element_located(culture_vul))
    driver.execute_script("arguments[0].scrollIntoView(false);" , culture_vul)
    culture_vul.click()

    #intoCultureVulture

    vino_wine = wait.until(EC.element_to_be_clickable((By.XPATH , "(//a[@href='/experiences/vino-vino-little-italy-wine-stroll'])[2]")))
    driver.execute_script("arguments[0].scrollIntoView(true);" , vino_wine)
    vino_wine.click()

    people_count = wait.until(EC.element_to_be_clickable((By.XPATH , "//select[@id='select_people']")))
    driver.execute_script("arguments[0].scrollIntoView(false);" , people_count)
    people_count.click()
    time.sleep(3)

    driver.find_element(By.XPATH , "(//option[@class='ng-star-inserted'])[11]").click()
    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.XPATH , "//div[@class='ngb-dp-content ngb-dp-months']")))
    # driver.find_element(By.XPATH , "//input[@id='ngbDate']").send_keys("10-10-2025")
    driver.find_element(By.XPATH , "//div[@aria-label='Friday, October 10, 2025']").click()

    time.sleep(3)

    # wait.until(EC.presence_of_element_located((By.XPATH , "//select[@class='form-control ng-untouched ng-pristine ng-valid dropdown-highlight']")))

    book_now = driver.find_element(By.XPATH , "//button[@class='themeBtn rounded-theme mx-auto secondry-theme ng-star-inserted']")
    book_now.click()

    time.sleep(5)

    assert "checkout" in driver.current_url.lower() , \
    "Booking Page did not open successfully"

