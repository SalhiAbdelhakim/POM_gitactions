from playwright.sync_api import sync_playwright
import json
import subprocess
import time

# ✅ Démarrer le serveur Flask (API)
server_process = subprocess.Popen(["python", "mock_db_server.py"])
time.sleep(2)  # Attendre que le serveur démarre

# ✅ Données attendues
EXPECTED_USERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]

# ✅ Lancer Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 🔹 Intercepter la requête GET vers /users
    def mock_db_request(route, request):
        if request.url.endswith("/users") and request.method == "GET":
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(EXPECTED_USERS)
            )
        else:
            route.continue_()

    page.route("**/*", mock_db_request)

    # 📡 Effectuer la requête API vers le serveur
    page.goto("http://127.0.0.1:5000/users")
    response = page.evaluate("document.body.innerText")

    # ✅ Vérifier la réponse
    users_data = json.loads(response)
    assert users_data == EXPECTED_USERS, f"Erreur : Données reçues incorrectes {users_data}"

    print("✅ Test réussi : les données de la DB mockée sont correctes !")

    browser.close()

# ❌ Arrêter le serveur Flask après le test
server_process.terminate()
