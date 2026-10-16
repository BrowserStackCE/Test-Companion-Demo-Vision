import json

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import TEST_CASE_ID
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.permission_dialog import PermissionDialog
from pages.profile_page import ProfilePage
from pages.signup_page import SignupPage

# Step definitions live in tests/steps; registering them as a plugin makes them visible to every scenario.
pytest_plugins = ["tests.steps.signup_delete_steps"]

# BrowserStack SDK injects the hub URL, credentials, device and app from browserstack.yml.
HUB_URL = "https://hub.browserstack.com/wd/hub"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def driver(request):
    options = UiAutomator2Options().load_capabilities({"platformName": "android"})
    drv = webdriver.Remote(HUB_URL, options=options)
    drv.set_custom_tag("ID", TEST_CASE_ID)
    yield drv
    report = getattr(request.node, "rep_call", None)
    passed = bool(report and report.passed)
    if not passed:
        # Leave evidence of the screen the failure happened on (visible in the pytest output).
        try:
            print("\n[FAILURE_PAGE_SOURCE]\n" + drv.page_source)
        except Exception as exc:  # the session may already be gone
            print(f"\n[FAILURE_PAGE_SOURCE] unavailable: {exc}")
    reason = "Scenario passed" if passed else "Scenario failed, see the pytest output"
    drv.execute_script(
        "browserstack_executor: "
        + json.dumps(
            {
                "action": "setSessionStatus",
                "arguments": {"status": "passed" if passed else "failed", "reason": reason},
            }
        )
    )
    drv.quit()


@pytest.fixture
def context():
    """Scenario-scoped bag for values generated at run time (e.g. the auto-filled user)."""
    return {}


@pytest.fixture
def permissions(driver):
    return PermissionDialog(driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def signup_page(driver):
    return SignupPage(driver)


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)
