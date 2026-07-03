from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import LoginPageLocators

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def load(self):
        self.driver.get(LOGIN_URL)
        return self

    def enter_credentials(self, username: str, password: str):
        self.wait.until(EC.visibility_of_element_located(LoginPageLocators.USERNAME_INPUT)).send_keys(username)
        self.wait.until(EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)).send_keys(password)
        return self

    def submit(self):
        self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SUBMIT_BUTTON)).click()
        return SecureAreaPage(self.driver)