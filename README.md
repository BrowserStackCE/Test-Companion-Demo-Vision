# Banking app – Android BDD tests (Appium + pytest-bdd on BrowserStack App Automate)

Gherkin scenarios in `features/` run on real Android devices through the BrowserStack SDK.

## Layout

```
browserstack.yml              BrowserStack config: project, build, device (app id comes from BROWSERSTACK_APP_ID)
pytest.ini                    pytest / pytest-bdd settings and markers
requirements.txt              pinned dependencies
features/                     Gherkin feature files (the test cases)
tests/
  conftest.py                 driver fixture, page-object fixtures, session status, failure evidence
  test_*.py                   binds a feature file to pytest (scenarios(...))
  steps/                      step definitions (no locators here)
pages/                        page objects: ALL locators live here
config/settings.py            timeouts, test case id, non-secret constants
```

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # then fill in your credentials, never commit .env
set -a; source .env; set +a
```

## Run

```bash
browserstack-sdk pytest                          # whole suite
browserstack-sdk pytest -m signup                # by tag
browserstack-sdk pytest -k tc1250                # by test case id
```

Results appear in BrowserStack Test Reporting & Analytics (link printed at the end of the run).

## Updating the app build

The app id is not stored in the repo. Upload the build to BrowserStack and export its `bs://` id before running:

```bash
export BROWSERSTACK_APP_ID=bs://<your-app-id>    # or put it in .env
```

## Conventions

- Feature files hold behaviour only; steps call page-object methods; locators exist only in `pages/`.
- Prefer accessibility id / resource-id; the bottom tab labels start with an invisible icon glyph, so they are matched with `descriptionContains`.
- No fixed sleeps: use the explicit waits in `pages/base_page.py`.
- Each scenario name ends with its Test Management id (e.g. `TC-1250`), and `conftest.py` also tags the session with it.
- The BrowserStack SDK needs `selenium==4.9.1` with Appium-Python-Client 2.6.1; do not upgrade one without the other.
- Every scenario creates and deletes its own user via the app's Auto-fill, so scenarios do not share state.
