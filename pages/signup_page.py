from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


def _res_id(value: str):
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{value}")')


class SignupPage(BasePage):
    FULL_NAME = _res_id("fullname-input")
    EMAIL = _res_id("email-input")
    PASSWORD = _res_id("password-input")
    CONFIRM_PASSWORD = _res_id("confirm-password-input")
    AUTOFILL_NEW_USER = (AppiumBy.ACCESSIBILITY_ID, "Auto-fill")
    CREATE_ACCOUNT = (AppiumBy.ACCESSIBILITY_ID, "Create your account")
    PROGRESS = (AppiumBy.CLASS_NAME, "android.widget.ProgressBar")

    FIELDS = {
        "full_name": FULL_NAME,
        "email": EMAIL,
        "password": PASSWORD,
        "confirm_password": CONFIRM_PASSWORD,
    }

    def all_fields_displayed(self) -> bool:
        return all(self.visible(locator).is_displayed() for locator in self.FIELDS.values())

    def autofill_new_user(self) -> None:
        self.scroll_into_view("Auto-fill")
        self.tap(self.AUTOFILL_NEW_USER)

    def field_value(self, name: str) -> str:
        return self.driver.find_element(*self.FIELDS[name]).text

    def wait_for_autofill(self, name: str, placeholders: tuple) -> str:
        """Wait until a field holds real data (not empty / not its placeholder) and return it."""
        return self.wait_until(
            lambda d: (v if (v := d.find_element(*self.FIELDS[name]).text) not in placeholders else False),
            message=f"Auto-fill did not populate '{name}'",
        )

    def submit(self) -> None:
        self.tap(self.CREATE_ACCOUNT)

    def progress_shown(self) -> bool:
        return self.visible(self.PROGRESS).is_displayed()

    def submit_enabled(self) -> bool:
        return self.driver.find_element(*self.CREATE_ACCOUNT).get_attribute("enabled") == "true"
