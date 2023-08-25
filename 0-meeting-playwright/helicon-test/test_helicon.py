from playwright.sync_api import Playwright, sync_playwright
import time


def test_helicon(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()  # **playwright.devices["iPhone 12 Pro landscape"]
    page = context.new_page()
    page.goto("https://helicon.ai/")
    # context.tracing.start(snapshots=True, screenshots=True, sources=True)
    page.get_by_text("By continuing to browse, you agree to our use of cookies.").click()
    page.get_by_role("button", name="Got it!").click()
    page.get_by_role("banner").get_by_role("link", name="Jobs").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Senior Full-stack Developer ➝").click()
    page1 = page1_info.value
    page1.get_by_role("button", name="Accept all").click()

    (page1.locator("section").filter
     (has_text="Stockholm · Hybrid Remote Senior Full-stack Developer Apply for this job")
     .get_by_role("button", name="Apply for this job").click())
    time.sleep(2)

    assert page1.query_selector("text=upload CV") is not None, "upload CV text not found on the page"
    page1.get_by_role("group", name="Do you have a work permit for a EU country?*").click()
    page1.get_by_text("No", exact=True).click()
    page1.get_by_label("How many years of experience do you have with frontend development?").click()
    page1.get_by_label("How many years of experience do you have with frontend development?").fill("5")
    page1.mouse.wheel(0, 300)
    time.sleep(2)
    page1.mouse.wheel(0, 1500)
    # page1.get_by_label("Upload CV").set_input_files('/Users/pavelbuzin/Desktop/Pavel Introduction.pdf')
    # time.sleep(10)
#     context.tracing.stop(path="trace1.zip")


def test_input(playwright: Playwright) -> None:  # Corrected argument name here
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page1 = context.new_page()
    page1.goto("https://helicontechnologies.teamtailor.com/jobs/2333453-senior-full-stack-developer")
#     context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page1.get_by_role("button", name="Accept all").click()

    text_element = page1.get_by_text("Upload CV")
    if text_element:
        text_element.scroll_into_view_if_needed()

    file_input = page1.get_by_label("Upload CV")
    file_path = '/Users/pavelbuzin/Desktop/Pavel Introduction.pdf'
    file_input.set_input_files(file_path)

    uploaded_file_element = page1.query_selector("text=Pavel Introduction.pdf")
    assert uploaded_file_element is not None, "File was not uploaded successfully"

#     context.tracing.stop(path="trace2.zip")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_helicon(playwright)
        test_input(playwright)

# PWDEBUG=1 pytest -s ...
# DEBUG=pw:api pytest -s ...
