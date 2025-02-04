from playwright.sync_api import sync_playwright 
import time
import json
from freezegun import freeze_time 

# ✅ Données fictives pour le test
USER = {
    "email": "testuser@example.com",
    "password": "password123",
    "username": "testuser",
    "token": "fake-jwt-token"
}

ARTICLES = {
    "articles": [
        {"slug": "article-1", "title": "Premier Article", "description": "Description 1", "body": "Contenu 1", "author": {"username": "Auteur1"}},
        {"slug": "article-2", "title": "Deuxième Article", "description": "Description 2", "body": "Contenu 2", "author": {"username": "Auteur2"}},
        {"slug": "article-3", "title": "Troisième Article", "description": "Description 3", "body": "Contenu 3", "author": {"username": "Auteur3"}}
    ],
    "articlesCount": 3
}



def mock_conduit_api():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 🎭 Mock API - Interception des requêtes
        def mock_request(route, request):
            url = request.url

            if "api/users" in url and request.method == "POST":
                route.fulfill(status=201, content_type="application/json", body=json.dumps({"user": USER}))

            elif "api/articles" in url and request.method == "GET":
                route.fulfill(status=200, content_type="application/json", body=json.dumps(ARTICLES))

            else:
                route.continue_()

        page.route("**/*", mock_request)

       

        # 🔗 Ouvrir Conduit
        page.goto("https://conduit.bondaracademy.com/")

        # 📝 Inscription
        page.click('text=Sign up')
        page.fill('input[placeholder="Username"]', USER["username"])
        page.fill('input[placeholder="Email"]', USER["email"])
        page.fill('input[placeholder="Password"]', USER["password"])
        page.click('button:has-text("Sign up")')
        time.sleep(2)

        # 🔑 Connexion
        
        page.wait_for_load_state("networkidle")  # Attendre que la page charge complètement
        page.wait_for_selector('a.nav-link active:has-text("Sign in")', state="visible", timeout=10000)
        page.click('a.nav-link active:has-text("Sign in")')
        page.fill('input[placeholder="Email"]', USER["email"])
        page.fill('input[placeholder="Password"]', USER["password"])
        page.click('button:has-text("Sign in")')
        time.sleep(2)

        # 📰 Vérifier les articles mockés
        page.goto("https://conduit.bondaracademy.com/")
        time.sleep(3)
        
       
        print("✅ Mock API  appliqués avec succès !")
        browser.close()

# 🔥 Lancer le test
mock_conduit_api()

