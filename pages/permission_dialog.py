from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class PermissionDialog(BasePage):
    """Android system permission dialogs. They are optional: a missing dialog must not fail a test."""

    NOTIFICATION_ALLOW = (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
    LOCATION_ALLOW_WHILE_USING = (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
    )

    def allow_notifications(self) -> bool:
        return self.tap_if_present(self.NOTIFICATION_ALLOW)

    def allow_location(self) -> None:
        """Location is requested right after sign-up on a fresh install, so it must appear.

        The sign-up request can be slow, hence the full default timeout instead of the short
        optional-dialog one; if the dialog never shows, fail here with a clear message.
        """
        self.tap(self.LOCATION_ALLOW_WHILE_USING)
