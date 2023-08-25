from playwright.sync_api import sync_playwright
import re


def get_integers(text):
    matches = re.findall(r'\d+', text)
    return [int(match) for match in matches]


def extract_div_name(div_text):
    div_name = re.sub(r'\(\d+\)', '', div_text).strip()
    return div_name


def check_all_divs():
    first_integers_sum = 0
    categories_sum = 0

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.lifeatspotify.com/jobs")
        page.click("text=Category")

        category_divs = page.query_selector_all(".desktopoptions_options__-vKlV > div")

        all_divs = []

        for div in category_divs:
            text = div.inner_text()
            integers = get_integers(text)

            if div.query_selector_all('*'):
                all_divs.append((text, integers))
                first_integers_sum += integers[0]
                categories_sum += sum(integers[1:])

        print("Integers in Categories:")
        for div, integers in all_divs:
            div_text = div.split("\n")[0]
            div_name = extract_div_name(div_text)
            print(f"Integers of {div_name}: {integers}")
            if len(integers) > 1:
                first_integer, *rest_integers = integers
                sum_of_rest = sum(rest_integers)
                if first_integer == sum_of_rest:
                    print(f"First integer {first_integer} in {div_name} is equal to the sum of "
                          f"the rest of the integers {sum_of_rest}.")
                else:
                    print(f"First integer {first_integer} in {div_name} is not equal to the sum of "
                          f"the rest of the integers {sum_of_rest}.")

        if first_integers_sum == categories_sum:
            print(f"The sum of integers in all parent categories ({first_integers_sum}) is equal to the sum of"
                  f" all their children ({categories_sum}).")
        else:
            print(f"The sum of integers in all parent categories ({first_integers_sum}) is not equal to the sum of"
                  f" all children ({categories_sum}).")

        context.close()
        browser.close()

    return first_integers_sum, categories_sum


sum_first_integers, category_sum = check_all_divs()
