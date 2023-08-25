**INSTALLATION OF PLAYWRIGHT**

```
pip install playwright
playwright install
pip install pytest
pip install pytest-playwright
```
Run this in the terminal whenever you start a project using Playwright.

**Official Playwright documentation:**
[PlaywrightDocs](https://playwright.dev/python/docs/intro)

Start every file name with test and every function with test in order to run Pytest Playwright tests.

To run the code itself use ```python3 %file_name%```, for tests run ```pytest %file_name%*```

Playwright supports lots of CLI commands, some of the most useful are:
```
-- slowmo 1000 (any number can be here, miliseconds), makes tests run a bit slower due to high speed of Playwright
-- headed (shows what happens in real test)
-- browser (chromium/firefox/webkit)
-- device (="iPhone 12 Pro" for instance if you want to try your test there)
-- video (if to enable video for every test, can be on/off/retain-on-failure)
-- screenshot (if to enable screenshot for every test, can be on/off/retain-on-failure)
-- tracing (snapshots, screenshots, sources. You should indicate where to start (usually after goto.page) and where to end tracing (usually before ))
and many more
```

**Link to all Playwright devices list:**
[DevicesAPI](https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json)
