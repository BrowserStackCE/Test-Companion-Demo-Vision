"""Central test settings. Non-secret values only; credentials come from the environment."""

DEFAULT_TIMEOUT = 30   # seconds, normal element waits
ALERT_TIMEOUT = 10     # seconds, optional OS permission dialogs
TEST_CASE_ID = "TC-1250"

# Placeholder strings the app shows in empty inputs; used to prove Auto-fill populated a field.
EMPTY_FIELD_PLACEHOLDERS = {
    "full_name": ("", "Enter your full name"),
    "email": ("", "Enter your email"),
    "password": ("", "Create a password"),
    "confirm_password": ("", "Confirm your password"),
}
