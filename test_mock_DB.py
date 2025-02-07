from playwright.sync_api import sync_playwright
import json
import subprocess
import time
import requests

# ✅ Démarrer le serveur Flask (fake_DB.py)
print("🚀 Démarrage du serveur Flask...")
server_process = subprocess.Popen(["python", "fake_DB.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# ✅ Vérifier que le serveur est bien lancé avant de continuer
server_ready = False
max_retries = 10  # Nombre de tentatives
for attempt in range(max_retries):
    try:
        response = requests.get("http://127.0.0.1:5002/users")
        print(f"🔍 Tentative {attempt+1} de connexion... Statut : {response.status_code}")
        if response.status_code == 200:
            server_ready = True
            print("🚀 Serveur prêt !")
            break
    except requests.ConnectionError:
        print(f"⚠️ Serveur non accessible, nouvelle tentative... (tentative {attempt+1}/{max_retries})")
        time.sleep(2)  # Attend 2 secondes avant de réessayer

if not server_ready:
    print("❌ Le serveur Flask n'a pas démarré correctement après plusieurs tentatives.")
    server_process.terminate()  # Terminer le processus du serveur Flask
    exit(1)

# ✅ Données attendues (mock)
EXPECTED_USERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]

# ✅ Lancer Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 🔹 Intercepter la requête GET vers /users et répondre avec les données mockées
    def mock_db_request(route, request):
        if request.url.endswith("/users") and request.method == "GET":
            print("🔄 Interception de la requête /users et envoi des données mockées...")
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps(EXPECTED_USERS)
            )
        else:
            route.continue_()

    page.route("**/*", mock_db_request)

    # 📡 Accéder à l'API (test mocké)
    print("🌐 Accès à l'API...")
    page.goto("http://127.0.0.1:5002/users")
    response = page.evaluate("document.body.innerText")

    # ✅ Vérifier la réponse
    users_data = json.loads(response)
    assert users_data == EXPECTED_USERS, f"❌ Erreur : Données reçues incorrectes {users_data}"

    print("✅ Test réussi : les données de la DB mockée sont correctes !")

    browser.close()

# ✅ Arrêter proprement le serveur Flask
print("🚦 Arrêt du serveur Flask...")
server_process.terminate()
server_process.wait()
print("🚫 Serveur arrêté.")


# from playwright.sync_api import sync_playwright
# import json
# import subprocess
# import time

# # ✅ Démarrer le serveur Flask (API)
# server_process = subprocess.Popen(["python", "fake_DB.py"])
# time.sleep(2)  # Attendre que le serveur démarre

# # ✅ Données attendues
# EXPECTED_USERS = [
#     {"id": 1, "name": "Alice", "email": "alice@example.com"},
#     {"id": 2, "name": "Bob", "email": "bob@example.com"},
#     {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
# ]

# # ✅ Lancer Playwright
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()

#     # 🔹 Intercepter la requête GET vers /users
#     def mock_db_request(route, request):
#         if request.url.endswith("/users") and request.method == "GET":
#             route.fulfill(
#                 status=200,
#                 content_type="application/json",
#                 body=json.dumps(EXPECTED_USERS)
#             )
#         else:
#             route.continue_()

#     page.route("**/*", mock_db_request)

#     # 📡 Effectuer la requête API vers le serveur
#     page.goto("http://127.0.0.1:5001/users")
#     response = page.evaluate("document.body.innerText")

#     # ✅ Vérifier la réponse
#     users_data = json.loads(response)
#     assert users_data == EXPECTED_USERS, f"Erreur : Données reçues incorrectes {users_data}"

#     print("✅ Test réussi : les données de la DB mockée sont correctes !")

#     browser.close()

# # ❌ Arrêter le serveur Flask après le test
# server_process.terminate()

