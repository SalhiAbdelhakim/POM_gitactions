class CheckoutPage:
    def __init__(self, page):
        self.page = page
        self.purchase_button = "button[onclick='purchaseOrder()']"

    def complete_checkout(self, name, country, city, card, month, year):
        self.page.click("button[data-target='#orderModal']")
        self.page.wait_for_selector("#name", timeout=10000)
        self.page.fill("#name", name)
        self.page.fill("#country", country)
        self.page.fill("#city", city)
        self.page.fill("#card", card)
        self.page.fill("#month", month)
        self.page.fill("#year", year)
        self.page.click(self.purchase_button)

    def get_confirmation_message(self):
        return self.page.locator(".sweet-alert h2").text_content()

