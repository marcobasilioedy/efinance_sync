from selenium.webdriver.support.ui import WebDriverWait

def create_wait(driver, timeout=30):
    return WebDriverWait(driver, timeout)
