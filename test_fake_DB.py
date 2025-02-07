
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

#  Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
    return conn

#  Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )""")

    # Ajouter des utilisateurs si la table est vide
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [("ahmed", "AD@example.com"), ("simo", "SI@example.com"), ("yasser", "yass@example.com")]
        )
        conn.commit()

    conn.close()

#  Page d'accueil
@app.route("/", methods=["GET"])
def home():
    return "🚀 API en ligne ! Allez sur /users pour voir la liste des utilisateurs."

#  Récupérer tous les utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

# 🚀 Lancer le serveur Flask
if __name__ == "__main__":
    init_db()  # Initialise la base de données avant de démarrer
    print("🚀 Serveur en ligne sur http://127.0.0.1:5001")
    app.run(host="127.0.0.1", port=5001, debug=True)


