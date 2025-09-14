import functools
import time
from typing import Callable, ParamSpec, TypeVar

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome as WebDriver

DEFAULT_TIMEOUT_S = 10
DEFAULT_DELAY_S = 1

P = ParamSpec("P")
R = TypeVar("R")

# Decorator factory to create wrappers for "search stage" functions that will
# log debug info and sleep before returning (to avoid being too quick to websites).
def search_stage_decorator(delay: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"running {f.__name__[1:]} ...", end=" ", flush=True)
            result = f(*args, **kwargs)
            time.sleep(delay)
            print("done.", flush=True)
            return result
        return wrapper
    return decorator


stage = search_stage_decorator(DEFAULT_DELAY_S)


class Searcher:
    def __init__(self) -> None:
        self.station_src = "PHL"
        self.station_dst = "WIL"
        self.date = "9/18/2025"

    def search(self) -> None:
        self._init_driver()
        self._allow_cookies()
        self._enter_station_codes()
        self._enter_trip_date()
        self._execute_search()

    @stage
    def _init_driver(self) -> None:
        self.driver = WebDriver(enable_cdp_events=True)
        self.driver.get("https://www.amtrak.com")

    @stage
    def _allow_cookies(self) -> None:
        button_allow_cookies = WebDriverWait(self.driver, DEFAULT_TIMEOUT_S).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        button_allow_cookies.click()

    @stage
    def _enter_station_codes(self) -> None:
        self._enter_input_by_id("mat-input-0", self.station_src)
        self._enter_input_by_id("mat-input-1", self.station_dst)

    @stage
    def _enter_trip_date(self) -> None:
        self._enter_input_by_id("mat-input-2", self.date)
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, "//am-farefinder-dates//button[contains(text(), 'Done')]")
        button.click()
        time.sleep(1)

    def _enter_input_by_id(self, id_: str, input_: str) -> None:
        e = self.driver.find_element(By.ID, id_)
        e.send_keys(input_)

    @stage
    def _execute_search(self) -> None:
        button = self.driver.find_element(By.XPATH, "//button[@amt-auto-test-id='fare-finder-findtrains-button']")
        button.click()
