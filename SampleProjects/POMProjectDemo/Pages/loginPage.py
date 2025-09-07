from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage():

    def __init__(self , driver):
        self.driver = driver
        self.username_textbox_name = 'username'
        self.password_textbox_name = 'password'
        self.login_button_xpath = '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button'


    def enter_username(self,username):
        WebDriverWait(self.driver,20).until(
            EC.presence_of_element_located((By.NAME , self.username_textbox_name))
        )
        self.driver.find_element(By.NAME , self.username_textbox_name).clear()
        self.driver.find_element(By.NAME , self.username_textbox_name).send_keys(username)

    def enter_password(self,password):
        self.driver.find_element(By.NAME , self.password_textbox_name).clear()
        self.driver.find_element(By.NAME , self.password_textbox_name).send_keys(password)

    def enter_login(self):
        self.driver.find_element(By.XPATH , self.login_button_xpath).click()