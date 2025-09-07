from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class HomePage():

    def __init__(self ,driver):
        self.driver = driver

        self.name_dropdown_class = 'oxd-userdropdown-name'
        self.logout_button_xpath = '//*[@id="app"]/div[1]/div[1]/header/div[1]/div[3]/ul/li/ul/li[4]/a'


    def click_dropdown(self):
        WebDriverWait(self.driver,20).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.name_dropdown_class))
        )
        self.driver.find_element(By.CLASS_NAME , self.name_dropdown_class).click()


    def click_logout(self):
        self.driver.find_element(By.XPATH, self.logout_button_xpath).click()