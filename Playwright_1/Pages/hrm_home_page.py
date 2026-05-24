from playwright.sync_api import Page, expect

class home_page:
    def __init__(self, page: Page):
        self.page = page
        self.upgrade_btn = page.get_by_role("button", name="Upgrade")
        self.performance_link = page.get_by_role("link", name="Performance")
        self.dashboard_link = page.get_by_role("link", name="Dashboard")

    def is_upgrade_button_visible(self):
        return self.upgrade_btn.is_visible()
    
    def click_performance(self):
        return self.performance_link.click()
    
    def click_dashboard(self):
        self.dashboard_link.click()