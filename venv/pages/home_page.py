class HomePage:
    def __init__(self, page):
        self.page = page
        self.signin_button = "#signin2"
        self.login_button = "#login2"
        self.username_field = "#sign-username"
        self.password_field = "#sign-password"
        self.register_button = "button[onclick='register()']"

    def navigate(self):
        self.page.goto("https://www.demoblaze.com/")

    def sign_up(self, username, password):
        self.page.click(self.signin_button)
        self.page.fill(self.username_field, username)
        self.page.fill(self.password_field, password)
        self.page.click(self.register_button)

    def log_in(self, username, password):
        self.page.click(self.login_button)
        self.page.fill("#loginusername", username)
        self.page.fill("#loginpassword", password)
        self.page.click("button[onclick='logIn()']")
