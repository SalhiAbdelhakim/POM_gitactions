from playwright.sync_api import sync_playwright
import json

# URLs
API_URL = "https://conduit-api.bondaracademy.com/api"

# Identifiants de connexion (modifie-les avec des identifiants valides)
EMAIL = "koko@gmail.com"
PASSWORD = "123"

def test_api():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        api_context = context.request

        # 1️⃣ Connexion et récupération du token
        login_data = json.dumps({"user": {"email": EMAIL, "password": PASSWORD}})
        login_response = api_context.post(f"{API_URL}/users/login", data=login_data, headers={"Content-Type": "application/json"})

        # Vérifier si la connexion réussit
        if login_response.status != 200:
            print("❌ Erreur de connexion:", login_response.text())
            return

        print("✅ Connexion réussie !")
        token = login_response.json()["user"]["token"]
        headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

        # 2️⃣ Création d'un article
        article_data = json.dumps({
            "article": {
                "title": "free",
                "description": "Un article créé avec Playwright",
                "body": "Ceci est un test d'API avec Playwright.",
                "tagList": ["playwright", "test"]
            }
        })
        create_response = api_context.post(f"{API_URL}/articles", data=article_data, headers=headers)

        if create_response.status != 201:
            print("❌ Erreur lors de la création de l'article:", create_response.text())
            return

        slug = create_response.json()["article"]["slug"]
        print(f"✅ Article créé avec succès ! Slug : {slug}")

        # 3️⃣ Récupération de l'article
        view_response = api_context.get(f"{API_URL}/articles/{slug}")

        if view_response.status != 200:
            print("❌ Erreur lors de la récupération de l'article:", view_response.text())
            return

        print(f"✅ Article récupéré : {view_response.json()['article']['title']}")

        # 4️⃣ Modification de l'article
        update_data = json.dumps({
            "article": {
                "title": "pilott",
                "description": "Mise à jour du test",
                "body": "Contenu mis à jour."
            }
        })
        update_response = api_context.put(f"{API_URL}/articles/{slug}", data=update_data, headers=headers)

        if update_response.status != 200:
            print("❌ Erreur lors de la modification de l'article:", update_response.text())
            return

        print("✅ Article modifié avec succès !")

        # 5️⃣ Suppression de l'article
        delete_response = api_context.delete(f"{API_URL}/articles/{slug}", headers=headers)

        if delete_response.status != 204:
            print("❌ Erreur lors de la suppression de l'article:", delete_response.text())
            return

        print("✅ Article supprimé avec succès !")

        browser.close()

if __name__ == "__main__":
    test_api()
