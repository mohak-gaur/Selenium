from selenium.webdriver.common.by import By

class HomePageLocators:
    Register = (By.CSS_SELECTOR,"a[class='ico-register']")
    Login = (By.CSS_SELECTOR,"a[class='ico-login']")
    SearchField = (By.ID,"small-searchterms")
    SearchButton=(By.CSS_SELECTOR,"button[type='submit']")

class RegisterPageLocators:
    Gender = (By.ID, "gender-male")
    FirstName = (By.ID, "FirstName")
    LastName = (By.ID, "LastName")
    Email = (By.ID , "Email")
    Password = (By.ID , "Password")
    ConfPassword = (By.ID , "ConfirmPassword")
    RegisterButton = (By.ID, "register-button")

class LoginPageLocators:
    Email = (By.XPATH , "//input[@id='Email']")
    Password = (By.XPATH, "//input[@id='Password']")
    LoginButton = (By.CSS_SELECTOR,".button-1.login-button")
    ForgetPass = (By.LINK_TEXT , "passwordrecovery")
    ErrorMessage = (By.CSS_SELECTOR,".message-error.validation-summary-errors")