class CartPage:
    def __init__(self, page):
        self.page = page
        self.cart_button = "#cartur"
        self.add_to_cart_button = "text=Add to cart"

    def add_to_cart(self, product_name):
        self.page.click(f"text={product_name}")
        self.page.click(self.add_to_cart_button)

    def go_to_cart(self):
        self.page.click(self.cart_button)

