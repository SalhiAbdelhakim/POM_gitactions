from playwright.sync_api import sync_playwright

def test_api():
    with sync_playwright() as p:
        # Lancer le navigateur
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Faire une requête GET
        # response = context.request.get("https://jsonplaceholder.typicode.com/posts/1")
        
        # # Vérifier le statut et les données
        # assert response.status == 200, "Statut attendu : 200"
        # data = response.json()
        # assert data["id"] == 1, "ID attendu : 1"
        # assert "title" in data, "La clé 'title' devrait exister"


        # payload = {"title": "foo", "body": "bar", "userId": 1}
        # response = context.request.post(
        # "https://jsonplaceholder.typicode.com/posts",
        # data=payload
        # )
        # assert response.status == 201
        # print(response.json())


        # xx = {"id": 1, "title": "foo", "body": "updated___content", "userId": 1}
        # response = context.request.put(
        # "https://jsonplaceholder.typicode.com/posts/1",
        # data=xx
        # )
        # assert response.status == 200
        # print(response.json())


        response = context.request.delete("https://jsonplaceholder.typicode.com/posts/1")
        # assert response.status == 204
        print(response.status)



        print("Test réussi avec succès !")

        # Fermer le navigateur
        browser.close()

# if __name__ == "__main__":
test_api()
