from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_TIMEOUT, ALERT_TIMEOUT


class BasePage:
    """Shared explicit-wait helpers. No fixed sleeps anywhere: every wait is condition based."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def visible(self, locator, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def present(self, locator, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def clickable(self, locator, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def tap(self, locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.clickable(locator, timeout).click()

    def text_of(self, locator, timeout: int = DEFAULT_TIMEOUT) -> str:
        return self.visible(locator, timeout).text

    def wait_until(self, condition, timeout: int = DEFAULT_TIMEOUT, message: str = ""):
        return WebDriverWait(self.driver, timeout).until(condition, message)

    def scroll_into_view(self, description: str) -> None:
        """Scroll the first scrollable container until the element with this content-desc is on screen."""
        self.driver.find_element(
            "-android uiautomator",
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().description("{description}"))',
        )

    def tap_if_present(self, locator, timeout: int = ALERT_TIMEOUT) -> bool:
        """Tap an element that may legitimately not appear (e.g. an OS permission dialog)."""
        try:
            self.clickable(locator, timeout).click()
            return True
        except TimeoutException:
            return False
