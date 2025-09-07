
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_geckodriver import Firefox as WebDriver
import time

DEFAULT_TIMEOUT_S = 10

class Searcher:

    def __init__(self):
        self.station_src = "PHL"
        self.station_dst = "WIL"
        self.date = "9/10/2025"

    def search(self) -> None:
        self._init_driver()
        self._allow_cookies()
        self._enter_station_codes()
        self._enter_trip_date()
        self._execute_search()

    def _init_driver(self) -> None:
        print("beginning search.")
        self.driver = WebDriver()
        self.driver.get("https://www.amtrak.com")

    def _allow_cookies(self) -> None:
        print("waiting to accept cookies...", end=" ")
        button_allow_cookies = WebDriverWait(self.driver, DEFAULT_TIMEOUT_S).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        button_allow_cookies.click()
        print("done.")

    def _enter_station_codes(self) -> None:
        print("entering station codes...", end="")
        self._enter_input_by_id("mat-input-0", self.station_src)
        self._enter_input_by_id("mat-input-1", self.station_dst)
        print("done.")

    def _enter_trip_date(self) -> None:
        print("entering trip date...", end="")
        self._enter_input_by_id("mat-input-2", self.date)
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, "//am-farefinder-dates//button[contains(text(), 'Done')]")
        button.click()
        time.sleep(1)
        print("done.")

    def _enter_input_by_id(self, id_: str, input_: str) -> None:
        e = self.driver.find_element(By.ID, id_)
        e.send_keys(input_)

    def _execute_search(self) -> None:
        print("executing search...", end="")
        button = self.driver.find_element(By.XPATH, "//button[@amt-auto-test-id='fare-finder-findtrains-button']")
        button.click()
        print("done.")
