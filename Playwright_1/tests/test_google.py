import re
from playwright.sync_api import expect

def test_google_search(page):
    page.wait_for_timeout(3000)
    page.goto("https://www.google.com/ncr")

    try:
        page.get_by_role("button", name="Accept all").click(timeout=5000)
    except:
        print("No popup")

    page.get_by_role("combobox", name="Search").fill("Playwright python")

    page.keyboard.press("Enter")

    expect(page).to_have_title(re.compile("Playwright",re.IGNORECASE))            