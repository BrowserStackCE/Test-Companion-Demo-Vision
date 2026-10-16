from pytest_bdd import given, parsers, then, when

from config.settings import EMPTY_FIELD_PLACEHOLDERS

DELETE_DIALOG_MESSAGE = "This will permanently delete your account and all data. This cannot be undone."


# ---------- Background / Given ----------
@given("the app is freshly installed and the notification permission is accepted")
def accept_notifications(permissions):
    permissions.allow_notifications()


@given("the user is on the Login screen")
def on_login_screen(login_page):
    assert login_page.is_displayed()
    assert login_page.heading_text() == "Welcome Back"


# ---------- Sign up ----------
@when("the user taps \"Don't have an account? Sign Up\"")
def tap_sign_up(login_page):
    login_page.open_signup()


@then("the Create Account screen shows the Full Name, Email, Password and Confirm Password fields")
def create_account_fields_visible(signup_page):
    assert signup_page.all_fields_displayed()


@when("the user scrolls down and taps the Auto-fill button")
def tap_autofill(signup_page):
    signup_page.autofill_new_user()


@then("the Full Name, Email, Password and Confirm Password fields are populated with generated data")
def fields_populated(signup_page, context):
    values = {
        name: signup_page.wait_for_autofill(name, placeholders)
        for name, placeholders in EMPTY_FIELD_PLACEHOLDERS.items()
    }
    assert "@" in values["email"], f"Auto-filled email is not an email: {values['email']!r}"
    assert values["password"], "Auto-fill left the Password field empty"
    assert values["confirm_password"], "Auto-fill left the Confirm Password field empty"
    context["full_name"] = values["full_name"]
    context["email"] = values["email"]


@when("the user taps Create Account")
def tap_create_account(signup_page):
    signup_page.submit()


@then("the Create Account button shows a progress indicator and is disabled")
def progress_and_disabled(signup_page):
    assert signup_page.progress_shown()
    assert not signup_page.submit_enabled()


@when("the location permission is accepted")
def accept_location(permissions):
    permissions.allow_location()


# ---------- Home ----------
@then("the Home screen greets the newly signed-up user by name")
def greeting_shows_new_user(home_page, context):
    home_page.wait_until_loaded()
    assert home_page.greeting_name(context["full_name"]) == context["full_name"]


@then("the Home tab is selected")
def home_tab_selected(home_page):
    assert home_page.home_tab_selected()


# ---------- Profile ----------
@when("the user opens the Profile tab and scrolls to the bottom")
def open_profile_and_scroll(home_page, profile_page):
    home_page.open_profile()
    profile_page.scroll_to_delete()


@then("the Profile shows the new user's email, Account Details and Settings")
def profile_content(profile_page, context):
    assert profile_page.text_displayed(context["email"]) == context["email"]
    assert profile_page.text_displayed("Account Details") == "Account Details"
    assert profile_page.text_displayed("Settings") == "Settings"


@then("the Delete Account button is visible and enabled")
def delete_button_enabled(profile_page):
    assert profile_page.delete_button_enabled()


@when("the user taps Delete Account")
def tap_delete_account(profile_page):
    profile_page.tap_delete_account()


@then(parsers.parse('a Delete Account confirmation dialog warns "{message}"'))
def confirmation_dialog(profile_page, message):
    assert message == DELETE_DIALOG_MESSAGE
    assert profile_page.dialog_title() == "Delete Account"
    assert profile_page.dialog_message() == message


@then("the dialog offers CANCEL and DELETE")
def dialog_buttons(profile_page):
    assert profile_page.dialog_cancel_label() == "CANCEL"
    assert profile_page.dialog_delete_label() == "DELETE"


@when("the user taps DELETE")
def tap_delete(profile_page):
    profile_page.confirm_delete()


@then("the user is returned to the Login screen")
def back_on_login(login_page):
    assert login_page.heading_text() == "Welcome Back"
