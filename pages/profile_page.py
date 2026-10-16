from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


def _text(value: str):
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{value}")')


class ProfilePage(BasePage):
    ACCOUNT_DETAILS = _text("Account Details")
    SETTINGS = _text("Settings")
    DELETE_ACCOUNT = (AppiumBy.ACCESSIBILITY_ID, "Delete your account permanently")

    # Native confirmation dialog
    DIALOG_TITLE = (AppiumBy.ID, "com.yash.bankingapp:id/alert_title")
    DIALOG_MESSAGE = (AppiumBy.ID, "android:id/message")
    DIALOG_CANCEL = (AppiumBy.ID, "android:id/button2")
    DIALOG_DELETE = (AppiumBy.ID, "android:id/button1")

    def text_displayed(self, value: str) -> str:
        return self.text_of(_text(value))

    def scroll_to_delete(self) -> None:
        self.scroll_into_view("Delete your account permanently")

    def delete_button_enabled(self) -> bool:
        return self.visible(self.DELETE_ACCOUNT).is_enabled()

    def tap_delete_account(self) -> None:
        self.tap(self.DELETE_ACCOUNT)

    def dialog_title(self) -> str:
        return self.text_of(self.DIALOG_TITLE)

    def dialog_message(self) -> str:
        return self.text_of(self.DIALOG_MESSAGE)

    def dialog_cancel_label(self) -> str:
        return self.text_of(self.DIALOG_CANCEL)

    def dialog_delete_label(self) -> str:
        return self.text_of(self.DIALOG_DELETE)

    def confirm_delete(self) -> None:
        self.tap(self.DIALOG_DELETE)
