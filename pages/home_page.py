from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class HomePage(BasePage):
    WELCOME_LABEL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Welcome")')
    # Tab content-desc is "<icon glyph>, <Name>": the glyph is an invisible private-use
    # character, so match the stable name part instead of the full string.
    HOME_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Home")')
    PROFILE_TAB = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Profile")')

    def wait_until_loaded(self) -> None:
        self.visible(self.WELCOME_LABEL)

    def greeting_name(self, expected_name: str) -> str:
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{expected_name}")')
        return self.text_of(locator)

    def home_tab_selected(self) -> bool:
        return self.visible(self.HOME_TAB).get_attribute("selected") == "true"

    def open_profile(self) -> None:
        self.tap(self.PROFILE_TAB)
