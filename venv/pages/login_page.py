from pages.base_page import BasePage

class LoginPage(BasePage):
    def login(self, username: str, password: str):
        self.fill("#loginusername", username)
        self.fill("#loginpassword", password)
        self.click("button:has-text('Log in')")
