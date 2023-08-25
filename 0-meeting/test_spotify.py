from playwright.sync_api import Playwright, sync_playwright
import re
from test_categories import sum_first_integers, category_sum


def get_elements_with_integer_values(page, wrapper_selector, excluded_selector=None):
    selector = wrapper_selector
    if excluded_selector:
        selector += f" > :not({excluded_selector})"

    elements = page.query_selector_all(selector)
    values = []

    for element in elements:
        text = element.text_content()
        matches = re.findall(r'\d+', text)
        integers = [int(match) for match in matches]
        values.extend(integers)

    return values


def test_spotify(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # try:
    page.goto("https://www.lifeatspotify.com/jobs")
    # context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.get_by_role("button", name="Accept Cookies").click()
    page.get_by_role("button", name="Close").click()

    page.get_by_text("Location", exact=True).click()
    location_wrapper_selector = ".desktopoptions_options__-vKlV"
    location_excluded_selector = ".mt-0.pb-20"
    location_values = get_elements_with_integer_values(page, location_wrapper_selector, location_excluded_selector)
    location_sum = sum(location_values)

    print("Integers in Location: ")
    for value in location_values:
        print(value, end=' ')

    print("\nSum of integers in Location:", location_sum)

    # page.get_by_text("Category", exact=True).click()
    # category_wrapper_selector = ".desktopoptions_options__-vKlV"
    # category_excluded_selector = ".mt-0.pb-20"
    # category_values = get_elements_with_integer_values(page, category_wrapper_selector, category_excluded_selector)
    # category_sum = sum(category_values)
    #
    # print("Integers in Category: ")
    # for value in category_values:
    #     print(value, end=' ')
    #
    # print("\nSum of integers in Category:", category_sum)

    page.get_by_text("Job type", exact=True).click()
    job_type_wrapper_selector = ".desktopoptions_options__-vKlV"
    job_type_values = get_elements_with_integer_values(page, job_type_wrapper_selector)
    job_type_sum = sum(job_type_values)

    print("Integers in Job type: ")
    for value in job_type_values:
        print(value, end=' ')

    print("\nSum of integers in Job type:", job_type_sum)

    if location_sum == job_type_sum == sum_first_integers == category_sum:
        assert True, (f"Sum of integers in: {sum_first_integers} Total, {location_sum} Location, "
                      f"{category_sum} Category, {job_type_sum} Job type categories is equal.")
    else:
        assert False, (f"Sum of integers in: {sum_first_integers} Total, {location_sum} Location, "
                       f"{category_sum} Category, {job_type_sum} Job type categories is not equal.")
    # finally:
    # context.tracing.stop(path="trace.zip")
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as pw:
        test_spotify(pw)
