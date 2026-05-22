import re
from playwright.sync_api import Page, expect
from Pages.login_hrm_pages import loginpage
from Pages.hrm_home_page import home_page


def test_example(page: Page) -> None:
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login = loginpage(page)
    login.login("Admin", "admin123")
    home = home_page(page)

    login_page.enter_username("Admin")
    login_page.enter_password("admin123")
    login_page.click_login() 

    expect(home.is_upgrade_button_visible()).to_be_true()
    home.click_performance()
    home.click_dashboard()
    