from core import (create_driver, create_wait)
from pages import login
from constants import (URL, ENTERPRISE, STORE, USER, PASSWORD)
import re

class GetToken:
    def get_token(self):
        driver = create_driver()
        wait = create_wait(driver)

        driver.get(URL)

        login(driver, wait, {
            'enterprise': ENTERPRISE,
            'store': STORE,
            'user': USER,
            'password': PASSWORD
        })

        current_url = driver.current_url

        match = re.search(r'\(S\(([^)]+)\)\)', current_url)
        session_id = match.group(1)
        driver.quit()

        return session_id