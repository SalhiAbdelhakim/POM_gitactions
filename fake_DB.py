from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# ✅ Fonction pour créer une base de données SQLite en mémoire
def create_mock_db():
    conn = sqlite3.connect(":memory:")  # Base en mémoire
    cursor = conn.cursor()
    
    # 🔹 Création de la table 'users'
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )""")

    # 🔹 Insertion de données fictives
    users = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com"),
        ("Charlie", "charlie@example.com")
    ]
    
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
    conn.commit()
    
    return conn

# ✅ Instance de la base mockée
mock_db_conn = create_mock_db()

@app.route("/users", methods=["GET"])
def get_users():
    cursor = mock_db_conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
    return jsonify(users)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
