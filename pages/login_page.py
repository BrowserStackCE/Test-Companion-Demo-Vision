from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class LoginPage(BasePage):
    HEADING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Welcome Back")')
    GO_TO_SIGNUP = (AppiumBy.ACCESSIBILITY_ID, "Go to sign up")

    def is_displayed(self) -> bool:
        return self.visible(self.HEADING).is_displayed()

    def heading_text(self) -> str:
        return self.text_of(self.HEADING)

    def open_signup(self) -> None:
        self.tap(self.GO_TO_SIGNUP)
