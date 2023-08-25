from playwright.sync_api import Playwright, sync_playwright
import time

def test_helicon_2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://helicon.ai/")
    time.sleep(2)
