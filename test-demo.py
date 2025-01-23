import pytest
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from faker import Faker

fake = Faker()

def test_demoblaze_e2e():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Initialiser les pages
        home = HomePage(page)
        cart = CartPage(page)
        checkout = CheckoutPage(page)

        # Étape 1 : Naviguer et créer un compte
        home.navigate()
        username = fake.user_name()
        password = fake.password()
        home.sign_up(username, password)
        page.wait_for_timeout(2000)  # Attendre pour simuler l'enregistrement

        # Étape 2 : Se connecter avec l'utilisateur créé
        home.log_in(username, password)
        page.wait_for_selector("#nameofuser", timeout=5000)
        assert page.locator("#nameofuser").text_content() == f"Welcome {username}"

        # Étape 3 : Ajouter un produit au panier
        cart.add_to_cart("Samsung galaxy s6")
        page.wait_for_timeout(2000)

        # Étape 4 : Aller au panier et confirmer la commande
        cart.go_to_cart()
        checkout.complete_checkout(
            name="John Doe",
            country="USA",
            city="New York",
            card="1234 5678 8765 4321",
            month="12",
            year="2025"
        )

        # Vérification finale
        confirmation_message = checkout.get_confirmation_message()
        assert "Thank you for your purchase!" in confirmation_message

        browser.close()
