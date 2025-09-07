from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path=r'C:\Programs\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.maximize_window()

driver.get('https://www.youtube.com')

wait = WebDriverWait(driver,10)

search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , "input[name='search_query']")))
search.send_keys("But Why")

driver.find_element(By.CSS_SELECTOR , "button[title='Search']").click()

desc = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "yt-formatted-string[id=description]")))

# print(desc[0].text)

desc[0].click()

subscribe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , "button.yt-spec-button-shape-next.yt-spec-button-shape-next--filled.yt-spec-button-shape-next--mono.yt-spec-button-shape-next--size-m.yt-spec-button-shape-next--enable-backdrop-filter-experiment")))
subscribe.click()

time.sleep(10)

driver.close()
driver.quit()