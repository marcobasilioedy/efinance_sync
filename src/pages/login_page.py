from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from errors.custom_errors import InvalidLoginCredentials

def login(driver, wait, credentials):
    try:
        wait.until(lambda d: d.find_element(By.ID, "txtEmpresa"))
    except TimeoutException:
        driver.refresh()
        wait.until(lambda d: d.find_element(By.ID, "txtEmpresa"))

    driver.find_element(By.ID, "txtEmpresa").send_keys(credentials['enterprise'])
    driver.find_element(By.ID, "txtLoja").send_keys(credentials['store'])
    driver.find_element(By.ID, "txtLogin").send_keys(credentials['user'])
    driver.find_element(By.ID, "txtSenha").send_keys(credentials['password'])
    driver.find_element(By.ID, "ext-gen45").click()

    time.sleep(2)

    try:
        aviso = driver.find_element(By.ID, "lblAviso")
        if any(erro in aviso.text.lower() for erro in [
            "acesso inválido",
            "loja não cadastrada",
            "empresa não cadastrada",
            "usuário bloqueado"
        ]):
            raise InvalidLoginCredentials()
    except TimeoutException:
        pass
    except Exception as e:
        raise e   
