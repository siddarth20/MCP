from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import SecureAreaLocators

class SecureAreaPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def is_loaded(self):
        self.wait.until(EC.visibility_of_element_located(SecureAreaLocators.HEADER))
        return self

    def get_flash_message(self):
        return self.wait.until(EC.visibility_of_element_located(SecureAreaLocators.FLASH_MESSAGE)).text

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(SecureAreaLocators.LOGOUT_BUTTON)).click()
        return LoginPage(self.driver)