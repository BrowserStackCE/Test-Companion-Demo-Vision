@android @TC-1250
Feature: Account lifecycle
  As a new customer of the banking app
  I want to register and later permanently delete my account
  So that I stay in control of my personal data

  Background:
    Given the app is freshly installed and the notification permission is accepted

  @signup @delete-account @regression
  Scenario: Sign up a new user and delete the account from Profile TC-1250
    Given the user is on the Login screen
    When the user taps "Don't have an account? Sign Up"
    Then the Create Account screen shows the Full Name, Email, Password and Confirm Password fields
    When the user scrolls down and taps the Auto-fill button
    Then the Full Name, Email, Password and Confirm Password fields are populated with generated data
    When the user taps Create Account
    Then the Create Account button shows a progress indicator and is disabled
    When the location permission is accepted
    Then the Home screen greets the newly signed-up user by name
    And the Home tab is selected
    When the user opens the Profile tab and scrolls to the bottom
    Then the Profile shows the new user's email, Account Details and Settings
    And the Delete Account button is visible and enabled
    When the user taps Delete Account
    Then a Delete Account confirmation dialog warns "This will permanently delete your account and all data. This cannot be undone."
    And the dialog offers CANCEL and DELETE
    When the user taps DELETE
    Then the user is returned to the Login screen
