from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(text)

    def verify_text(self, selector: str, expected_text: str):
        assert self.page.locator(selector).inner_text() == expected_text

    def verify_visible(self, selector: str):
        assert self.page.locator(selector).is_visible()
