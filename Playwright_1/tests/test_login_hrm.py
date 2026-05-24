import re
from playwright.sync_api import Page 
from Pages.login_hrm_pages import loginpage
from Pages.hrm_home_page import home_page


def test_example(page: Page) -> None:
    login = loginpage(page)
    home = home_page(page)
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
   
    login.enter_username("Admin")
    login.enter_password("admin123")
    login.click_login() 

    home.is_upgrade_button_visible()
    home.click_performance()
    home.click_dashboard()
    